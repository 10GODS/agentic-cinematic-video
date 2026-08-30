"""
Orchestrator: Main pipeline that runs the agentic cinematic video generation.
"""

import os
import gc
import json
import time
from datetime import datetime
import torch

from .config import CONFIG
from .director import load_planner, plan_scenes
from .critic import load_critic, clip_score
from .keyframe_generator import load_sdxl, generate_keyframe_for_scene
from .video_generator import load_svd, image_to_clip_frames
from .interpolator import interpolate_frames
from .upscaler import load_upsampler, upscale_frames
from .assembler import frames_to_mp4, assemble_final_video

def free_mem():
    """Free GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

def run_pipeline(config=None):
    """Run the full agentic cinematic video generation pipeline."""
    if config is None:
        from .config import CONFIG
        config = CONFIG
    
    manifest = {"started": datetime.utcnow().isoformat(), "config": {**config}, "scenes": []}
    t0 = time.time()

    OUTPUT_DIR = "./agentic_cinematic_output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Stage 0: Planning scenes with local director agent ===")
    tok, planner = load_planner()
    scenes = plan_scenes(config["premise"], config["num_scenes"], config["style"], tok, planner)
    del planner, tok
    free_mem()
    for s in scenes:
        print(f"  scene {s['scene_id']}: {s['description']}")

    print("\n=== Stage 1: Keyframe generation (SDXL) ===")
    sdxl = load_sdxl()
    clip_model, clip_processor = load_critic()
    keyframes = []
    for scene in scenes:
        img, score = generate_keyframe_for_scene(
            scene, sdxl, config, 
            clip_model=clip_model, clip_processor=clip_processor
        )
        img.save(f"{OUTPUT_DIR}/scene_{scene['scene_id']:02d}_keyframe.png")
        keyframes.append(img)
        manifest["scenes"].append({
            "scene_id": scene["scene_id"],
            "final_prompt": scene["image_prompt"],
            "clip_score": score,
        })
    del sdxl, clip_model, clip_processor
    free_mem()

    print("\n=== Stage 2: Image-to-video (SVD-XT) ===")
    svd = load_svd()
    all_scene_frames = []
    for scene, img in zip(scenes, keyframes):
        print(f"  animating scene {scene['scene_id']} ...")
        frames = image_to_clip_frames(img, svd, config)
        all_scene_frames.append(frames)
    del svd
    free_mem()

    print("\n=== Stage 3: Motion interpolation ===")
    interp_scene_frames = [
        interpolate_frames(frames, config["target_fps_after_interp"], config["video_fps"])
        for frames in all_scene_frames
    ]

    print("\n=== Stage 4: Super-resolution upscaling (Real-ESRGAN) ===")
    upsampler = load_upsampler()
    final_clip_paths = []
    for scene, frames in zip(scenes, interp_scene_frames):
        print(f"  upscaling scene {scene['scene_id']} ...")
        up_frames = upscale_frames(frames, upsampler, config["upscale_factor"])
        path = f"{OUTPUT_DIR}/scene_{scene['scene_id']:02d}_final.mp4"
        frames_to_mp4(up_frames, config["target_fps_after_interp"], path)
        final_clip_paths.append(path)
    del upsampler
    free_mem()

    print("\n=== Stage 5: Final assembly ===")
    final_path = f"{OUTPUT_DIR}/final_cinematic_video.mp4"
    assemble_final_video(final_clip_paths, final_path, config["crossfade_seconds"])

    manifest["finished"] = datetime.utcnow().isoformat()
    manifest["elapsed_seconds"] = round(time.time() - t0, 1)
    manifest["final_video"] = final_path
    with open(f"{OUTPUT_DIR}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone in {manifest['elapsed_seconds']}s. Final video: {final_path}")
    return final_path

if __name__ == "__main__":
    run_pipeline()
