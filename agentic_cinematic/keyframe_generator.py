"""
Keyframe Generator: SDXL image generation with agentic retry.
"""

import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import os

def load_sdxl(device="cuda", dtype=torch.float16):
    """Load the SDXL pipeline."""
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=dtype, variant="fp16", use_safetensors=True,
    ).to(device)
    pipe.enable_vae_slicing()
    pipe.enable_attention_slicing()
    return pipe

NEGATIVE_PROMPT = "blurry, low quality, deformed, watermark, text, extra limbs, bad anatomy, cropped, worst quality"

def generate_keyframe_for_scene(scene, sdxl_pipe, config, retry=0, clip_model=None, clip_processor=None, device="cuda"):
    """Generate a keyframe for a scene with agentic retry based on CLIP scoring."""
    prompt = f"{scene['image_prompt']}, {config['style']}"
    image = sdxl_pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE_PROMPT,
        width=config["image_size"][0],
        height=config["image_size"][1],
        num_inference_steps=config["sdxl_steps"],
        guidance_scale=config["sdxl_guidance"],
    ).images[0]

    # Score the generated image
    if clip_model is not None and clip_processor is not None:
        from .critic import clip_score
        score = clip_score(image, scene["image_prompt"], clip_model, clip_processor, device)
    else:
        score = 1.0  # If no critic available, assume good score

    print(f"  scene {scene['scene_id']} attempt {retry + 1}: CLIP alignment = {score:.3f}")

    if score < config["clip_quality_threshold"] and retry < config["max_retries_per_scene"]:
        print(f"  -> below threshold ({config['clip_quality_threshold']}), agent is retrying with a strengthened prompt")
        scene = {**scene, "image_prompt": scene["image_prompt"] + ", highly detailed, sharp focus, masterpiece"}
        return generate_keyframe_for_scene(scene, sdxl_pipe, config, retry + 1, clip_model, clip_processor, device)

    return image, score
