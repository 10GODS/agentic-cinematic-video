"""
Configuration for the Agentic Cinematic Video Generation pipeline.
"""

CONFIG = {
    "premise": "A lone astronaut discovers an ancient temple on a moon of Saturn, guarded by a spectral tiger made of starlight.",
    "num_scenes": 6,
    "style": "cinematic, hyperrealistic, dramatic volumetric lighting, anamorphic lens flare, 35mm film grain, epic scale, award-winning cinematography",

    "image_size": (1024, 576),          # 16:9, SDXL-native
    "sdxl_steps": 30,
    "sdxl_guidance": 7.0,

    "video_frames_per_scene": 25,       # SVD-XT default window
    "video_fps": 7,                     # SVD-XT native output fps
    "target_fps_after_interp": 24,      # cinematic frame rate after RIFE/optical-flow interpolation

    "upscale_factor": 2,                # Real-ESRGAN output scale

    "clip_quality_threshold": 0.26,     # min CLIP image-text alignment before we accept a keyframe
    "max_retries_per_scene": 2,         # agentic self-correction budget per scene

    "crossfade_seconds": 0.4,
}
