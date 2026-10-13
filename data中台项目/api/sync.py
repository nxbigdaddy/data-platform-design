from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class SyncTaskBase(BaseModel):
    name: str
    sourceId: int
    targetId: int
    syncType: str
    syncStrategy: Dict[str, Any]

class SyncTaskCreate(SyncTaskBase):
    pass

class SyncTaskUpdate(BaseModel):
    name: Optional[str] = None
    sourceId: Optional[int] = None
    targetId: Optional[int] = None
    syncType: Optional[str] = None
    syncStrategy: Optional[Dict[str, Any]] = None

class SyncTaskResponse(SyncTaskBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

# 模拟同步任务数据
sync_tasks = []
next_task_id = 1

@router.post("/task", response_model=SyncTaskResponse)
async def create_sync_task(task: SyncTaskCreate):
    global next_task_id
    new_task = SyncTaskResponse(
        id=next_task_id,
        name=task.name,
        sourceId=task.sourceId,
        targetId=task.targetId,
        syncType=task.syncType,
        syncStrategy=task.syncStrategy,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    sync_tasks.append(new_task)
    next_task_id += 1
    return new_task

@router.get("/task", response_model=List[SyncTaskResponse])
async def get_sync_tasks():
    return sync_tasks

@router.get("/task/{id}", response_model=SyncTaskResponse)
async def get_sync_task(id: int):
    for task in sync_tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="同步任务不存在")

@router.put("/task/{id}", response_model=SyncTaskResponse)
async def update_sync_task(id: int, task: SyncTaskUpdate):
    for i, t in enumerate(sync_tasks):
        if t.id == id:
            update_data = task.model_dump(exclude_unset=True)
            updated_task = t.model_copy(update=update_data)
            updated_task.update_time = "2026-03-12T00:00:00"
            sync_tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="同步任务不存在")

@router.delete("/task/{id}")
async def delete_sync_task(id: int):
    global sync_tasks
    sync_tasks = [t for t in sync_tasks if t.id != id]
    return {"message": "同步任务删除成功"}

@router.post("/task/{id}/start")
async def start_sync_task(id: int):
    for i, task in enumerate(sync_tasks):
        if task.id == id:
            task.status = "RUNNING"
            task.update_time = "2026-03-12T00:00:00"
            sync_tasks[i] = task
            return {"id": id, "status": "RUNNING"}
    raise HTTPException(status_code=404, detail="同步任务不存在")

@router.post("/task/{id}/stop")
async def stop_sync_task(id: int):
    for i, task in enumerate(sync_tasks):
        if task.id == id:
            task.status = "STOPPED"
            task.update_time = "2026-03-12T00:00:00"
            sync_tasks[i] = task
            return {"id": id, "status": "STOPPED"}
    raise HTTPException(status_code=404, detail="同步任务不存在")

@router.get("/task/{id}/status")
async def get_sync_task_status(id: int):
    for task in sync_tasks:
        if task.id == id:
            return {
                "id": id,
                "status": task.status,
                "progress": 50,  # 模拟进度
                "logs": ["开始同步", "同步中", "已同步1000条数据"]
            }
    raise HTTPException(status_code=404, detail="同步任务不存在")
