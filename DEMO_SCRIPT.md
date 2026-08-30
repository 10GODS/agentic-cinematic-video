# ?? 3-Minute Demo Video Script
## Agentic Cinematic Video Generation for Summer Blockbuster Hackathon

This script guides the creation of a compelling 3-minute demonstration video that shows your agentic system functioning as built, highlights the Google Cloud and Partner technology integration, and solves the real M&E workflow problem.

## ?? Video Timing Breakdown

### [0:00-0:30] PROBLEM STATEMENT: The Pre-Production Bottleneck
- **Visual**: Split screen showing expensive traditional pre-production
  - Left: Concept artists drawing storyboards ($$$/hour)
  - VFX artists creating pre-vis in expensive suites
  - Directors and cinematographers in lengthy meetings
  - Stacks of money burning or clock spinning fast
- **Text Overlay**: "Hollywood spends $2B+ annually on pre-production visualization"
- **Narration**: 
  > "Film studios spend weeks and hundreds of thousands of dollars on concept art, storyboards, and pre-visualization before shooting even begins. Creative misalignment between teams leads to costly reshoots and wasted resources."
- **Transition**: Quick cut to glitch effect transforming into clean interface

### [0:30-1:00] INTRODUCTION: The Agentic Solution
- **Visual**: Clean animated logo: "Agentic Cinematic Video Generation"
- **Visual**: Simple diagram showing agent collaboration
  - Story Premise ? [Director Agent] ? [Critic Agent] ? Cinematic Video
- **Text Overlay**: "Autonomous AI Agents for Film Pre-Production"
- **Narration**:
  > "Our agentic system transforms a one-sentence story premise into cinematic reference videos, replacing expensive traditional pre-vis workflows with autonomous AI collaboration."
- **Quick Cuts**: 
  - Close-up of terminal showing agentic pipeline starting
  - Split screen: Text input ? Agent planning ? Visual output

### [1:00-1:45] TECHNICAL DEMO: Agents in Action
- **Visual**: Screen recording of Jupyter notebook or terminal running the pipeline
- **Highlight 1: Director Agent Planning** (1:00-1:15)
  - Show premise input: "A lone astronaut discovers an ancient temple on a moon of Saturn, guarded by a spectral tiger made of starlight."
  - Show console output: Director agent generating scene plans
  - Highlight: "scene 1: Establishing shot of: [premise], extreme wide shot, rule of thirds, golden hour lighting, static shot"
  - **Text Overlay**: "Director Agent: Plans cinematic shots with shot type, composition, lighting, camera movement"
- **Highlight 2: Critic Agent Quality Control** (1:15-1:30)
  - Show keyframe generation with CLIP scores
  - Show retry mechanism when score < threshold
  - Show strengthened prompt on retry
  - **Text Overlay**: "Critic Agent: Scores keyframes & requests retries for visual refinement"
- **Highlight 3: Agentic Collaboration Loop** (1:30-1:45)
  - Show multiple iterations improving CLIP score
  - Visual: Progress bar or score improvement animation
  - **Text Overlay**: "Autonomous retry loop: Director refines, Critic scores until quality threshold met"

### [1:45-2:15] CLOUD & PARTNER INTEGRATION: Real Enterprise Use
- **Visual**: Split screen demonstration
  - Left: Terminal showing pipeline running
  - Right: Live updating dashboards
- **Google Cloud Storage Segment** (1:45-1:55)
  - Show console output: "[GCS] Uploaded scene_01_keyframe.png to gs://agentic-cinematic-hackathon/keyframes/..."
  - Show GCS browser showing uploaded keyframes and final video
  - **Text Overlay**: "Actual Google Cloud Use: Media asset management via Storage API"
  - **Small Icon**: ?? GCS
- **Grafana Labs Segment** (1:55-2:10)
  - Show live Grafana dashboard with panels:
    - "Scene Planning Duration" (graph)
    - "Keyframe CLIP Scores" (gauge per scene)
    - "Generation Retries" (counter)
    - "GPU Memory Usage" (time series)
  - Show metric updates happening in real-time as pipeline runs
  - **Text Overlay**: "Partner Technology Use: Grafana Labs for production observability"
  - **Small Icon**: ?? Grafana
- **Narration** (throughout 1:45-2:15):
  > "Unlike demos that fake cloud integration, our system makes actual Google Cloud Storage API calls to manage media assets. We integrate Grafana Labs - our partner technology - for real-time observability of the agentic pipeline, showing exactly how this would operate in a production M&E environment."

### [2:15-2:45] CINEMATIC OUTPUT & QUALITY ENHANCEMENTS
- **Visual**: Show final video playing in multiple formats
  - Full cinematic video (2048x1152 with film LUT)
  - Side-by-side comparison: Raw output vs. Enhanced output
  - Close-up details showing film grain and motion blur
- **Highlight Quality Features**:
  - **Film LUT**: Show teal-and-orange color grading
    - **Text Overlay**: "Cinematic Color Grading: Teal-and-orange film LUT applied"
  - **Motion Blur**: Show subtle blur on moving elements
    - **Text Overlay**: "Subtle Motion Blur: Reduces CGI crispness for filmic feel"
  - **Shot Adaptation**: Show wide shot with more motion vs. close-up with subtle motion
    - **Text Overlay**: "Adaptive Motion: SVD-XT motion bucket tuned to shot type"
  - **Resolution**: Show 2048x1152 upscaled output
    - **Text Overlay**: "2x Upscaling: Real-ESRGAN for cinematic resolution"
- **Narration**:
  > "The system doesn't just generate video - it creates professional pre-visualization with cinematic enhancements: film LUT color grading, subtle motion blur, adaptive motion based on shot type, and 2x upscaling to cinematic resolution - all autonomously determined by our agents."

### [2:45-3:00] RESULTS & CALL TO ACTION
- **Visual**: Final video playing full screen with uplifting music
- **Text Overlays** (appearing sequentially):
  - "Generated Entirely on Kaggle T4 GPU"
  - "No External API Keys - All Models Run Locally"
  - "Google Cloud Storage & Grafana Labs Integrated"
  - "Solves Real M&E Workflow Problem"
- **Narration**:
  > "What once required weeks of manual work and hundreds of thousands of dollars can now be accomplished by autonomous AI agents working together. Our system demonstrates actual Google Cloud use for media asset management, genuine partner technology integration with Grafana Labs, and solves a real bottleneck in film pre-production."
- **Final Screen** (last 5 seconds):
  - Centered: "Agentic Cinematic Video Generation"
  - Bottom left: "GitHub: github.com/[YOUR_USERNAME]/agentic-cinematic-video"
  - Bottom right: "#AgenticCinema #SummerBlockbuster"
  - **Text Overlay**: "Try it with your own story premise: python run.py --premise \"[Your story here]\""
  - **Narration**: "Visit our GitHub repository to run this yourself and transform your story into cinematic pre-vis."

## ?? Production Tips for the Demo Video

### Recording:
- Use OBS Studio or similar screen recording software
- Record at 1080p or higher resolution
- Record system audio for console output clarity
- Consider using a microphone for narration (clear, professional tone)

### Editing Software:
- Free options: DaVinci Resolve, Shotcut, OpenShot
- Paid options: Adobe Premiere Pro, Final Cut Pro

### Key Elements to Include:
1. **Actual Console Output**: Show real logs from your running pipeline
2. **Live Metrics**: Show Grafana dashboard updating in real-time
3. **Cloud Evidence**: Show GCS console or gsutil commands showing uploads
4. **Before/After**: Show raw vs. enhanced video (film LUT, motion blur)
5. **Clear Narrative**: Explain what you're showing - don't just show code
6. **Professional Appearance**: Clean desktop, close irrelevant apps

### What NOT to Do:
- ? Don't make it a cinematic trailer with no technical content
- ? Don't fake cloud/show fake metrics
- ? Don't show only the final video without explaining how it was made
- ? Don't exceed 3 minutes (judges will stop watching)
- ? Don't use copyrighted music without permission

## ?? Verification Checklist for Judges

Before submitting, ensure your demo video shows:
- [ ] Actual code running (not mocked output)
- [ ] Clear evidence of Google Cloud Storage API calls
- [ ] Clear evidence of Grafana Labs metric submission
- [ ] The Director and Critic agents working together
- [ ] The final video output with visible enhancements
- [ ] Explanation of the M&E problem being solved
- [ ] Publicly accessible URL (YouTube or Vimeo)
- [ ] English audio or subtitles
- [ ] Length = 3 minutes

## ?? Remember: Show, Don't Just Tell

The most effective demo videos:
1. **Show** the agents collaborating (console output of plans and scores)
2. **Show** the cloud integration (actual upload commands and GCS evidence)
3. **Show** the partner tech integration (live Grafana dashboard)
4. **Show** the final product with enhancements
5. **Tell** the viewer what they're seeing and why it matters

Good luck with your submission! Your agentic cinema project has all the elements needed to stand out - now go show the judges what autonomous AI can do for film pre-production. ???
