"""
Monitoring Module: Handles Grafana Labs metrics for agentic cinematic pipeline.
Provides easy integration for observability in the Summer Blockbuster Hackathon submission.
"""

import json
import time
import requests
from typing import Dict, Optional

class GrafanaMonitor:
    """Handles sending metrics to Grafana Cloud for agentic pipeline observability."""
    
    def __init__(self, user: str, api_key: str, url: str = "https://metrics.grafana.com/api/prometheus/push"):
        self.user = user
        self.api_key = api_key
        self.url = url
        self.enabled = bool(user and api_key)
        
        if not self.enabled:
            print("[Monitor] Grafana monitoring disabled (missing credentials)")
    
    def send_metric(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Send a single metric to Grafana Cloud."""
        if not self.enabled:
            return
            
        if labels is None:
            labels = {}
        
        data = [{
            "metric": metric_name,
            "values": [int(time.time()), value],
            "labels": {
                "job": "agentic_cinema_hackathon",
                "instance": "kaggle_t4",
                **labels
            }
        }]
        
        try:
            response = requests.post(
                self.url,
                data=json.dumps(data),
                auth=(self.user, self.api_key),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 204:
                print(f"[Monitor] Sent {metric_name}: {value}")
            else:
                print(f"[Monitor] Grafana error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[Monitor] Error sending metric (non-fatal): {e}")
    
    def send_stage_timing(self, stage_name: str, duration_seconds: float):
        """Send timing metric for a pipeline stage."""
        self.send_metric(f"{stage_name}_duration", duration_seconds, {"stage": stage_name})
    
    def send_quality_score(self, scene_id: int, score: float):
        """Send CLIP quality score for a scene."""
        self.send_metric("keyframe_clip_score", score, {"scene": str(scene_id)})
    
    def send_gpu_memory(self, device_id: int = 0):
        """Send current GPU memory usage."""
        try:
            import torch
            if torch.cuda.is_available():
                memory_gb = torch.cuda.memory_allocated(device_id) / 1e9
                self.send_metric("gpu_memory_used", memory_gb, {"unit": "GB", "device": str(device_id)})
        except ImportError:
            pass  # Torch not available

# Convenience function for simple usage
def send_grafana_metric(metric_name: str, value: float, labels: Optional[Dict[str, str]] = None,
                       user: str = "", api_key: str = "", url: str = "https://metrics.grafana.com/api/prometheus/push"):
    """Send a metric to Grafana Cloud using direct parameters."""
    if not user or not api_key:
        return
        
    monitor = GrafanaMonitor(user, api_key, url)
    monitor.send_metric(metric_name, value, labels)
