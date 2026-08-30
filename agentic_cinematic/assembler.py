"""
Assembler: Combine video clips with crossfades into final video with cinematic enhancements.
Adds film LUT color grading, motion blur, and high-quality encoding for professional pre-vis output.
"""

from moviepy.editor import ImageSequenceClip, concatenate_videoclips, VideoFileClip
import os
import numpy as np
import cv2
from PIL import Image

def apply_film_lut(frame_pil):
    """Apply subtle filmic color grading (teal-and-orange) for cinematic look."""
    frame = np.array(frame_pil).astype(np.float32) / 255.0
    
    # Teal-and-orange lift/gamma/gain (cinematic look)
    lift = np.array([0.90, 0.93, 1.00])   # Slightly lift shadows toward teal
    gamma = np.array([1.00, 0.95, 1.05])  # Adjust midtones
    gain = np.array([1.05, 1.00, 0.92])   # Slightly gain highlights toward orange
    
    # Apply lift/gamma/gain
    frame = np.power(np.clip(frame, 0, 1), gamma) 
    frame = frame * gain + lift
    frame = np.clip(frame, 0, 1)
    
    # Add subtle film grain
    grain_strength = 0.015
    grain = np.random.normal(0, grain_strength, frame.shape)
    frame = np.clip(frame + grain, 0, 1)
    
    return (frame * 255).astype(np.uint8)

def add_motion_blur(frames_pil, strength=0.25):
    """Add subtle motion blur to make CGI feel more cinematic and less "crisp"."""
    if len(frames_pil) < 2:
        return frames_pil
    
    blurred = [frames_pil[0]]
    for i in range(1, len(frames_pil)):
        prev = np.array(frames_pil[i-1])
        curr = np.array(frames_pil[i])
        # Simple frame blending for motion blur
        blended = cv2.addWeighted(prev, 1-strength, curr, strength, 0)
        blurred.append(Image.fromarray(blended))
    blurred.append(frames_pil[-1])
    return blurred

def frames_to_mp4(frames_pil, fps, out_path, config=None):
    """Convert frames to MP4 video with optional cinematic enhancements."""
    arrays = [np.array(f) for f in frames_pil]
    
    # Apply cinematic enhancements if enabled
    if config and config.get("apply_film_lut", False):
        arrays = [apply_film_lut(Image.fromarray(arr)) for arr in arrays]
    
    if config and config.get("apply_motion_blur", False):
        strength = config.get("motion_blur_strength", 0.25)
        pil_frames = [Image.fromarray(arr) for arr in arrays]
        pil_frames = add_motion_blur(pil_frames, strength)
        arrays = [np.array(f) for f in pil_frames]
    
    clip = ImageSequenceClip(arrays, fps=fps)
    # High quality encoding for professional output
    clip.write_videofile(
        out_path, 
        codec="libx264", 
        audio=False, 
        logger=None,
        preset="medium",
        ffmpeg_params=["-crf", "18"]  # Visually lossless quality
    )
    clip.close()
    return out_path

def assemble_final_video(scene_clip_paths, final_path, crossfade, config=None, audio_path=None):
    """Assemble final video with crossfades between scenes and optional enhancements."""
    clips = [VideoFileClip(p) for p in scene_clip_paths]
    
    # Apply vignette to each clip for cinematic feel (subtle)
    def add_vignette(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        # Create vignette mask
        x = np.linspace(-1, 1, w)
        y = np.linspace(-1, 1, h)
        xv, yv = np.meshgrid(x, y)
        d = np.sqrt(xv**2 + yv**2)
        mask = np.clip(1 - d*1.2, 0, 1)**0.5
        vignette = np.dstack([mask]*3)
        return (frame * vignette).astype(np.uint8)
    
    # Apply vignette if we want it (can be disabled)
    if config and config.get("apply_vignette", False):
        clips = [clip.fl(add_vignette) for clip in clips]
    
    # Variable crossfade based on scene transition for dramatic effect
    faded_clips = [clips[0]]
    for i, clip in enumerate(clips[1:]):
        # Longer crossfades for dramatic transitions (every 3rd scene)
        duration = crossfade * (1.5 if i % 3 == 0 else 1.0)
        faded_clips.append(clip.crossfadein(duration))
    
    final = concatenate_videoclips(faded_clips, method="compose", padding=-crossfade)
    
    # Attach audio if provided
    if audio_path and os.path.exists(audio_path):
        from moviepy.editor import AudioFileClip
        audio_clip = AudioFileClip(audio_path)
        # Loop or trim audio to match video duration exactly
        if audio_clip.duration > final.duration:
            audio_clip = audio_clip.subclip(0, final.duration)
        final = final.set_audio(audio_clip)
        
    final.write_videofile(
        final_path, 
        codec="libx264", 
        audio_codec="aac" if audio_path else None,
        audio=True if audio_path else False, 
        logger=None,
        preset="medium",
        ffmpeg_params=["-crf", "18"]
    )
    final.close()
    if audio_path and 'audio_clip' in locals():
        audio_clip.close()
    for c in clips:
        c.close()
    return final_path
