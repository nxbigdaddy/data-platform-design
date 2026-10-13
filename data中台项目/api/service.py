from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class ApiBase(BaseModel):
    name: str
    url: str
    method: str
    params: Optional[Dict[str, Any]] = None

class ApiCreate(ApiBase):
    pass

class ApiResponse(ApiBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    create_time: str

    class Config:
        from_attributes = True

class MonitorResponse(BaseModel):
    system_status: str
    components: List[Dict[str, Any]]
    metrics: Dict[str, Any]

# 模拟API数据
apis = []
next_api_id = 1

# 模拟用户数据
users = []
next_user_id = 1

@router.post("/api", response_model=ApiResponse)
async def create_api(api: ApiCreate):
    global next_api_id
    new_api = ApiResponse(
        id=next_api_id,
        name=api.name,
        url=api.url,
        method=api.method,
        params=api.params,
        status="ACTIVE",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    apis.append(new_api)
    next_api_id += 1
    return new_api

@router.get("/api", response_model=List[ApiResponse])
async def get_apis():
    return apis

@router.get("/api/{id}", response_model=ApiResponse)
async def get_api(id: int):
    for api in apis:
        if api.id == id:
            return api
    raise HTTPException(status_code=404, detail="API不存在")

@router.post("/user", response_model=UserResponse)
async def create_user(user: UserCreate):
    global next_user_id
    new_user = UserResponse(
        id=next_user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        create_time="2026-03-12T00:00:00"
    )
    users.append(new_user)
    next_user_id += 1
    return new_user

@router.get("/user", response_model=List[UserResponse])
async def get_users():
    return users

@router.get("/user/{id}", response_model=UserResponse)
async def get_user(id: int):
    for user in users:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="用户不存在")

@router.get("/monitor", response_model=MonitorResponse)
async def get_monitor():
    # 模拟监控数据
    return MonitorResponse(
        system_status="HEALTHY",
        components=[
            {"name": "数据源平台", "status": "HEALTHY", "response_time": 0.1},
            {"name": "数据库同步平台", "status": "HEALTHY", "response_time": 0.2},
            {"name": "数据中枢平台", "status": "HEALTHY", "response_time": 0.15},
            {"name": "数据存储平台", "status": "HEALTHY", "response_time": 0.05}
        ],
        metrics={
            "cpu_usage": 40,
            "memory_usage": 60,
            "disk_usage": 30,
            "api_calls": 1000,
            "error_rate": 0.1
        }
    )
