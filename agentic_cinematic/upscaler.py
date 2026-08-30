"""
Upscaler: Real-ESRGAN for super-resolution upscaling with T4-optimized settings.
Reduces tile artifacts while maintaining quality for cinematic output.
"""

import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import cv2
import numpy as np
from PIL import Image

def load_upsampler(device="cuda"):
    """Load the Real-ESRGAN upsampler with T4-optimized tile settings."""
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    weights_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    return RealESRGANer(
        scale=4, model_path=weights_url, model=model,
        tile=180,           # Reduced from 400 for better T4 fit
        tile_pad=15,        # Padding to reduce tile artifacts
        pre_pad=10,
        half=True, 
        device=device,
    )

def upscale_frames(frames_pil, upsampler, outscale):
    """Upscale frames using Real-ESRGAN with optional enhancement."""
    out = []
    for f in frames_pil:
        bgr = cv2.cvtColor(np.array(f), cv2.COLOR_RGB2BGR)
        enhanced, _ = upsampler.enhance(bgr, outscale=outscale)
        out.append(Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)))
    return out
