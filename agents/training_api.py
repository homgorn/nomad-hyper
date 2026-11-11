"""FastAPI training API for Unsloth Desktop backend."""
# Requires: pip install fastapi uvicorn unsloth transformers trl peft accelerate bitsandbytes
# Usage: uvicorn agents.training_api:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path

app = FastAPI(title="NOMAD Hyper Training API")

class TrainRequest(BaseModel):
    domain: str
    model: str = "qwen3.5:4b"
    epochs: int = 3
    lr: float = 2e-4
    batch_size: int = 2
    lora_rank: int = 32

class JobStatus(BaseModel):
    id: str
    status: str
    progress: float = 0.0
    message: str = ""

jobs = {}

@app.post("/api/train")
async def start_training(req: TrainRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 0.0,
        "message": f"Training {req.domain} model {req.model}",
        "request": req.dict()
    }
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/train/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/api/train/{job_id}/adapter")
async def get_adapter(job_id: str):
    adapter_path = Path(f"./data/adapters/{job_id}")
    if not adapter_path.exists():
        raise HTTPException(status_code=404, detail="Adapter not ready")
    return {"path": str(adapter_path), "domain": jobs[job_id]["request"]["domain"]}

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "nomad-hyper-training"}

# TODO: implement actual Unsloth training loop in background task
# TODO: integrate with agents/orchestrator.py
