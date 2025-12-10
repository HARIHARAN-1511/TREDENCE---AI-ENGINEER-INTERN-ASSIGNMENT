# Workflow Engine
A lightweight Python backend for defining and executing agentic workflows. Built with FastAPI.

## Overview
This project implements a simple graph-based workflow engine. It allows you to define nodes (Python functions) and edges to create complex execution flows with branching and looping. The state is shared across all steps.

I built this to demonstrate:
- Clean API design with FastAPI
- State management and transitions
- Conditional logic (branching/loops)
- Extensibility via a tool registry

## How to Run

### 1. Verification Script (Quickest Test)
To verify that the core engine logic works without starting the full web server, I created a script for you.

Run this command in your terminal:
```bash
python run_verification.py
```
You should see output showing the "Code Review" workflow running, detecting issues, looping to fix them, and finishing.

### 2. Running the API Server (The Main App)
To run the full FastAPI application:

**Step A: Install Dependencies**
If you haven't already, install the required packages:
```bash
pip install -r requirements.txt
```

**Step B: Start the Server**
Run this command from the `trendence-main` directory:
```bash
uvicorn app.main:app --reload
```
You should see a message saying `Application startup complete`.

### 3. Using the Workflow Engine
Once the server is running, the easiest way to interact with it is via the automatic documentation page.

1.  Open your browser to: **`http://127.0.0.1:8000/docs`**
2.  **Create a Graph**:
    *   Click on **`POST /graph/create/sample`**.
    *   Click **Try it out** -> **Execute**.
    *   Copy the `graph_id` from the response (e.g., `"graph_id": "some-uuid"`).
3.  **Run the Graph**:
    *   Click on **`POST /graph/run`**.
    *   Click **Try it out**.
    *   Paste your `graph_id` into the JSON body.
    *   You can use the default `initial_state` or provide some Python code to test:
        ```json
        {
          "graph_id": "PASTE_YOUR_ID_HERE",
          "initial_state": {
            "code": "def hello():\n    print('world')"
          }
        }
        ```
    *   Click **Execute**.

You will see the workflow execute, the steps taken in `history`, and the final results!

## Structure
- `app/engine.py`: The core graph runner.
- `app/main.py`: API endpoints.
- `app/workflow.py`: The sample agent logic.
- `app/tools.py`: Helper functions for the agent.
