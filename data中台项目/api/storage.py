from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class ClusterBase(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

class ClusterCreate(ClusterBase):
    pass

class ClusterUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class ClusterResponse(ClusterBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class ResourceMonitorResponse(BaseModel):
    cluster_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float

class StoragePolicyBase(BaseModel):
    name: str
    type: str
    rules: Dict[str, Any]

class StoragePolicyCreate(StoragePolicyBase):
    pass

class StoragePolicyResponse(StoragePolicyBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

# 模拟集群数据
clusters = []
next_cluster_id = 1

# 模拟存储策略数据
storage_policies = []
next_policy_id = 1

@router.post("/cluster", response_model=ClusterResponse)
async def create_cluster(cluster: ClusterCreate):
    global next_cluster_id
    new_cluster = ClusterResponse(
        id=next_cluster_id,
        name=cluster.name,
        type=cluster.type,
        config=cluster.config,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    clusters.append(new_cluster)
    next_cluster_id += 1
    return new_cluster

@router.get("/cluster", response_model=List[ClusterResponse])
async def get_clusters():
    return clusters

@router.get("/cluster/{id}", response_model=ClusterResponse)
async def get_cluster(id: int):
    for cluster in clusters:
        if cluster.id == id:
            return cluster
    raise HTTPException(status_code=404, detail="集群不存在")

@router.put("/cluster/{id}", response_model=ClusterResponse)
async def update_cluster(id: int, cluster: ClusterUpdate):
    for i, c in enumerate(clusters):
        if c.id == id:
            update_data = cluster.model_dump(exclude_unset=True)
            updated_cluster = c.model_copy(update=update_data)
            updated_cluster.update_time = "2026-03-12T00:00:00"
            clusters[i] = updated_cluster
            return updated_cluster
    raise HTTPException(status_code=404, detail="集群不存在")

@router.delete("/cluster/{id}")
async def delete_cluster(id: int):
    global clusters
    clusters = [c for c in clusters if c.id != id]
    return {"message": "集群删除成功"}

@router.get("/cluster/{id}/monitor", response_model=ResourceMonitorResponse)
async def get_cluster_monitor(id: int):
    for cluster in clusters:
        if cluster.id == id:
            return ResourceMonitorResponse(
                cluster_id=id,
                cpu_usage=45.5,
                memory_usage=60.2,
                disk_usage=30.1,
                network_usage=25.3
            )
    raise HTTPException(status_code=404, detail="集群不存在")

@router.post("/policy", response_model=StoragePolicyResponse)
async def create_storage_policy(policy: StoragePolicyCreate):
    global next_policy_id
    new_policy = StoragePolicyResponse(
        id=next_policy_id,
        name=policy.name,
        type=policy.type,
        rules=policy.rules,
        status="ACTIVE",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    storage_policies.append(new_policy)
    next_policy_id += 1
    return new_policy

@router.get("/policy", response_model=List[StoragePolicyResponse])
async def get_storage_policies():
    return storage_policies

@router.get("/policy/{id}", response_model=StoragePolicyResponse)
async def get_storage_policy(id: int):
    for policy in storage_policies:
        if policy.id == id:
            return policy
    raise HTTPException(status_code=404, detail="存储策略不存在")
