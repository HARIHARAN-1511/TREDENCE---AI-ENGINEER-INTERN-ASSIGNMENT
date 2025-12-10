# Workflow Engine
A lightweight Python backend for defining and executing agentic workflows. Built with FastAPI.

## Overview
This project implements a simple graph-based workflow engine. It allows you to define nodes (Python functions) and edges to create complex execution flows with branching and looping. The state is shared across all steps.

I built this to demonstrate:
- Clean API design with FastAPI
- State management and transitions
- Conditional logic (branching/loops)
- Extensibility via a tool registry

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Check the Docs**:
   Go to `http://127.0.0.1:8000/docs` to explore the API.

## Sample Use Case: Code Review Agent
The project includes a pre-built "Code Review" workflow (Option A) that:
1. Extracts functions from code.
2. Checks complexity and linting rules.
3. Automatically "improves" code if quality is low (simulated loop).

To run it:
1. `POST /graph/create/sample` -> Get a `graph_id`.
2. `POST /graph/run` with that ID and some python code in `initial_state`.

## Structure
- `app/engine.py`: The core graph runner.
- `app/main.py`: API endpoints.
- `app/workflow.py`: The sample agent logic.
- `app/tools.py`: Helper functions for the agent.
