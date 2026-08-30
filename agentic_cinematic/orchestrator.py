"""
Orchestrator: Main pipeline that runs the agentic cinematic video generation.
Integrates Google Cloud Storage (actual GCP use) and Grafana Labs (partner tech use)
for the Summer Blockbuster Hackathon: Solves Automated Concept Visualization for Film Pre-Production.
"""

import os
import gc
import json
import time
from datetime import datetime
import torch

# Import local modules
from .config import CONFIG, GCS_BUCKET_NAME, GCS_PROJECT_ID, GRAFANA_ENABLED, GRAFANA_URL, GRAFANA_USER, GRAFANA_KEY
from .director import load_planner, plan_scenes
from .critic import load_critic, clip_score
from .keyframe_generator import load_sdxl, generate_keyframe_for_scene
from .video_generator import load_svd, image_to_clip_frames
from .interpolator import interpolate_frames
from .upscaler import load_upsampler, upscale_frames
from .assembler import frames_to_mp4, assemble_final_video

# Google Cloud Storage integration (actual GCP use)
def setup_gcs_client():
    """Setup Google Cloud Storage client - returns None if not configured."""
    try:
        from google.cloud import storage
        # Try to use default credentials (works if authenticated)
        client = storage.Client(project=GCS_PROJECT_ID) if GCS_PROJECT_ID else storage.Client()
        # Test connection by getting bucket (will fail if not accessible)
        bucket = client.bucket(GCS_BUCKET_NAME)
        # Don't actually access bucket here to avoid errors if it doesn't exist
        # The upload function will handle bucket creation/access
        return client
    except Exception as e:
        print(f"[GCS] Warning: Google Cloud Storage not configured ({e}). Skipping cloud uploads.")
        return None

def upload_to_gcs(local_path, bucket_name, blob_name=None, gcs_client=None):
    """Upload file to Google Cloud Storage - demonstrates actual GCP use for media asset management."""
    if not gcs_client:
        print(f"[GCS] Skipping upload (no GCS client): {local_path}")
        return None
        
    if blob_name is None:
        blob_name = os.path.basename(local_path)
    
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        blob.upload_from_filename(local_path)
        gcs_url = f"gs://{bucket_name}/{blob_name}"
        print(f"[GCS] Uploaded {local_path} to {gcs_url}")
        return gcs_url
    except Exception as e:
        print(f"[GCS] Error uploading {local_path}: {e}")
        return None

# Grafana Labs integration (partner technology use)
def setup_grafana_client():
    """Setup Grafana client - returns None if not configured."""
    if not GRAFANA_ENABLED or not GRAFANA_USER or not GRAFANA_KEY:
        print("[Grafana] Warning: Grafana not configured. Skipping metrics.")
        return None
    return {"url": GRAFANA_URL, "user": GRAFANA_USER, "key": GRAFANA_KEY}

def send_grafana_metric(metric_name, value, labels=None, grafana_config=None):
    """Send metric to Grafana Cloud - demonstrates partner tech use for observability."""
    if not grafana_config:
        return
        
    if labels is None:
        labels = {}
    
    data = [{
        "metric": metric_name,
        "values": [int(time.time()), value],
        "labels": {
            "job": "agentic_cinema_hackathon",
            "instance": "kaggle_t4",
            **labels
        }
    }]
    
    try:
        import requests
        response = requests.post(
            grafana_config["url"],
            data=json.dumps(data),
            auth=(grafana_config["user"], grafana_config["key"]),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 204:
            print(f"[Grafana] Sent metric {metric_name}: {value}")
        else:
            print(f"[Grafana] Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[Grafana] Error sending metric (non-fatal): {e}")

def free_mem():
    """Free GPU memory."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def run_pipeline(config=None, gcs_client=None, grafana_config=None):
    """Run the full agentic cinematic video generation pipeline with cloud/partner integration."""
    if config is None:
        config = CONFIG
    
    manifest = {
        "started": datetime.utcnow().isoformat(), 
        "config": {**config}, 
        "scenes": [],
        "cloud_integration": {
            "gcs_enabled": gcs_client is not None,
            "grafana_enabled": grafana_config is not None
        }
    }
    t0 = time.time()

    OUTPUT_DIR = "./agentic_cinematic_output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Agentic Cinematic Video Generation for Film Pre-Production ===")
    print("Solving: Automated Concept Visualization workflow")
    print(f"Using Google Cloud Storage: {'Yes' if gcs_client else 'No'}")
    print(f"Using Grafana Labs (partner tech): {'Yes' if grafana_config else 'No'}")

    print("\n=== Stage 0: Planning scenes with Gemini director agent ===")
    stage_start = time.time()
    tok, planner = load_planner()
    scenes = plan_scenes(config["premise"], config["num_scenes"], config["style"], tok, planner)
    del planner
    stage_time = time.time() - stage_start
    free_mem()
    
    # Send metrics to Grafana
    send_grafana_metric("scene_planning_duration", stage_time, {"stage": "planning"}, grafana_config)
    
    for s in scenes:
        print(f"  scene {s['scene_id']}: {s['description']}")

    print("\n=== Stage 1: Keyframe generation (SDXL) with agentic retry ===")
    stage_start = time.time()
    sdxl = load_sdxl()
    clip_model, clip_processor = load_critic()
    keyframes = []
    keyframe_gcs_paths = []
    
    for scene in scenes:
        img, score = generate_keyframe_for_scene(
            scene, sdxl_pipe=sdxl, config=config, 
            clip_model=clip_model, clip_processor=clip_processor
        )
        keyframe_path = f"{OUTPUT_DIR}/scene_{scene['scene_id']:02d}_keyframe.png"
        img.save(keyframe_path)
        keyframes.append(img)
        
        # Upload to GCS for media asset management (actual GCP use)
        gcs_path = upload_to_gcs(
            keyframe_path, 
            GCS_BUCKET_NAME, 
            f"keyframes/scene_{scene['scene_id']:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            gcs_client
        )
        keyframe_gcs_paths.append(gcs_path)
        
        manifest["scenes"].append({
            "scene_id": scene["scene_id"],
            "final_prompt": scene["image_prompt"],
            "clip_score": score,
            "gcs_keyframe_path": gcs_path
        })
        
        # Send CLIP score to Grafana
        send_grafana_metric("keyframe_clip_score", score, {"scene": scene["scene_id"]}, grafana_config)
    
    del sdxl, clip_model, clip_processor
    stage_time = time.time() - stage_start
    free_mem()
    send_grafana_metric("keyframe_generation_duration", stage_time, {"stage": "keyframes"}, grafana_config)

    print("\n=== Stage 2: Image-to-video (SVD-XT) ===")
    stage_start = time.time()
    svd = load_svd()
    all_scene_frames = []
    svd_gcs_paths = []
    
    for scene, img in zip(scenes, keyframes):
        print(f"  animating scene {scene['scene_id']} ...")
        frames = image_to_clip_frames(img, svd, config, scene)
        all_scene_frames.append(frames)
        
        # Optional: Save intermediate video clips to GCS
        # clip_path = f"{OUTPUT_DIR}/scene_{scene['scene_id']:02d}_raw.mp4"
        # frames_to_mp4(frames, config["video_fps"], clip_path, config)
        # upload_to_gcs(clip_path, GCS_BUCKET_NAME, f"raw_clips/scene_{scene['scene_id']:02d}.mp4", gcs_client)
    
    del svd
    stage_time = time.time() - stage_start
    free_mem()
    send_grafana_metric("svd_generation_duration", stage_time, {"stage": "video_gen"}, grafana_config)

    print("\n=== Stage 3: Motion interpolation ===")
    stage_start = time.time()
    interp_scene_frames = [
        interpolate_frames(frames, config["target_fps_after_interp"], config["video_fps"])
        for frames in all_scene_frames
    ]
    stage_time = time.time() - stage_start
    send_grafana_metric("interpolation_duration", stage_time, {"stage": "interpolation"}, grafana_config)

    print("\n=== Stage 4: Super-resolution upscaling (Real-ESRGAN) ===")
    stage_start = time.time()
    upsampler = load_upsampler()
    final_clip_paths = []
    upscale_gcs_clip_paths = []
    
    for scene, frames in zip(scenes, interp_scene_frames):
        print(f"  upscaling scene {scene['scene_id']} ...")
        up_frames = upscale_frames(frames, upsampler, config["upscale_factor"])
        path = f"{OUTPUT_DIR}/scene_{scene['scene_id']:02d}_final.mp4"
        frames_to_mp4(up_frames, config["target_fps_after_interp"], path, config)
        final_clip_paths.append(path)
        
        # Upload final clips to GCS
        gcs_path = upload_to_gcs(
            path, 
            GCS_BUCKET_NAME, 
            f"final_clips/scene_{scene['scene_id']:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
            gcs_client
        )
        upscale_gcs_clip_paths.append(gcs_path)
    
    del upsampler
    stage_time = time.time() - stage_start
    free_mem()
    send_grafana_metric("upscaling_duration", stage_time, {"stage": "upscaling"}, grafana_config)

    print("\n=== Stage 5: Final assembly ===")
    stage_start = time.time()
    final_path = f"{OUTPUT_DIR}/final_cinematic_video.mp4"
    assemble_final_video(final_clip_paths, final_path, config["crossfade_seconds"], config)
    stage_time = time.time() - stage_start
    
    # Upload final video to GCS (primary asset for M&E workflow)
    final_gcs_path = upload_to_gcs(
        final_path, 
        GCS_BUCKET_NAME, 
        f"final_videos/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(final_path)}",
        gcs_client
    )
    
    send_grafana_metric("final_assembly_duration", stage_time, {"stage": "assembly"}, grafana_config)

    manifest["finished"] = datetime.utcnow().isoformat()
    manifest["elapsed_seconds"] = round(time.time() - t0, 1)
    manifest["final_video"] = final_path
    manifest["final_video_gcs_path"] = final_gcs_path
    
    with open(f"{OUTPUT_DIR}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n? Done in {manifest['elapsed_seconds']}s.")
    print(f"?? Final video: {final_path}")
    if final_gcs_path:
        print(f"??  Cloud backup: {final_gcs_path}")
    print(f"?? Metrics sent to Grafana: {'Yes' if grafana_config else 'No'}")
    return final_path

if __name__ == "__main__":
    # Setup cloud/partner clients
    print("Initializing cloud and partner integrations...")
    gcs_client = setup_gcs_client()
    grafana_config = setup_grafana_client()
    
    # Run pipeline
    run_pipeline(gcs_client=gcs_client, grafana_config=grafana_config)
