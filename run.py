#!/usr/bin/env python3
"""
Entry point for Agentic Cinematic Video Generation - Summer Blockbuster Hackathon.
Solves: Automated Concept Visualization for Film Pre-Production
Integrates: Google Cloud Storage (asset management) + Grafana Labs (observability)
"""

import argparse
import sys
import os

# Add the current directory to Python path so we can import agentic_cinematic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agentic_cinematic import orchestrator

def main():
    parser = argparse.ArgumentParser(
        description="Generate cinematic videos from text prompts using agentic AI for film pre-production",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate video with default premise (Saturn astronaut)
  python run.py
  
  # Generate video with custom premise
  python run.py --premise "A detective discovers a clue in a rainy neon city"
  
  # Generate shorter video for faster testing
  python run.py --scenes 4 --premise "Two rivals face off in a western showdown"
  
  # For full hackathon submission, ensure GCS and Grafana credentials are set as environment variables
        '''
    )
    parser.add_argument("--premise", type=str, help="Story premise for the video")
    parser.add_argument("--scenes", type=int, help="Number of scenes in the video (1-8)")
    parser.add_argument("--output", type=str, default="./agentic_cinematic_output", help="Output directory")
    
    args = parser.parse_args()
    
    # Validate scenes argument
    if args.scenes is not None and (args.scenes < 1 or args.scenes > 8):
        print("Error: Number of scenes must be between 1 and 8")
        return 1
    
    print("?? Agentic Cinematic Video Generation")
    print("?? Summer Blockbuster Hackathon Submission")
    print("?? Solving: Automated Concept Visualization for Film Pre-Production")
    print("??  Integrates: Google Cloud Storage + Grafana Labs (partner tech)")
    print()
    
    # Setup cloud and partner integrations
    from agentic_cinematic.orchestrator import setup_gcs_client, setup_grafana_client
    from agentic_cinematic.config import CONFIG
    
    print("Initializing cloud and partner integrations...")
    gcs_client = setup_gcs_client()
    grafana_config = setup_grafana_client()
    
    # Apply CLI overrides to config
    config = {**CONFIG}
    if args.premise:
        config["premise"] = args.premise
    if args.scenes:
        config["num_scenes"] = args.scenes
    
    # Run the pipeline
    try:
        final_video_path = orchestrator.run_pipeline(
            config=config, gcs_client=gcs_client, grafana_config=grafana_config
        )
        print(f"\n\U0001f3ac Success! Final video generated at: {final_video_path}")
        print("\U0001f4cb Check agentic_cinematic_output/manifest.json for full execution details")
        print("\U0001f4ca Grafana dashboard should show real-time metrics if configured")
        print("\u2601\ufe0f  Media assets uploaded to Google Cloud Storage if configured")
        return 0
    except Exception as e:
        print(f"\n\u274c Error running pipeline: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
