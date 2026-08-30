"""
Configuration for Agentic Cinematic Video Generation - Summer Blockbuster Hackathon Edition
Solves: Automated Concept Visualization for Film Pre-Production
Uses: Google Cloud Storage (asset management) + Grafana Labs (observability)
"""

import os

# Google Gemini API Configuration (Director Agent - Gemini Enterprise)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

# Google Cloud Configuration
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "agentic-cinematic-hackathon")
GCS_PROJECT_ID = os.environ.get("GCS_PROJECT_ID", None)  # Will use default if not set

# Grafana Configuration (for partner tech use)
GRAFANA_ENABLED = os.environ.get("GRAFANA_ENABLED", "false").lower() == "true"
GRAFANA_URL = os.environ.get("GRAFANA_URL", "https://metrics.grafana.com/api/prometheus/push")
GRAFANA_USER = os.environ.get("GRAFANA_USER", "")  # Set via Kaggle secrets
GRAFANA_KEY = os.environ.get("GRAFANA_KEY", "")    # Set via Kaggle secrets

CONFIG = {
    # Core premise - can be overridden
    "premise": "A lone astronaut discovers an ancient temple on a moon of Saturn, guarded by a spectral tiger made of starlight.",
    "num_scenes": 6,
    "style": "cinematic, hyperrealistic, dramatic volumetric lighting, anamorphic lens flare, 35mm film grain, epic scale, award-winning cinematography",

    # Image generation (SDXL)
    "image_size": (1024, 576),          # 16:9, SDXL-native
    "sdxl_steps": 35,                   # Increased for quality
    "sdxl_guidance": 7.5,               # Slightly higher guidance

    # Video generation (SVD-XT)
    "video_frames_per_scene": 20,       # Reduced to save VRAM for interpolation
    "video_fps": 7,                     # SVD-XT native output fps
    "target_fps_after_interp": 24,      # Cinematic frame rate

    # Upscaling (Real-ESRGAN)
    "upscale_factor": 2,                # 2x upscale to 2048x1152

    # Agentic behavior thresholds
    "clip_quality_threshold": 0.24,     # Slightly lower to reduce retry time
    "max_retries_per_scene": 1,         # Limited retries for T4 efficiency

    # Assembly
    "crossfade_seconds": 0.4,

    # Quality enhancement flags
    "apply_film_lut": True,
    "apply_motion_blur": True,
    "motion_blur_strength": 0.25,

    # Adaptive quality allocation (more effort on important scenes)
    "scene_importance_weights": {
        1: 1.0,   # Establishing shot
        2: 1.2,   # Inciting moment
        3: 1.1,   # Rising tension
        4: 1.3,   # Confrontation
        5: 1.5,   # Climax (most important)
        6: 1.0,   # Resolution
        7: 0.9,   # Aftermath
        8: 0.8    # Final image
    }
}
