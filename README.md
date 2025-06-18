# Bitcoin Trading Advisor Crew

Welcome to the Bitcoin Trading Advisor Crew project, powered by [crewAI](https://crewai.com) and [Fast API](https://fastapi.tiangolo.com/). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
Then to install Fast API and related packages

```bash
uv pip install -r requirements.txt
```

## Using Ollama with Crewai
There's a bug in the litellm package, there's an open PR for it but to solve it for now make the fix manually
PR: https://github.com/BerriAI/litellm/pull/10917/files
File path: .venv/lib/python3.12/site-packages/litellm/litellm_core_utils/prompt_templates/factory.py

## LLM
You can use whatever LLM model you prefer, you just need to update the self.llm variable to initialise the correct model

```python
self.llm = LLM(
    model="ollama/qwen2.5:latest",
    base_url="http://localhost:11434",
    api_key="ollama",  # dummy value
    # temperature=0.1,
)
```

To use the default llm, make sure before running the project to:
1. Install Ollama: [ollama.ai](https://ollama.com/)
2. In a terminal, run the model: ollama run qwen2.5:latest

## Running the Project

To start the FAST api project, run this from the root folder of your project:

```bash
uvicorn app.main:app --reload
```

thorugh postman connect to the websocket endpoint, every 15 minutes a recommendatino will be broadcasted to all clients connected on it.

Endpoint: ws://127.0.0.1:8000/ws/get-decision
