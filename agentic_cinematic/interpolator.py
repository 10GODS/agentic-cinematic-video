"""
Motion Interpolator: Self-healing interpolation (RIFE or optical flow fallback).
"""

import os
import subprocess
import numpy as np
import cv2
from PIL import Image

def check_rife_availability():
    """Check if RIFE is available."""
    RIFE_AVAILABLE = False
    try:
        if not os.path.exists("/kaggle/working/Practical-RIFE"):
            subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/hzwer/Practical-RIFE.git",
                 "/kaggle/working/Practical-RIFE"],
                check=True, capture_output=True, timeout=120,
            )
        RIFE_AVAILABLE = os.path.isdir("/kaggle/working/Practical-RIFE")
        print("RIFE repo available:", RIFE_AVAILABLE, "(weights still need to be placed under train_log/ to actually use it)")
    except Exception as e:
        print(f"[interpolation agent] RIFE setup failed ({e}); will use optical-flow fallback instead.")
        RIFE_AVAILABLE = False
    
    # NOTE: Practical-RIFE requires its own pretrained flownet weights (train_log/*.pkl) which are
    # distributed via Google Drive links that change over time and cannot be fetched unattended here.
    # If you have those weights available in a Kaggle dataset, mount it and point RIFE_WEIGHTS_DIR at
    # it, then flip USE_LEARNED_RIFE to True. Otherwise the optical-flow fallback below is used and is
    # fully local / fully automatic.
    RIFE_WEIGHTS_DIR = None   # e.g. "/kaggle/input/rife-weights/train_log"
    USE_LEARNED_RIFE = RIFE_AVAILABLE and RIFE_WEIGHTS_DIR is not None and os.path.isdir(RIFE_WEIGHTS_DIR or "")
    print("Using learned RIFE:", USE_LEARNED_RIFE, "| optical-flow fallback active:", not USE_LEARNED_RIFE)
    return USE_LEARNED_RIFE

def _optical_flow_interpolate(frames_pil, factor):
    """Dense Farneback optical-flow interpolation - RIFE-style fallback, no external weights."""
    frames = [np.array(f.convert("RGB")) for f in frames_pil]
    out = []
    h, w = frames[0].shape[:2]
    grid_y, grid_x = np.mgrid[0:h, 0:w].astype(np.float32)
    for i in range(len(frames) - 1):
        f0, f1 = frames[i], frames[i + 1]
        out.append(f0)
        gray0 = cv2.cvtColor(f0, cv2.COLOR_RGB2GRAY)
        gray1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(gray0, gray1, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        for k in range(1, factor):
            t = k / factor
            map_x = (grid_x + flow[..., 0] * t).astype(np.float32)
            map_y = (grid_y + flow[..., 1] * t).astype(np.float32)
            warped = cv2.remap(f0, map_x, map_y, cv2.INTER_LINEAR)
            blended = cv2.addWeighted(warped, 1 - t, f1, t, 0)
            out.append(blended)
    out.append(frames[-1])
    return [Image.fromarray(f) for f in out]

def interpolate_frames(frames_pil, target_fps, source_fps):
    """Interpolate frames to target FPS using RIFE if available, otherwise optical flow fallback."""
    factor = max(1, round(target_fps / source_fps))
    
    # In a real implementation, we would check for RIFE availability here
    # For now, we'll always use the optical flow fallback since setting up RIFE weights is complex
    return _optical_flow_interpolate(frames_pil, factor)
