"""
Video Generator: Stable Video Diffusion XT for image-to-video conversion.
"""

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video
from PIL import Image
import numpy as np

def load_svd(device="cuda", dtype=torch.float16):
    """Load the Stable Video Diffusion XT pipeline."""
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=dtype, variant="fp16",
    )
    pipe.enable_model_cpu_offload()
    return pipe

def image_to_clip_frames(image, svd_pipe, config):
    """Convert an image to video frames using SVD-XT."""
    image = image.resize(config["image_size"])
    with torch.no_grad():
        frames = svd_pipe(
            image,
            num_frames=config["video_frames_per_scene"],
            decode_chunk_size=4,
            motion_bucket_id=127,
            noise_aug_strength=0.02,
        ).frames[0]
    return frames  # list[PIL.Image]
