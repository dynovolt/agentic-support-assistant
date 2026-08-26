\# Trendly Agentic Support Assistant



An AI-powered customer support assistant built for Trendly using Groq, FastAPI and Python.



The assistant can answer order-related questions, retrieve policy information, check return eligibility, create eligible returns and escalate cases that require human support.

## Live Demo

Live application:

https://agentic-support-assistant-m8v5.onrender.com/

The application is deployed using FastAPI and can be accessed directly through the browser.

## Local Start Command

After installing dependencies and configuring the Groq API key:

```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8000

\## Features



\- Order lookup

\- Shipping and return policy questions

\- Return eligibility checking

\- Return creation

\- Lost parcel escalation

\- Multi-turn conversations

\- Session-based conversation memory

\- Simple web chat interface

\- Human escalation for unsupported cases



\## Architecture



The application follows a simple tool-calling agent architecture:



User

↓

Web UI

↓

FastAPI

↓

LLM Agent

↓

Tools

├── get\_order

├── search\_policy

├── check\_eligibility

├── create\_return

└── escalate



The LLM decides which tool is required based on the user's request.



Business rules are enforced by the application tools and policy data rather than relying only on the model's response.



\## Project Structure



```text

agent.py             Agent and tool-calling logic

api.py               FastAPI backend

tools.py             Business tools

data.py              Local data loading

prompt.py            System prompt

orders.json          Sample order data

trendly\_policy.md    Support policy

test\_tools.py        Tool tests

requirements.txt     Python dependencies



static/

└── index.html       Web chat interface





## AI Usage Note

AI tools were used during development to assist with code generation, debugging, prompt refinement, test-case design, and documentation.

The implementation was reviewed, tested, and modified manually. The final business logic, tool definitions, prompts, test cases, deployment configuration, and project structure were validated against the assignment requirements.



