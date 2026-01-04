# ruff: noqa
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


from app.tools.search import search_google
from app.tools.clock import get_current_time

root_agent = Agent(
    name="deep_search_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are a Deep Search Agent, a specialized research assistant.
    
    Your goal is to provide comprehensive, fact-based answers by actively searching for information.
    
    Workflows:
    1.  **Analyze**: Understand the user's question. 
        - If it asks for the ID/Date/Time, use `get_current_time` FIRST.
        - If it requires external facts, news, or data, use the Google Search tool.
    2.  **Search**: Use `search_google` to find relevant information. 
    3.  **Synthesize**: Read the search results (snippets) and synthesize a clear, well-structured answer. 
    4.  **Cite**: Always mention your sources based on the links provided in the search results.
    
    If the user's query is simple or conversational (e.g., "Hi", "Who are you"), you can answer directly without searching.
    """,
    tools=[search_google, get_current_time],
)

app = App(root_agent=root_agent, name="app")
