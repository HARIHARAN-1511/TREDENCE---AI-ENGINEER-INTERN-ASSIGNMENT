from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid
import asyncio

from app.engine import WorkflowEngine, NodeFunction
from app.workflow import create_code_review_workflow, extract_code, check_complexity, detect_issues, evaluate_quality, suggest_improvements

app = FastAPI(title="Workflow Engine API")

# In-memory storage
graphs: Dict[str, WorkflowEngine] = {}
runs: Dict[str, Dict[str, Any]] = {}

# --- Models ---

class EdgeDefinition(BaseModel):
    source: str
    target: str

class GraphDefinition(BaseModel):
    nodes: List[str]
    edges: List[EdgeDefinition]
    entry_point: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class RunResponse(BaseModel):
    run_id: str
    status: str
    final_state: Optional[Dict[str, Any]]
    history: List[str]

# Available nodes for dynamic graph creation
NODE_REGISTRY: Dict[str, NodeFunction] = {
    "extract": extract_code,
    "complexity": check_complexity,
    "lint": detect_issues,
    "evaluate": evaluate_quality,
    "improve": suggest_improvements
}

# --- Endpoints ---

@app.post("/graph/create")
def create_graph(definition: GraphDefinition):
    """Create a new custom workflow graph."""
    engine = WorkflowEngine()
    
    for node_name in definition.nodes:
        if node_name not in NODE_REGISTRY:
            raise HTTPException(status_code=400, detail=f"Unknown node function: {node_name}")
        engine.add_node(node_name, NODE_REGISTRY[node_name])
        
    for edge in definition.edges:
        engine.add_edge(edge.source, edge.target)
        
    engine.set_entry_point(definition.entry_point)
    
    graph_id = str(uuid.uuid4())
    graphs[graph_id] = engine
    return {"graph_id": graph_id, "message": "Graph created successfully"}

@app.post("/graph/create/sample")
def create_sample_graph():
    """Create the pre-configured Code Review workflow."""
    engine = create_code_review_workflow()
    graph_id = str(uuid.uuid4())
    graphs[graph_id] = engine
    return {"graph_id": graph_id, "type": "Code Review Sample"}

@app.post("/graph/run", response_model=RunResponse)
async def run_graph(request: RunRequest):
    graph_id = request.graph_id
    if graph_id not in graphs:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    engine = graphs[graph_id]
    run_id = str(uuid.uuid4())
    
    runs[run_id] = {"status": "running", "state": request.initial_state, "history": []}
    
    try:
        result = await engine.run(request.initial_state)
        runs[run_id].update({
            "status": "completed",
            "state": result["final_state"],
            "history": result["history"]
        })
        
        return {
            "run_id": run_id,
            "status": "completed",
            "final_state": result["final_state"],
            "history": result["history"]
        }
    except Exception as e:
        runs[run_id]["status"] = "failed"
        runs[run_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]

@app.get("/")
def read_root():
    return {"message": "Workflow Engine is running. Docs at /docs"}
