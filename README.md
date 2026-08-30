# Agentic Cinematic Video Generation

An end-to-end **agentic** pipeline that turns a one-line story premise into a short cinematic video, running entirely on a single GPU with **no external API keys**.

## Features

- **Agentic Director Agent**: A local LLM (Qwen2.5-1.5B-Instruct) plans scenes and writes prompts autonomously
- **Agentic Critic Agent**: A local CLIP model scores keyframes and automatically retries low-scoring scenes
- **Self-healing Interpolation**: Tries to use RIFE interpolation, falls back to optical-flow if unavailable
- **Fully Local**: Runs on a single consumer GPU (tested on T4/Kaggle) with no external API dependencies
- **Modular Design**: Each stage is decoupled for easy modification and extension

## Pipeline Stages

1. **Plan** - Local LLM (Director agent) breaks premise into scenes + prompts
2. **Keyframes** - SDXL generates images per scene, agentically retried via CLIP scoring (Critic agent)
3. **Image?Video** - Stable Video Diffusion XT animates keyframes into clips
4. **Interpolate** - RIFE (or optical-flow fallback) smooths motion to target FPS
5. **Upscale** - Real-ESRGAN upscales frames for cinematic quality
6. **Assemble** - Scenes are cross-faded into final MP4 video

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-cinematic-video.git
cd agentic-cinematic-video

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from agentic_cinematic import orchestrator

# Run with default configuration (Saturn astronaut premise)
final_video_path = orchestrator.run_pipeline()

# Or run with custom configuration
from agentic_cinematic.config import CONFIG
CONFIG["premise"] = "Your custom story premise here"
CONFIG["num_scenes"] = 4
final_video_path = orchestrator.run_pipeline(CONFIG)
```

## Requirements

- GPU with CUDA support (tested on NVIDIA T4 with 16GB VRAM)
- Python 3.8+
- Dependencies listed in `requirements.txt`

## How It Works

### Agentic Behavior

This pipeline demonstrates true agentic AI behavior through:

1. **Director Agent (LLM)**: Autonomously plans the cinematic breakdown of your story premise into visual scenes
2. **Critic Agent (CLIP)**: Evaluates each generated keyframe against its prompt and decides whether to retry with improved prompts
3. **Self-healing Systems**: Each stage includes fallback mechanisms to ensure the pipeline completes unattended

### Technical Details

- Uses quantized models (fp16) to fit within GPU memory constraints
- Implements aggressive memory cleanup between stages to enable running multiple large models on a single GPU
- Designed for reproducibility with seeded random number generation
- Includes comprehensive logging via `manifest.json` for auditability

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built for the Google Cloud Summer Blockbuster Hackathon
- Leverages state-of-the-art open models: Qwen, SDXL, SVD-XT, Real-ESRGAN, CLIP
'
