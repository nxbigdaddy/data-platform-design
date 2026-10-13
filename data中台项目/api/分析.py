from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class CubeBase(BaseModel):
    name: str
    dimensions: List[str]
    measures: List[str]
    source_table: str

class CubeCreate(CubeBase):
    pass

class CubeResponse(CubeBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    sql: str
    limit: int = 100

class QueryResponse(BaseModel):
    columns: List[str]
    rows: List[List]
    total: int
    execution_time: float

class DataLakeFormatBase(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

class DataLakeFormatCreate(DataLakeFormatBase):
    pass

class DataLakeFormatResponse(DataLakeFormatBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

# 模拟立方体数据
cubes = []
next_cube_id = 1

# 模拟数据湖格式数据
data_lake_formats = []
next_format_id = 1

@router.post("/cube", response_model=CubeResponse)
async def create_cube(cube: CubeCreate):
    global next_cube_id
    new_cube = CubeResponse(
        id=next_cube_id,
        name=cube.name,
        dimensions=cube.dimensions,
        measures=cube.measures,
        source_table=cube.source_table,
        status="CREATED",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    cubes.append(new_cube)
    next_cube_id += 1
    return new_cube

@router.get("/cube", response_model=List[CubeResponse])
async def get_cubes():
    return cubes

@router.get("/cube/{id}", response_model=CubeResponse)
async def get_cube(id: int):
    for cube in cubes:
        if cube.id == id:
            return cube
    raise HTTPException(status_code=404, detail="立方体不存在")

@router.post("/cube/{id}/build")
async def build_cube(id: int):
    for i, cube in enumerate(cubes):
        if cube.id == id:
            cube.status = "BUILDING"
            cube.update_time = "2026-03-12T00:00:00"
            cubes[i] = cube
            return {"id": id, "status": "BUILDING"}
    raise HTTPException(status_code=404, detail="立方体不存在")

@router.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    # 模拟执行SQL查询
    return QueryResponse(
        columns=["id", "name", "value", "date"],
        rows=[
            [1, "产品A", 100, "2026-03-01"],
            [2, "产品B", 200, "2026-03-01"],
            [3, "产品A", 150, "2026-03-02"],
            [4, "产品B", 250, "2026-03-02"]
        ],
        total=4,
        execution_time=0.123
    )

@router.post("/datalake/format", response_model=DataLakeFormatResponse)
async def create_data_lake_format(format: DataLakeFormatCreate):
    global next_format_id
    new_format = DataLakeFormatResponse(
        id=next_format_id,
        name=format.name,
        type=format.type,
        config=format.config,
        status="ACTIVE",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    data_lake_formats.append(new_format)
    next_format_id += 1
    return new_format

@router.get("/datalake/format", response_model=List[DataLakeFormatResponse])
async def get_data_lake_formats():
    return data_lake_formats

@router.get("/datalake/format/{id}", response_model=DataLakeFormatResponse)
async def get_data_lake_format(id: int):
    for format in data_lake_formats:
        if format.id == id:
            return format
    raise HTTPException(status_code=404, detail="数据湖格式不存在")
