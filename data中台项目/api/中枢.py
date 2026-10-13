from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class MetadataBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class MetadataCreate(MetadataBase):
    pass

class MetadataResponse(MetadataBase):
    id: int
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    name: str
    type: str
    metadata_id: int
    tags: Optional[List[str]] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    status: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True

class LineageResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class QualityCheckResponse(BaseModel):
    asset_id: int
    check_results: List[Dict[str, Any]]
    overall_score: float

# 模拟元数据数据
metadata_list = []
next_metadata_id = 1

# 模拟资产数据
assets = []
next_asset_id = 1

@router.post("/metadata", response_model=MetadataResponse)
async def create_metadata(metadata: MetadataCreate):
    global next_metadata_id
    new_metadata = MetadataResponse(
        id=next_metadata_id,
        name=metadata.name,
        type=metadata.type,
        description=metadata.description,
        attributes=metadata.attributes,
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    metadata_list.append(new_metadata)
    next_metadata_id += 1
    return new_metadata

@router.get("/metadata", response_model=List[MetadataResponse])
async def get_metadata(type: Optional[str] = None):
    if type:
        return [m for m in metadata_list if m.type == type]
    return metadata_list

@router.get("/metadata/{id}", response_model=MetadataResponse)
async def get_metadata_by_id(id: int):
    for metadata in metadata_list:
        if metadata.id == id:
            return metadata
    raise HTTPException(status_code=404, detail="元数据不存在")

@router.post("/asset", response_model=AssetResponse)
async def create_asset(asset: AssetCreate):
    global next_asset_id
    new_asset = AssetResponse(
        id=next_asset_id,
        name=asset.name,
        type=asset.type,
        metadata_id=asset.metadata_id,
        tags=asset.tags,
        status="ACTIVE",
        create_time="2026-03-12T00:00:00",
        update_time="2026-03-12T00:00:00"
    )
    assets.append(new_asset)
    next_asset_id += 1
    return new_asset

@router.get("/asset", response_model=List[AssetResponse])
async def get_assets():
    return assets

@router.get("/asset/{id}", response_model=AssetResponse)
async def get_asset(id: int):
    for asset in assets:
        if asset.id == id:
            return asset
    raise HTTPException(status_code=404, detail="资产不存在")

@router.get("/lineage/{id}", response_model=LineageResponse)
async def get_lineage(id: int):
    # 模拟数据血缘
    return LineageResponse(
        nodes=[
            {"id": 1, "name": "源表1", "type": "TABLE"},
            {"id": 2, "name": "中间表", "type": "TABLE"},
            {"id": id, "name": "目标表", "type": "TABLE"}
        ],
        edges=[
            {"source": 1, "target": 2, "type": "TRANSFORM"},
            {"source": 2, "target": id, "type": "TRANSFORM"}
        ]
    )

@router.get("/quality/{id}", response_model=QualityCheckResponse)
async def get_quality_check(id: int):
    # 模拟数据质量检查
    return QualityCheckResponse(
        asset_id=id,
        check_results=[
            {"check_type": "完整性", "status": "PASS", "score": 95},
            {"check_type": "一致性", "status": "PASS", "score": 90},
            {"check_type": "准确性", "status": "WARN", "score": 80},
            {"check_type": "时效性", "status": "PASS", "score": 98}
        ],
        overall_score=90.75
    )
