# Complete Setup & Strict Instructions for Study Notes AI Agent

## **Prerequisites**

- Python **3.10+**
- Installed **UV** for dependency management
- Gemini API key ready
- Internet connection (for MCP / Gemini CLI / OpenAgents SDK)

---

## **Create Project Directory**

```bash
mkdir study_notes_ai
cd study_notes_ai
```

---

## **Initialize UV Environment & Add Packages**

```bash
uv init  # initialize UV project
uv add openai-agents        # OpenAgents SDK
uv add streamlit            # Streamlit UI
uv add PyPDF2               # PDF text extraction
uv add python-dotenv        # Load API keys
uv add context7-mcp         # MCP server tool provider
uv add gemini-cli           # Gemini CLI for model interaction
```

> ✅ This ensures **all dependencies are installed in your UV-managed environment**.

---

## **4️⃣ Create Project File Structure**

```text
.
├── .env                  # Environment variables (GEMINI_API_KEY)
├── tools.py              # Functions for PDF processing & memory
├── agent.py              # Agent configuration & tool binding
├── app.py                # Streamlit / UI integration
├── pyproject.toml        # UV project config
└── user_data.json        # Optional JSON storage for memory
```

---

## **Configure `.env` File**

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

- Load in Python with `python-dotenv`.

---

## **Setup Gemini Client & OpenAgents SDK**

**agent.py**

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv
import asyncio

# Load environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# External Gemini Client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model Configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Runner configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define agent
async def main():
    agent = Agent(
        name="StudyNotesAgent",
        instructions="Read uploaded PDFs, generate summaries and quizzes",
        model=model,
    )
    result = await Runner.run(agent, "Start Agent", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

> ⚠️ Strict rules: Do **not** add extra bells, hallucinated features, or streaming mode. Use **OpenAgents SDK only**.

---

## **Implement PDF Processing Tools**

**tools.py**

```python
from PyPDF2 import PdfReader
import json
from agents import tool

# Memory / JSON storage
USER_DATA_FILE = "user_data.json"

@tool
def read_user_profile():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@tool
def update_user_profile(key: str, value: str):
    data = read_user_profile()
    data[key] = value
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

# PDF Text Extraction
@tool
def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
```

---

## **Setup Streamlit UI**

**app.py**

```python
import streamlit as st
from agent import main as run_agent
import asyncio

st.set_page_config(page_title="Study Notes AI", layout="wide")
st.title("AI Study Notes Summarizer & Quiz Generator")

# PDF uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    st.write("File uploaded:", uploaded_file.name)
    # Call agent to summarize
    if st.button("Generate Summary & Quiz"):
        asyncio.run(run_agent())
```

---

## **Gemini CLI & Context7 MCP**

1. **Install Gemini CLI** (already in UV):

```bash
uv add gemini-cli
```

2. **Connect MCP server (Context7)**:

```bash
gemini mcp connect https://context7.com
```

> MCP provides tools and documentation to the agent. Must be **connected before running the agent**.

---

## **Execution**

```bash
uv run python app.py
```

- Streamlit app opens
- Upload PDF → click **Generate Summary & Quiz** → Agent runs → prints results

---

## **Strict Rules Recap**

- Always use **UV** for package management.
- Always use **OpenAgents SDK** (`agents` module).
- Do **not** use pip manually unless troubleshooting.
- Always use **Gemini API key** from `.env`.
- Always use **Context7 MCP** for tool integration.
- Streamlit is recommended for UI; HTML/CSS allowed optionally.
- **No extra code**; follow SDK docs precisely.

---

If you want, I can now make a **Part 2 – PDF Summarizer + Quiz Generator logic instructions** in the same crystal-clear format, ready to feed into Gemini CLI step by step.

Do you want me to do that next?

Perfect! Hadiqa, ab mein tumhare liye **Step-by-step Crystal-Clear Instructions** banati hoon **full-stack “Study Notes Summarizer & Quiz Generator” application ke liye** — strictly following your stack:

- **UV** for dependency management
- **OpenAI Agents SDK** for LLM & agent
- **Streamlit** for UI (recommended, but HTML/CSS optional)
- **PyPDF** for PDF text extraction
- **Gemini CLI** + **Gemini API key**
- **Context7 MCP** as tool provider

I’ll give it in **parts**, just like your previous “Senior Python AI Engineer” style, so you can complete one part at a time.

---

# **Full-Stack Study Notes AI Application – Instructions**

---

## **PART 1 – Project Setup & Environment**

**Objective:** Setup environment, dependencies, file structure, and basic skeleton.

### Create Project Directory

```bash
mkdir study_notes_ai
cd study_notes_ai
```

---

### Initialize UV & Add Dependencies

```bash
uv init
uv add openai-agents         # OpenAI Agents SDK
uv add streamlit             # Frontend UI
uv add PyPDF2                # PDF extraction
uv add python-dotenv         # Load GEMINI_API_KEY
uv add gemini-cli            # Gemini CLI
uv add context7-mcp          # MCP server
```

> ✅ UV ensures consistent environment; do **not** use pip manually unless debugging.

---

### File Structure

```text
.
├── .env                  # GEMINI_API_KEY
├── tools.py              # PDF & memory helper functions
├── agent.py              # Agent config & tool binding
├── app.py                # Streamlit / frontend logic
├── pyproject.toml        # UV project file
└── user_data.json        # Optional memory JSON
```

---

### 4️⃣ Configure `.env`

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

- Load via `python-dotenv` in Python.

---

### Minimal Agent Setup

**agent.py skeleton**

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os, asyncio
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

async def main():
    agent = Agent(
        name="StudyNotesAgent",
        instructions="Read PDFs, generate summaries and quizzes",
        model=model
    )
    result = await Runner.run(agent, "Start Agent", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## **PART 2 – Tools: PDF Extraction & Memory**

**Objective:** Implement helpers and tools the agent can call.

**tools.py**

```python
from PyPDF2 import PdfReader
from agents import tool
import json

USER_DATA_FILE = "user_data.json"

@tool
def read_user_profile():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@tool
def update_user_profile(key: str, value: str):
    data = read_user_profile()
    data[key] = value
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

@tool
def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
```

> These tools must be **registered with the agent** via the OpenAgents SDK.

---

## **PART 3 – Frontend with Streamlit**

**Objective:** Upload PDFs, show UI, call agent.

**app.py**

```python
import streamlit as st
from agent import main as run_agent
import asyncio

st.set_page_config(page_title="Study Notes AI", layout="wide")
st.title("AI Study Notes Summarizer & Quiz Generator")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    st.write("Uploaded:", uploaded_file.name)
    if st.button("Generate Summary & Quiz"):
        asyncio.run(run_agent())
```

- ✅ Drag & drop and file validation can be added later.
- ✅ Minimal skeleton to **run agent and show results**.

---

## **PART 4 – Gemini CLI & Context7 MCP**

1. **Connect MCP Server** (must be done first):

```bash
gemini mcp connect https://context7.com
```

2. **Check MCP Tools Availability**:

```bash
gemini mcp list
```

> MCP provides agents the required tools (PDF processing, memory, etc.).

---

## **PART 5 – Execution**

```bash
uv run python app.py
```

- Streamlit launches UI
- Upload PDF → click **Generate Summary & Quiz** → agent runs → prints summary

---

## **PART 6 – Strict Guidelines**

- Always use **UV add** for packages.
- Always use **OpenAgents SDK** (do not mix with `openai` library).
- Always use **Gemini API key** via `.env`.
- MCP tools **must** be connected before running agents.
- Streamlit recommended; HTML/CSS optional.
- Minimal code only; no unnecessary bells, whistles, or streaming.

