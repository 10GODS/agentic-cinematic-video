# Agentic Cinematic Video Generation - 3 Minute Demo Video Script

## [0:00-0:30] Introduction
- Opening shot: Title screen with project name and tagline
- Narration: "Meet Agentic Cinematic Video Generation - a revolutionary AI system that turns simple text prompts into Hollywood-quality videos using autonomous AI agents."
- Brief overview: "Unlike traditional video generation tools that require complex prompting and manual iteration, our system uses AI agents that work together autonomously to create cinematic videos from a single sentence."
- Key features text overlay:
  - Fully local execution (no API keys needed)
  - Agentic AI with Director and Critic agents
  - Runs on consumer GPU (tested on NVIDIA T4)
  - End-to-end pipeline from text to video

## [0:30-1:30] Technical Overview
- Animation showing pipeline stages:
  1. Text Premise ? Director Agent (LLM) ? Scene Plans & Prompts
  2. Scene Prompts ? SDXL ? Keyframes ? Critic Agent (CLIP) ? Score & Retry if needed
  3. Approved Keyframes ? SVD-XT ? Video Clips
  4. Video Clips ? Interpolation (RIFE/Optical Flow) ? Smooth Motion
  5. Frames ? Real-ESRGAN ? Upscaled Frames
  6. Upscaled Clips ? Assembler ? Final Video with Crossfades
- Narration explains each stage briefly:
  - "Our Director Agent, powered by a local Qwen LLM, breaks your story into cinematic scenes and crafts detailed image prompts."
  - "The Critic Agent, using CLIP neural networks, evaluates each generated frame and asks for improvements when needed - all autonomously."
  - "Stable Video Diffusion XT brings still images to life, while our self-healing interpolation ensures smooth motion."
  - "Real-ESRGAN upscales to cinematic quality, and finally our assembler blends everything with professional crossfades."

## [1:30-2:30] Live Demo
- Screen capture of the Jupyter notebook running
- Show the CONFIG cell with the Saturn astronaut premise
- Show execution of each stage with console output highlights:
  - Director agent planning scenes
  - Keyframe generation with CLIP scores and retries
  - Video generation with SVD-XT
  - Interpolation process
  - Upscaling with Real-ESRGAN
  - Final assembly
- Display intermediate results:
  - Generated keyframe images
  - Short video clips
- Show final output: agentic_cinematic_output/final_cinematic_video.mp4 playing

## [2:30-3:00] Results and Conclusion
- Final video playing in full
- Text overlay: "Generated entirely on a single GPU with no external APIs"
- Narration: "What once required teams of artists, expensive software, and hours of manual work can now be accomplished by autonomous AI agents working together."
- Call to action:
  - GitHub repository: [github.com/yourusername/agentic-cinematic-video]
  - "Clone, run, and create your own cinematic adventures!"
- Closing screen with project name and hashtag: #AgenticCinema
