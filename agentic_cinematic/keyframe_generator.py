"""
Keyframe Generator: SDXL image generation with agentic retry and cinematic enhancements.
Improves visual quality for film pre-production use case.
"""

import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import os

def load_sdxl(device="cuda", dtype=torch.float16):
    """Load the SDXL pipeline with quality optimizations."""
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "RunDiffusion/Juggernaut-XL-v9",
        torch_dtype=dtype, variant="fp16", use_safetensors=True,
    ).to(device)
    pipe.enable_vae_slicing()
    pipe.enable_attention_slicing()
    
    # Use DPM++ 2M Karras scheduler for better quality if available
    try:
        from diffusers import DPMSolverMultistepScheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    except ImportError:
        pass  # Keep default scheduler
    
    return pipe

NEGATIVE_PROMPT = "blurry, low quality, deformed, watermark, text, extra limbs, bad anatomy, cropped, worst quality, oversaturated, blurry background, cartoon, 3d render"

def generate_keyframe_for_scene(scene, sdxl_pipe, config, retry=0, clip_model=None, clip_processor=None, device="cuda"):
    """Generate a keyframe for a scene with agentic retry based on CLIP scoring and cinematic enhancements."""
    # Build prompt with cinematic elements from director
    prompt = f"{scene['image_prompt']}, {config['style']}, film grain, cinematic lighting"
    
    # Add negative prompt enhancements
    negative_prompt = NEGATIVE_PROMPT
    
    # Calculate adaptive steps based on scene importance (more effort on key scenes)
    base_steps = config["sdxl_steps"]
    importance_weight = scene.get("importance", 1.0)
    adaptive_steps = min(int(base_steps * importance_weight), 45)  # Cap at 45 for T4
    
    # Slightly higher guidance for important scenes
    guidance_scale = config["sdxl_guidance"] * (1.0 + (importance_weight - 1.0) * 0.2)
    
    image = sdxl_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=config["image_size"][0],
        height=config["image_size"][1],
        num_inference_steps=adaptive_steps,
        guidance_scale=guidance_scale,
    ).images[0]

    # Score the generated image using CLIP critic
    if clip_model is not None and clip_processor is not None:
        from .critic import clip_score
        score = clip_score(image, scene["image_prompt"], clip_model, clip_processor, device)
    else:
        score = 1.0  # If no critic available, assume good score

    print(f"  scene {scene['scene_id']} attempt {retry + 1}: CLIP alignment = {score:.3f} (adaptive steps: {adaptive_steps})")

    # Agentic retry logic - only retry if score is below threshold and we have retries left
    if score < config["clip_quality_threshold"] and retry < config["max_retries_per_scene"]:
        print(f"  -> below threshold ({config['clip_quality_threshold']}), agent is retrying with strengthened prompt")
        # Strengthen prompt for retry
        strengthened_prompt = scene["image_prompt"] + ", highly detailed, sharp focus, masterpiece, 8k resolution"
        scene_retry = {**scene, "image_prompt": strengthened_prompt}
        return generate_keyframe_for_scene(scene_retry, sdxl_pipe, config, retry + 1, clip_model, clip_processor, device)

    return image, score
