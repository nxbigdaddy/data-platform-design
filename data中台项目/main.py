from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="数据中台API",
    description="数据中台系统的API接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

@app.get("/")
async def root():
    return {"message": "数据中台API服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 导入路由
from api import datasource, sync, storage,汇聚,中枢,分析,开发,service

app.include_router(datasource.router, prefix="/api/datasource", tags=["数据源平台"])
app.include_router(sync.router, prefix="/api/sync", tags=["数据库同步平台"])
app.include_router(storage.router, prefix="/api/storage", tags=["数据存储平台"])
app.include_router(汇聚.router, prefix="/api/汇聚", tags=["数据汇聚平台"])
app.include_router(中枢.router, prefix="/api/中枢", tags=["数据中枢平台"])
app.include_router(分析.router, prefix="/api/分析", tags=["数据分析平台"])
app.include_router(开发.router, prefix="/api/开发", tags=["数据开发平台"])
app.include_router(service.router, prefix="/api/service", tags=["统一服务层"])
