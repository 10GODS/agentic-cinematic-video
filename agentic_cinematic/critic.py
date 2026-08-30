"""
Critic Agent: CLIP-based quality gate for scoring keyframes in film pre-production.
Provides agentic feedback to Director for iterative refinement.
"""

import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image

def load_critic(device="cuda", dtype=torch.float16):
    """Load the CLIP critic model for quality assessment."""
    CLIP_MODEL_ID = "openai/clip-vit-base-patch32"
    clip_model = CLIPModel.from_pretrained(CLIP_MODEL_ID).to(device).eval()
    clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID)
    return clip_model, clip_processor

@torch.no_grad()
def clip_score(image: Image.Image, text: str, clip_model, clip_processor, device="cuda") -> float:
    """Score an image against a text prompt using CLIP for agentic feedback."""
    inputs = clip_processor(text=[text], images=image, return_tensors="pt", padding=True, truncation=True, max_length=77).to(device)
    outputs = clip_model(**inputs)
    img_e = outputs.image_embeds / outputs.image_embeds.norm(dim=-1, keepdim=True)
    txt_e = outputs.text_embeds / outputs.text_embeds.norm(dim=-1, keepdim=True)
    return (img_e @ txt_e.T).item()
