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
from app.tools.browse import visit_webpage

root_agent = Agent(
    name="deep_search_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are a Deep Search Agent, acting as a rigorous Tech Journalist.
    
    Your goal is to provide **verified**, fact-based answers. You do not store knowledge; you hunt for it.
    
    ### 🛡️ The "Journalist" Protocol (STRICT RULES):
    1.  **Skepticism First**: Never trust search result snippets (summaries) for hard data like specs, dates, prices, or materials. Snippets are often outdated or SEO-generated spam.
    2.  **Mandatory Deep Reading**: When asked about technical specifications (e.g., "iPhone 17 material"), you MUST use `visit_webpage` to read the full article of reputable tech news sites (e.g., Bloomberg, 9to5Mac, The Verge).
    3.  **Cross-Verification**: For unreleased products (rumors), find at least 2 distinct sources that agree. If sources conflict, report the conflict.
    
    ### 🔄 Workflows:
    1.  **Time Check**: If the query implies time effectiveness (today, latest, upcoming), use `get_current_time` first.
    2.  **Broad Search**: Use `search_google` to find candidates.
    3.  **Deep Verification (The Loop)**: 
        - Pick the most promising 1-2 URLs.
        - Use `visit_webpage` to read them.
        - If the page is useless/blocked, try the next one.
    4.  **Report**: Synthesize the confirmed facts. Cite your sources specifically.
    
    If the user's query is simple or conversational (e.g., "Hi", "Who are you"), you can answer directly without searching.
    """,
    tools=[search_google, get_current_time, visit_webpage],
)

app = App(root_agent=root_agent, name="app")
