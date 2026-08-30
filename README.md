# ?? Agentic Cinematic Video Generation
## Summer Blockbuster Hackathon Submission
### Solving Automated Concept Visualization for Film Pre-Production

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Storage-4285F4.svg)](https://cloud.google.com/storage)
[![Grafana Labs](https://img.shields.io/badge/Grafana-Labs-F16800.svg)](https://grafana.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

> **"Transforming film pre-production from weeks of manual work to minutes of agentic AI collaboration"**

## ?? The Problem: Film Pre-Production Bottleneck

Hollywood spends **$2B+ annually** on pre-production visualization including concept art, storyboards, and pre-visualization (pre-vis). This process involves:
- Weeks of manual iteration between directors, cinematographers, and VFX artists
- Costly miscommunications leading to expensive reshoots
- Limited ability to explore creative alternatives due to time/budget constraints

## ?? Our Agentic Solution

We built an **autonomous agentic system** that transforms a one-sentence story premise into cinematic reference videos, replacing expensive traditional pre-vis workflows.

### ?? Hackathon Requirements Met
| Requirement | How We Satisfy It |
|-------------|-------------------|
| **Actual Google Cloud Use** | ? Google Cloud Storage for media asset management (keyframes, clips, final videos) |
| **Partner Technology Use** | ? Grafana Labs for real-time observability of agentic pipeline |
| **Real M&E Workflow Problem** | ? Solves pre-production visualization bottleneck in film industry |
| **Public GitHub Repo** | ? This repository with MIT license |
| **3-Minute Demo Video** | ? Shows agent functioning as built (see DEMO_SCRIPT.md) |

## ?? Agentic Architecture

Our system features two collaborating AI agents working autonomously:

### 1. **Director Agent** (Google Gemini API (Gemini Enterprise))
- **Role**: Creative director & cinematographer
- **Function**: Breaks story premise into cinematic shots with specific:
  - Shot types (extreme wide, close-up, over-the-shoulder, etc.)
  - Composition techniques (rule of thirds, leading lines, symmetry)
  - Lighting styles (golden hour, chiaroscuro, volumetric god rays)
  - Camera movements (push-ins, pans, tilts)
- **Output**: Detailed scene plans and SDXL-ready prompts

### 2. **Critic Agent** (Local CLIP Model)
- **Role**: Visual quality supervisor
- **Function**: 
  - Scores generated keyframes against director's prompts using CLIP
  - Requests retries with strengthened prompts when quality below threshold
  - Provides iterative feedback for visual refinement
- **Output**: Quality scores and agentic retry decisions

### ?? Agentic Collaboration
```
Story Premise 
    ? Director Agent: Plans shots & writes prompts
    ? Critic Agent: Scores keyframes & requests retries
    ? Director Agent: Refines prompts based on feedback
    ? (Repeat until quality threshold met)
    ? SVD-XT: Generates video clips
    ? Interpolation: Smooths motion to 24fps cinematic
    ? Real-ESRGAN: Upscales to cinematic resolution
    ? Assembler: Creates final video with crossfades
```

## ?? Google Cloud Integration (Actual Use)

We integrate **Google Cloud Storage** for professional media asset management:

- **Keyframes**: Uploaded as PNG files for concept art review
- **Video Clips**: Intermediate SVD-XT outputs stored for iteration
- **Final Output**: Cinematic reference videos available for team access
- **Versioning**: Timestamped files enable change tracking
- **Access Control**: Team members can access assets via GCP IAM

**Benefits for M&E Workflow:**
- Centralized asset repository for global teams
- Eliminates file sharing bottlenecks
- Enables asynchronous review and feedback
- Provides backup and disaster recovery

## ?? Grafana Labs Integration (Partner Tech Use)

We integrate **Grafana Cloud** for production-grade observability:

### Metrics Monitored in Real-Time:
- **Agent Collaboration**: 
  - Scene planning duration
  - Keyframe CLIP scores (quality feedback)
  - Generation retry counts (agentic behavior)
- **Pipeline Performance**:
  - Stage-by-stage timing (SDXL, SVD-XT, interpolation, upscaling)
  - GPU memory utilization
  - End-to-end generation time
- **Quality Assurance**:
  - Final output validation
  - Resource efficiency metrics

### Benefits for M&E Workflow:
- **Production Readiness**: Shows system is monitorable in production
- **Debugging**: Identifies bottlenecks in agentic collaboration
- **Optimization**: Data-driven improvements to creative process
- **Transparency**: Provides visibility into autonomous agent decisions

## ?? Key Features for Film Pre-Production

### Cinematic Quality Enhancements:
- **Film LUT Color Grading**: Teal-and-orange cinematic look
- **Subtle Motion Blur**: Reduces "CGI crispness" for filmic feel
- **Adaptive Quality Allocation**: More render effort on emotionally important scenes (climax gets 50% more effort)
- **Shot-Type Specific Motion**: SVD-XT motion bucket adapted to camera movement (close-ups = subtle motion, wide shots = more motion)
- **Professional Encoding**: CRF 18 for visually lossless output

### Agentic Intelligence:
- **Autonomous Retry Loop**: Director and Critic collaborate without human intervention
- **Fallback Systems**: Self-healing interpolation (optical flow if RIFE unavailable)
- **Memory Management**: Aggressive GPU cleanup between stages for T4 compatibility
- **Deterministic Fallback**: Template-based planning if LLM output unparseable

## ?? Project Structure
```
agentic-cinematic-video/
+-- agentic_cinematic/           # Core agentic pipeline
�   +-- __init__.py
�   +-- config.py                # Settings & cloud/partner config
�   +-- director.py              # LLM-based scene planner (Director agent)
�   +-- critic.py                # CLIP-based quality critic (Critic agent)
�   +-- keyframe_generator.py    # SDXL with agentic retry
�   +-- video_generator.py       # SVD-XT with shot-type motion adaptation
�   +-- interpolator.py          # Self-healing optical flow interpolation
�   +-- upscaler.py              # Real-ESRGAN with T4 optimization
�   +-- assembler.py             # Final assembly with cinematic enhancements
�   +-- orchestrator.py          # Main pipeline with GCS & Grafana integration
+-- monitoring.py                # Grafana metrics helper
+-- run.py                       # Command-line entry point
+-- requirements.txt             # Dependencies
+-- README.md                    # This file
+-- DEMO_SCRIPT.md               # Guide for 3-minute demo video
+-- LICENSE                      # MIT license
+-- .gitignore                   # Git ignore rules
```

## ?? Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/agentic-cinematic-video.git
cd agentic-cinematic-video
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Gemini API Key
   ``bash
   set GEMINI_API_KEY="your-api-key-here"
   ``

4. Run with Default Premise (Saturn Astronaut)
```bash
python run.py
```

### 5. Run with Custom Premise
```bash
python run.py --premise "Your story premise here" --scenes 6
```

### 6. For Hackathon Submission (Configure Cloud/Partner)
```bash
# Set environment variables for Google Cloud
export GCS_BUCKET_NAME="your-hackathon-bucket"
export GCS_PROJECT_ID="your-gcp-project-id"  # Optional

# Set environment variables for Grafana Labs
export GRAFANA_ENABLED="true"
export GRAFANA_USER="your-grafana-cloud-user"
export GRAFANA_KEY="your-grafana-cloud-api-key"
export GRAFANA_URL="https://metrics.grafana.com/api/prometheus/push"  # Default

# Then run
python run.py
```

## ?? Creating Your 3-Minute Demo Video

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for a complete script showing:
- Problem statement visualization
- Agentic Director/Critic collaboration demo
- Google Cloud Storage uploads in action
- Live Grafana dashboard updating with pipeline metrics
- Final cinematic output with film LUT applied
- Clear call-to-action for judges

## ?? Submission Checklist

For your Devpost submission, ensure you have:

1. [ ] **Public GitHub Repository** (this repo)
2. [ ] **Open Source License** (MIT License included)
3. [ ] **3-Minute Demo Video** showing:
   - Agent functioning as built (not cinematic trailer)
   - Publicly visible on YouTube/Vimeo with English audio/subtitles
   - Demonstrates actual Google Cloud and Partner tech use
4. [ ] **Hosted Project URL** (can be GitHub Pages or similar)
5. [ ] **Completed Devpost Form**

## ?? Why This Wins the Hackathon

### Technical Excellence:
- ? **Actual GCP Use**: Not just namedropping - real Storage API calls for media asset management
- ? **Partner Technology**: Real Grafana Labs integration with meaningful metrics
- ? **T4 Compatible**: Core generation runs on free Kaggle T4 GPU
- ? **Production Ready**: Observability, error handling, and logging
- ? **Open Source**: MIT license allows commercial use

### M&E Impact:
- ? **Solves Real Problem**: Addresses $2B+ pre-production bottleneck
- ? **Clear Workflow**: Maps directly to film industry roles (Director, Critic/VFX supervisor)
- ? **Business Value**: Shows time/cost savings potential
- ? **Innovation**: First agentic system for cinematic pre-vis

### Demo Quality:
- ? **Visual Appeal**: Cinematic enhancements make output professionally compelling
- ? **Technical Depth**: Shows sophisticated agentic collaboration
- ? **Cloud Narrative**: Clear story of GCP and partner integration
- ? **Judging Criteria Alignment**: 
  - Technological Implementation (GCP + Grafana + agentic AI)
  - Design (Complete product experience, not just PoC)
  - Potential Impact (Solves real M&E problem)
  - Quality of Idea (Creative, non-obvious use of tech)

## ?? License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ?? Acknowledgments

- Built for the [Google Cloud Summer Blockbuster Hackathon](https://summerblockbuster.devpost.com/)
- Leverages state-of-the-art open models: Gemini 2.0 Flash, SDXL, SVD-XT, Real-ESRGAN, CLIP
- Inspired by the future of agentic AI in media and entertainment

---

**Ready to transform your story premise into cinematic pre-vis?**  
?? Edit the premise in `run.py` or pass it via `--premise`  
?? Run `python run.py` and watch the agents collaborate  
?? See your vision come alive in agentic_cinematic_output/

*"Lights. Camera. Agents."* ????

