"""
Audio Agent: MusicGen-based cinematic soundtrack generation.
Creates custom background scores based on the Director's scene planning.
"""

import torch
import scipy.io.wavfile
import numpy as np

def load_audio_model(device="cuda", dtype=torch.float16):
    """Load the MusicGen model for soundtrack generation."""
    try:
        from transformers import AutoProcessor, MusicgenForConditionalGeneration
        
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained(
            "facebook/musicgen-small", 
            torch_dtype=dtype
        ).to(device)
        return processor, model
    except Exception as e:
        print(f"[Audio Agent] Error loading MusicGen: {e}")
        return None, None

def generate_soundtrack(premise, duration_seconds, processor, model, out_path, device="cuda"):
    """Generate a custom cinematic soundtrack matching the story premise."""
    print(f"  [Audio Agent] Composing {duration_seconds}s cinematic score...")
    
    # Create a cinematic prompt from the premise
    prompt = f"Epic cinematic orchestral movie soundtrack, tense, dramatic, high quality, matching this story: {premise}"
    
    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    ).to(device)
    
    # Calculate max_new_tokens (MusicGen uses 50 tokens per second of audio)
    tokens_per_second = 256 / 5.0 # roughly 50
    max_new_tokens = int(duration_seconds * tokens_per_second)
    
    with torch.no_grad():
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    audio_data = audio_values[0, 0].cpu().numpy()
    
    # Save to wav
    scipy.io.wavfile.write(out_path, rate=sampling_rate, data=audio_data)
    print(f"  [Audio Agent] Soundtrack saved to {out_path}")
    return out_path
