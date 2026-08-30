"""
Video Generator: Stable Video Diffusion XT for image-to-video conversion with cinematic motion adaptation.
Adapts motion based on shot type from director for more natural pre-visualization.
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

def image_to_clip_frames(image, svd_pipe, config, scene=None):
    """Convert an image to video frames using SVD-XT with motion adaptation based on shot type."""
    image = image.resize(config["image_size"])
    
    # Base motion bucket
    motion_bucket_id = 127  # SVD-XT default
    
    # Adapt motion based on shot type from director agent
    if scene and "camera" in scene:
        camera_desc = scene["camera"].lower()
        if "close-up" in camera_desc or "extreme close-up" in camera_desc:
            motion_bucket_id = 80   # Subtle motion for intimate shots
        elif "wide shot" in camera_desc or "extreme wide shot" in camera_desc:
            motion_bucket_id = 180  # More motion for establishing shots
        elif "pan" in camera_desc:
            motion_bucket_id = 150  # Moderate motion for pans
        elif "tilt" in camera_desc:
            motion_bucket_id = 140  # Slight tilt motion
    
    with torch.no_grad():
        frames = svd_pipe(
            image,
            num_frames=config["video_frames_per_scene"],
            decode_chunk_size=4,
            motion_bucket_id=motion_bucket_id,
            noise_aug_strength=0.02,
        ).frames[0]
    return frames  # list[PIL.Image]
