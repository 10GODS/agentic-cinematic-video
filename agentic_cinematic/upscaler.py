"""
Upscaler: Real-ESRGAN for super-resolution upscaling.
"""

import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import cv2
import numpy as np
from PIL import Image

def load_upsampler(device="cuda"):
    """Load the Real-ESRGAN upsampler."""
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    weights_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    return RealESRGANer(
        scale=4, model_path=weights_url, model=model,
        tile=400, tile_pad=10, pre_pad=0, half=True, device=device,
    )

def upscale_frames(frames_pil, upsampler, outscale):
    """Upscale frames using Real-ESRGAN."""
    out = []
    for f in frames_pil:
        bgr = cv2.cvtColor(np.array(f), cv2.COLOR_RGB2BGR)
        enhanced, _ = upsampler.enhance(bgr, outscale=outscale)
        out.append(Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)))
    return out
