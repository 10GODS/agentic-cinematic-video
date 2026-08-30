"""
Director Agent: Gemini-powered scene planning with cinematic expertise.
Uses Google Gemini API (Gemini Enterprise) for intelligent scene decomposition
for film pre-production use case.

Fallback: deterministic beat-based template when Gemini is unavailable.
"""

import json
import os

# Try to import Gemini SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[director agent] google-generativeai not installed. Will use template fallback.")


def load_planner(device=None, dtype=None):
    """
    Load the Gemini planner.
    
    Returns a (tokenizer, model) tuple for API compatibility with the rest of the pipeline.
    For Gemini, tokenizer is None and model is the GenerativeModel instance.
    If Gemini is not configured, returns (None, None) and plan_scenes will use the fallback.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    if not GEMINI_AVAILABLE or not api_key:
        if not api_key:
            print("[director agent] GEMINI_API_KEY not set. Will use template fallback.")
        return None, None
    
    genai.configure(api_key=api_key)
    
    # Use Gemini 3.6 Flash for fast, cost-effective scene planning
    model_name = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    model = genai.GenerativeModel(
        model_name,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
            response_mime_type="application/json",
        ),
    )
    print(f"[director agent] {model_name} loaded for scene planning.")
    return None, model  # tokenizer=None, model=GenerativeModel


def fallback_scene_template(premise, num_scenes, style):
    """Enhanced deterministic beat structure with cinematic techniques."""
    shot_types = [
        "extreme wide shot", "wide shot", "medium shot", "close-up", 
        "extreme close-up", "over-the-shoulder", "two-shot", "point-of-view shot"
    ]
    composition_rules = [
        "rule of thirds", "leading lines", "symmetry", 
        "depth layers", "framing within frame", "diagonal composition"
    ]
    lighting_styles = [
        "golden hour lighting", "cinematic chiaroscuro", 
        "volumetric god rays", "rim lighting", "fill light", 
        "practical lighting", "motivated lighting"
    ]
    camera_movements = [
        "static shot", "slow push-in", "slow pull-out", 
        "left-to-right pan", "right-to-left pan", 
        "tilt up", "tilt down"
    ]
    
    beats = ["Establishing shot", "Inciting moment", "Rising tension", 
             "Confrontation", "Climax", "Resolution", "Aftermath", "Final image"][:num_scenes]
    
    scenes = []
    for i, beat in enumerate(beats, start=1):
        shot_idx = min(i, len(shot_types)-1)
        comp_idx = (i * 2) % len(composition_rules)
        light_idx = (i * 3) % len(lighting_styles)
        cam_idx = (i * 4) % len(camera_movements)
        
        shot_type = shot_types[shot_idx]
        composition = composition_rules[comp_idx]
        lighting = lighting_styles[light_idx]
        camera_move = camera_movements[cam_idx]
        
        enhanced_premise = premise
        if i == 1:
            enhanced_premise = f"wide establishing shot showing the scale and setting of: {premise}"
        elif i == 5:
            enhanced_premise = f"dramatic climax moment of: {premise}"
            
        scenes.append({
            "scene_id": i,
            "description": f"{beat} of: {premise}",
            "image_prompt": f"{enhanced_premise}, {shot_type}, {composition}, {lighting}, {camera_move}, {style}, 35mm film, professional cinematography",
            "camera": f"{shot_type}, {camera_move}",
            "mood": "cinematic",
            "importance": i
        })
    return scenes


def plan_scenes(premise, num_scenes, style, tok, model, device=None):
    """
    Plan scenes using Gemini director agent with cinematic expertise.
    Falls back to deterministic template if Gemini is unavailable.
    """
    if model is None:
        print("[director agent] Using enhanced template fallback (no Gemini).")
        return fallback_scene_template(premise, num_scenes, style)
    
    system_instruction = (
        "You are an expert film director AI planning shots for cinematic pre-visualization. "
        "You understand shot composition, lighting, camera movement, and visual storytelling. "
        "Your job is to decompose a story premise into a sequence of cinematic scenes, "
        "each with detailed image generation prompts suitable for Stable Diffusion XL."
    )
    
    user_prompt = f"""Premise: {premise}
Number of scenes: {num_scenes}
Visual style to bake into every image prompt: {style}

Generate a JSON array of {num_scenes} scene objects. Each object must have these keys:
- "scene_id" (int, 1-indexed)
- "description" (one sentence describing the narrative beat)
- "image_prompt" (a single detailed line suitable for an SDXL image model -- include shot type, composition, lighting, camera movement, and the visual style)
- "camera" (short camera/lens direction and movement, e.g. "extreme wide shot, slow push-in")
- "mood" (one or two words describing the emotional tone)

Rules:
1. Scene 1 should be an establishing shot.
2. The climax scene should have the most dramatic visual composition.
3. Each image_prompt must be self-contained (don't reference other scenes).
4. Vary shot types across scenes (wide, medium, close-up, etc.).
5. Include the visual style "{style}" in every image_prompt.

Respond with ONLY the JSON array, no other text."""

    try:
        response = model.generate_content(
            f"{system_instruction}\n\n{user_prompt}"
        )
        text = response.text
        
        if "``" + "`" in text:
            start = text.index("``" + "`") + 3
            if text[start:].startswith("json"):
                start += 4
            end = text.rindex("``" + "`")
            text = text[start:end].strip()
        
        scenes = json.loads(text)
        assert isinstance(scenes, list) and len(scenes) > 0
        
        for s in scenes:
            assert "image_prompt" in s and "scene_id" in s
            if "camera" not in s:
                s["camera"] = "medium shot"
            if "mood" not in s:
                s["mood"] = "cinematic"
        
        print(f"[director agent] Gemini planned {len(scenes)} scenes successfully.")
        return scenes[:num_scenes]
        
    except Exception as e:
        print(f"[director agent] Gemini call failed ({e}); using enhanced template fallback.")
        return fallback_scene_template(premise, num_scenes, style)