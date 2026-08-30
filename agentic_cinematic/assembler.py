"""
Assembler: Combine video clips with crossfades into final video.
"""

from moviepy.editor import ImageSequenceClip, concatenate_videoclips, VideoFileClip
import os

def frames_to_mp4(frames_pil, fps, out_path):
    """Convert frames to MP4 video."""
    import numpy as np
    arrays = [np.array(f) for f in frames_pil]
    clip = ImageSequenceClip(arrays, fps=fps)
    clip.write_videofile(out_path, codec="libx264", audio=False, logger=None)
    clip.close()
    return out_path

def assemble_final_video(scene_clip_paths, final_path, crossfade):
    """Assemble final video with crossfades between scenes."""
    clips = [VideoFileClip(p) for p in scene_clip_paths]
    faded = [clips[0]] + [c.crossfadein(crossfade) for c in clips[1:]]
    final = concatenate_videoclips(faded, method="compose", padding=-crossfade)
    final.write_videofile(final_path, codec="libx264", audio=False, logger=None)
    final.close()
    for c in clips:
        c.close()
    return final_path
