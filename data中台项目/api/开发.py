from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class StreamJobBase(BaseModel):
    name: str
    type: str
    code: str
    config: Dict[str, Any]

class StreamJobCreate(StreamJobBase):
    pass

class StreamJobResponse(StreamJobBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class PipelineBase(BaseModel):
    name: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class PipelineCreate(PipelineBase):
    pass

class PipelineResponse(PipelineBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

# 模拟流处理作业数据
stream_jobs = []
next_job_id = 1

# 模拟数据管道数据
pipelines = []
next_pipeline_id = 1

@router.post("/stream/job", response_model=StreamJobResponse)
async def create_stream_job(job: StreamJobCreate):
    global next_job_id
    new_job = StreamJobResponse(
        id=next_job_id,
        name=job.name,
        type=job.type,
        code=job.code,
        config=job.config,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    stream_jobs.append(new_job)
    next_job_id += 1
    return new_job

@router.get("/stream/job", response_model=List[StreamJobResponse])
async def get_stream_jobs():
    return stream_jobs

@router.get("/stream/job/{id}", response_model=StreamJobResponse)
async def get_stream_job(id: int):
    for job in stream_jobs:
        if job.id == id:
            return job
    raise HTTPException(status_code=404, detail="流处理作业不存在")

@router.post("/stream/job/{id}/start")
async def start_stream_job(id: int):
    for i, job in enumerate(stream_jobs):
        if job.id == id:
            job.status = "RUNNING"
            job.update_time = "2026-03-12T00:00:00"
            stream_jobs[i] = job
            return {"id": id, "status": "RUNNING"}
    raise HTTPException(status_code=404, detail="流处理作业不存在")

@router.post("/stream/job/{id}/stop")
async def stop_stream_job(id: int):
    for i, job in enumerate(stream_jobs):
        if job.id == id:
            job.status = "STOPPED"
            job.update_time = "2026-03-12T00:00:00"
            stream_jobs[i] = job
            return {"id": id, "status": "STOPPED"}
    raise HTTPException(status_code=404, detail="流处理作业不存在")

@router.get("/stream/job/{id}/status")
async def get_stream_job_status(id: int):
    for job in stream_jobs:
        if job.id == id:
            return {
                "id": id,
                "status": job.status,
                "metrics": {
                    "processed_records": 10000,
                    "latency_ms": 100,
                    "error_rate": 0.1
                },
                "logs": ["作业启动", "处理中", "无错误"]
            }
    raise HTTPException(status_code=404, detail="流处理作业不存在")

@router.post("/pipeline", response_model=PipelineResponse)
async def create_pipeline(pipeline: PipelineCreate):
    global next_pipeline_id
    new_pipeline = PipelineResponse(
        id=next_pipeline_id,
        name=pipeline.name,
        nodes=pipeline.nodes,
        edges=pipeline.edges,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    pipelines.append(new_pipeline)
    next_pipeline_id += 1
    return new_pipeline

@router.get("/pipeline", response_model=List[PipelineResponse])
async def get_pipelines():
    return pipelines

@router.get("/pipeline/{id}", response_model=PipelineResponse)
async def get_pipeline(id: int):
    for pipeline in pipelines:
        if pipeline.id == id:
            return pipeline
    raise HTTPException(status_code=404, detail="数据管道不存在")
