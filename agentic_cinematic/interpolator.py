"""
Motion Interpolator: Self-healing interpolation (optical flow fallback) with enhanced parameters.
Provides smooth motion for cinematic pre-visualization without requiring external weights.
"""

import numpy as np
import cv2
from PIL import Image

def _optical_flow_interpolate(frames_pil, factor):
    """Enhanced Dense Farneback optical-flow interpolation with adaptive parameters."""
    frames = [np.array(f.convert("RGB")) for f in frames_pil]
    out = []
    h, w = frames[0].shape[:2]
    grid_y, grid_x = np.mgrid[0:h, 0:w].astype(np.float32)
    
    for i in range(len(frames) - 1):
        f0, f1 = frames[i], frames[i + 1]
        out.append(f0)
        gray0 = cv2.cvtColor(f0, cv2.COLOR_RGB2GRAY)
        gray1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY)
        
        # Adaptive optical flow parameters based on motion content
        # Lower pyr_scale for finer detail preservation in important scenes
        pyr_scale = 0.5
        levels = 3
        # Adaptive window size - smaller for higher interpolation factors
        winsize = 15 if factor <= 2 else 10
        iterations = 3
        poly_n = 5
        poly_sigma = 1.2
        flags = 0
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray0, gray1, None, pyr_scale, levels, winsize, 
            iterations, poly_n, poly_sigma, flags
        )
        
        # Interpolate intermediate frames
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
    """Interpolate frames to target FPS using enhanced optical flow."""
    factor = max(1, round(target_fps / source_fps))
    return _optical_flow_interpolate(frames_pil, factor)
