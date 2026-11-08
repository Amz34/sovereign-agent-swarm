#!/usr/bin/env python3
"""
Base Agent Interface with Gemini 2.5 Flash SDK Integration
"""

import os
import sys
import json
import time
from typing import Dict, Any, List
from bus.protocol import SwarmMessage

def get_client():
    from google import genai
    return genai.Client()

class BaseSwarmAgent:
    def __init__(self, agent_id: str, role_title: str, system_mission: str, model: str = "gemini-2.5-flash"):
        self.agent_id = agent_id
        self.role_title = role_title
        self.system_mission = system_mission
        self.model = model
        self.client = get_client()

    def generate_json_response(self, prompt: str, schema_desc: str = "") -> Dict[str, Any]:
        """Queries Gemini with strict JSON enforcement and exponential backoff."""
        from google.genai import types
        full_prompt = f"""You are '{self.agent_id}' ({self.role_title}).
Mission: {self.system_mission}

{prompt}

Respond ONLY in valid RFC 8259 JSON format matching this schema:
{schema_desc}
Do NOT include markdown formatting wrappers like ```json or ```."""

        backoff = 3.0
        for attempt in range(4):
            try:
                resp = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
                text = resp.text.strip()
                return json.loads(text)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_time = backoff * (2 ** attempt)
                    print(f"  [{self.agent_id}] ⏳ Rate limit hit, backing off {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    time.sleep(backoff)

        # Fallback empty dict
        return {}
