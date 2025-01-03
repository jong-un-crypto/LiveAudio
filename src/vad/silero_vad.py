from .vad_interface import VADInterface

import torch
import numpy as np

class SileroVAD(VADInterface):
    def __init__(self,  **kwargs):
        self.model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad", model="silero_vad", force_reload=False, onnx=False,
        )

        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            self.VADIterator,
            self.collect_chunks,
        ) = utils

        self.sampling_rate = sampling_rate = 16000
        self.collar = 1.0

    async def detect_activity(self, client):
        frames = np.frombuffer(client.scratch_buffer, dtype=np.int16)

        # normalization see https://discuss.pytorch.org/t/torchaudio-load-normalization-question/71470
        frames = frames / (1 << 15)

        audio = torch.tensor(frames.astype(np.float32))
        vad_results = self.get_speech_timestamps(
            audio, self.model, sampling_rate=self.sampling_rate, threshold = 0.5,
            min_speech_duration_ms = 250, max_speech_duration_s = float('inf'), min_silence_duration_ms = 500, speech_pad_ms = 30
        )
  
        vad_segments = []
        if len(vad_results) > 0:
            vad_segments = [
                {"start": segment["start"] / 1000 , "end": segment["end"] / 1000, "confidence": 1.0}
                for segment in vad_results
            ]
        return vad_segments
