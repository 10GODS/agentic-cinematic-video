#!/usr/bin/env python3
"""
Main entry point for the Agentic Cinematic Video Generation system.
"""

import argparse
import sys
import os

# Add the current directory to Python path so we can import agentic_cinematic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agentic_cinematic import orchestrator
from agentic_cinematic.config import CONFIG

def main():
    parser = argparse.ArgumentParser(description="Generate cinematic videos from text prompts using agentic AI")
    parser.add_argument("--premise", type=str, help="Story premise for the video")
    parser.add_argument("--scenes", type=int, help="Number of scenes in the video")
    parser.add_argument("--output", type=str, default="./agentic_cinematic_output", help="Output directory")
    
    args = parser.parse_args()
    
    # Update config if arguments provided
    config = CONFIG.copy()
    if args.premise:
        config["premise"] = args.premise
    if args.scenes:
        config["num_scenes"] = args.scenes
    
    print("Starting Agentic Cinematic Video Generation...")
    print(f"Premise: {config['premise']}")
    print(f"Number of scenes: {config['num_scenes']}")
    
    # Run the pipeline
    final_video_path = orchestrator.run_pipeline(config)
    
    print(f"\nSuccess! Final video generated at: {final_video_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
