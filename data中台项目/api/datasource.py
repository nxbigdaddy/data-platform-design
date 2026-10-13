from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class DataSourceBase(BaseModel):
    name: str
    type: str
    host: str
    port: int
    database: str
    username: str
    password: str

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: YOUR_PASSWORD] = None

class DataSourceResponse(DataSourceBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class TestConnectionRequest(BaseModel):
    type: str
    host: str
    port: int
    database: str
    username: str
    password: str

class TestConnectionResponse(BaseModel):
    success: bool
    message: str

class ExecuteSqlRequest(BaseModel):
    datasourceId: int
    sql: str
    limit: int = 100

class ExecuteSqlResponse(BaseModel):
    columns: List[str]
    rows: List[List]
    total: int

# 模拟数据源数据
data_sources = []
next_id = 1

@router.post("/", response_model=DataSourceResponse)
async def create_datasource(datasource: DataSourceCreate):
    global next_id
    new_datasource = DataSourceResponse(
        id=next_id,
        name=datasource.name,
        type=datasource.type,
        host=datasource.host,
        port=datasource.port,
        database=datasource.database,
        username=datasource.username,
        password=YOUR_PASSWORD,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    data_sources.append(new_datasource)
    next_id += 1
    return new_datasource

@router.get("/", response_model=List[DataSourceResponse])
async def get_datasources():
    return data_sources

@router.get("/{id}", response_model=DataSourceResponse)
async def get_datasource(id: int):
    for datasource in data_sources:
        if datasource.id == id:
            return datasource
    raise HTTPException(status_code=404, detail="数据源不存在")

@router.put("/{id}", response_model=DataSourceResponse)
async def update_datasource(id: int, datasource: DataSourceUpdate):
    for i, ds in enumerate(data_sources):
        if ds.id == id:
            update_data = datasource.model_dump(exclude_unset=True)
            updated_datasource = ds.model_copy(update=update_data)
            updated_datasource.update_time = "2026-03-12T00:00:00"
            data_sources[i] = updated_datasource
            return updated_datasource
    raise HTTPException(status_code=404, detail="数据源不存在")

@router.delete("/{id}")
async def delete_datasource(id: int):
    global data_sources
    data_sources = [ds for ds in data_sources if ds.id != id]
    return {"message": "数据源删除成功"}

@router.post("/test", response_model=TestConnectionResponse)
async def test_connection(request: TestConnectionRequest):
    # 模拟测试连接
    return TestConnectionResponse(
        success=True,
        message="连接成功"
    )

@router.post("/execute", response_model=ExecuteSqlResponse)
async def execute_sql(request: ExecuteSqlRequest):
    # 模拟执行SQL
    return ExecuteSqlResponse(
        columns=["id", "name", "value"],
        rows=[[1, "测试1", 100], [2, "测试2", 200]],
        total=2
    )
