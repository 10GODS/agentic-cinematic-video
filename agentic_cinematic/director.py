"""
Director Agent: Local LLM (Qwen2.5-1.5B-Instruct) for scene planning.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import os
import gc
import torch

def load_planner(device="cuda", dtype=torch.float16):
    """Load the local LLM planner (Qwen2.5-1.5B-Instruct)."""
    PLANNER_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
    
    tok = AutoTokenizer.from_pretrained(PLANNER_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        PLANNER_MODEL_ID, 
        torch_dtype=dtype
    ).to(device)
    model.eval()
    return tok, model

def fallback_scene_template(premise, num_scenes, style):
    """Deterministic beat structure used if the local LLM's output can't be parsed as JSON."""
    beats = ["Establishing shot", "Inciting moment", "Rising tension", "Confrontation",
             "Climax", "Resolution", "Aftermath", "Final image"][:num_scenes]
    scenes = []
    for i, beat in enumerate(beats, start=1):
        scenes.append({
            "scene_id": i,
            "description": f"{beat} of: {premise}",
            "image_prompt": f"{beat}, {premise}, {style}",
            "camera": "wide establishing shot" if i == 1 else "medium shot, slow push-in",
            "mood": "epic",
        })
    return scenes

def plan_scenes(premise, num_scenes, style, tok, model, device="cuda"):
    """Plan scenes using the local LLM director agent."""
    system = ("You are a film director AI planning shots for a short cinematic video. "
              "Respond with ONLY a JSON array — no prose, no markdown code fences.")
    user = (
        f"Premise: {premise}\\n"
        f"Number of scenes: {num_scenes}\\n"
        f"Visual style to bake into every image prompt: {style}\\n"
        "Each array element must be an object with keys: "
        "'scene_id' (int, 1-indexed), 'description' (one sentence), "
        "'image_prompt' (a single detailed line suitable for an SDXL image model), "
        "'camera' (short camera/lens direction), 'mood' (one or two words)."
    )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=900, temperature=0.7, do_sample=True,
                              pad_token_id=tok.eos_token_id)
    text = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    try:
        start, end = text.index("["), text.rindex("]") + 1
        scenes = json.loads(text[start:end])
        assert isinstance(scenes, list) and len(scenes) > 0
        for s in scenes:
            assert "image_prompt" in s and "scene_id" in s
    except Exception as e:
        print(f"[director agent] could not parse local LLM output ({e}); using template fallback.")
        scenes = fallback_scene_template(premise, num_scenes, style)

    return scenes[:num_scenes]
