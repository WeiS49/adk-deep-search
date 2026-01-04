# Google GenAI SDK (v1beta) & Architecture Protocol
> **Version:** 2025.12.25 (Post-Gemini 3 Preview Release)
> **Library:** `google-genai` (Strict Pydantic Enforcement)

## 1. 🧠 Model Selection Strategy (Data Source: Real-time API)

根据 2025 年 12 月的 API 数据，请遵循以下选型策略：

| Role | Model ID | Key Specs | Why Use? |
| :--- | :--- | :--- | :--- |
| **Explorer (Dev)** | `gemini-3-flash-preview` | **Newest Arch** | 学习阶段首选。推理能力最强，响应最快。 |
| **Workhorse (Prod)** | `gemini-2.5-flash` | **65k Output**, Thinking | 生产环境首选。输出长度是 2.0 的 8 倍，支持 CoT 思考。 |
| **The Brain (Complex)**| `gemini-3-pro-preview` | **Max Intelligence** | 处理极其复杂的逻辑或多模态任务。 |
| **Avoid** | `gemini-flash-latest` | Unstable Alias | 避免在代码中使用 Alias，以防版本突变导致 Prompt 失效。 |

---

## 2. 🔌 Client Initialization (The Connectivity Layer)

**CRITICAL RULE**: 网络配置（超时、重试）必须封装在 `types.HttpOptions` 中。严禁在 Client 根层级传递 `retry_options`。

### Code Pattern (Copy-Paste Ready)
```python
import os
from google import genai
from google.genai import types

def get_client() -> genai.Client:
    """Factory to create the correct client based on environment."""
    
    # 统一的网络层配置
    network_config = types.HttpOptions(
        api_version="v1beta",
        timeout=30000  # 30 seconds
    )

    # Path A: Vertex AI (Recommended for $300 Credits)
    if os.environ.get("GOOGLE_CLOUD_PROJECT"):
        return genai.Client(
            vertexai=True,
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
            http_options=network_config
        )
    
    # Path B: API Key (Quick Prototype)
    return genai.Client(
        api_key=os.environ.get("GOOGLE_API_KEY"),
        http_options=network_config
    )