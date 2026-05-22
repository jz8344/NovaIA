import struct
import base64
from loguru import logger

ASTERISK_RATE = 8000
ASTERISK_SAMPLE_WIDTH = 2   # 16-bit
ASTERISK_CHANNELS = 1

GEMINI_INPUT_RATE = 16000
GEMINI_OUTPUT_RATE = 24000


def resample_linear(data: bytes, from_rate: int, to_rate: int) -> bytes:
    if from_rate == to_rate:
        return data

    # Optimización por decimación rápida para tasas proporcionales (elimina el bucle for en CPU)
    if from_rate == 24000 and to_rate == 8000:
        samples_in = struct.unpack(f"<{len(data) // 2}h", data)
        samples_out = samples_in[::3]
        return struct.pack(f"<{len(samples_out)}h", *samples_out)

    if from_rate == 24000 and to_rate == 16000:
        samples_in = struct.unpack(f"<{len(data) // 2}h", data)
        samples_out = [samples_in[i] for i in range(len(samples_in)) if i % 3 != 2]
        return struct.pack(f"<{len(samples_out)}h", *samples_out)

    # Fallback algoritmo lineal para otras tasas
    samples_in = struct.unpack(f"<{len(data) // 2}h", data)
    ratio = to_rate / from_rate
    n_out = int(len(samples_in) * ratio)
    samples_out = []

    for i in range(n_out):
        src_idx = i / ratio
        idx = int(src_idx)
        frac = src_idx - idx

        if idx + 1 < len(samples_in):
            sample = int(samples_in[idx] * (1 - frac) + samples_in[idx + 1] * frac)
        else:
            sample = samples_in[min(idx, len(samples_in) - 1)]

        sample = max(-32768, min(32767, sample))
        samples_out.append(sample)

    return struct.pack(f"<{len(samples_out)}h", *samples_out)


class AudioProcessor:

    @staticmethod
    def asterisk_to_gemini(pcm_8khz: bytes) -> bytes:
        return resample_linear(pcm_8khz, ASTERISK_RATE, GEMINI_INPUT_RATE)

    @staticmethod
    def gemini_to_asterisk(pcm_24khz: bytes) -> bytes:
        return resample_linear(pcm_24khz, GEMINI_OUTPUT_RATE, ASTERISK_RATE)

    @staticmethod
    def pcm_to_base64(pcm_data: bytes) -> str:
        return base64.b64encode(pcm_data).decode("utf-8")

    @staticmethod
    def base64_to_pcm(b64_data: str) -> bytes:
        return base64.b64decode(b64_data)

    @staticmethod
    def browser_to_gemini(pcm_16khz: bytes) -> bytes:
        return pcm_16khz

    @staticmethod
    def gemini_to_browser(pcm_24khz: bytes) -> bytes:
        return resample_linear(pcm_24khz, GEMINI_OUTPUT_RATE, GEMINI_INPUT_RATE)
