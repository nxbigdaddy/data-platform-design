from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class ConnectorBase(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

class ConnectorCreate(ConnectorBase):
    pass

class ConnectorResponse(ConnectorBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class EtlTaskBase(BaseModel):
    name: str
    source_connector_id: int
    target_connector_id: int
    transformation_rules: List[Dict[str, Any]]
    schedule: str

class EtlTaskCreate(EtlTaskBase):
    pass

class EtlTaskResponse(EtlTaskBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

# 模拟连接器数据
connectors = []
next_connector_id = 1

# 模拟ETL任务数据
etl_tasks = []
next_task_id = 1

@router.post("/connector", response_model=ConnectorResponse)
async def create_connector(connector: ConnectorCreate):
    global next_connector_id
    new_connector = ConnectorResponse(
        id=next_connector_id,
        name=connector.name,
        type=connector.type,
        config=connector.config,
        status="ACTIVE",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    connectors.append(new_connector)
    next_connector_id += 1
    return new_connector

@router.get("/connector", response_model=List[ConnectorResponse])
async def get_connectors():
    return connectors

@router.get("/connector/{id}", response_model=ConnectorResponse)
async def get_connector(id: int):
    for connector in connectors:
        if connector.id == id:
            return connector
    raise HTTPException(status_code=404, detail="连接器不存在")

@router.delete("/connector/{id}")
async def delete_connector(id: int):
    global connectors
    connectors = [c for c in connectors if c.id != id]
    return {"message": "连接器删除成功"}

@router.post("/etl/task", response_model=EtlTaskResponse)
async def create_etl_task(task: EtlTaskCreate):
    global next_task_id
    new_task = EtlTaskResponse(
        id=next_task_id,
        name=task.name,
        source_connector_id=task.source_connector_id,
        target_connector_id=task.target_connector_id,
        transformation_rules=task.transformation_rules,
        schedule=task.schedule,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    etl_tasks.append(new_task)
    next_task_id += 1
    return new_task

@router.get("/etl/task", response_model=List[EtlTaskResponse])
async def get_etl_tasks():
    return etl_tasks

@router.get("/etl/task/{id}", response_model=EtlTaskResponse)
async def get_etl_task(id: int):
    for task in etl_tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="ETL任务不存在")

@router.post("/etl/task/{id}/start")
async def start_etl_task(id: int):
    for i, task in enumerate(etl_tasks):
        if task.id == id:
            task.status = "RUNNING"
            task.update_time = "2026-03-12T00:00:00"
            etl_tasks[i] = task
            return {"id": id, "status": "RUNNING"}
    raise HTTPException(status_code=404, detail="ETL任务不存在")

@router.get("/etl/task/{id}/status")
async def get_etl_task_status(id: int):
    for task in etl_tasks:
        if task.id == id:
            return {
                "id": id,
                "status": task.status,
                "progress": 75,  # 模拟进度
                "logs": ["开始执行", "正在转换数据", "已处理10000条记录"]
            }
    raise HTTPException(status_code=404, detail="ETL任务不存在")
