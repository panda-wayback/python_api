"""FastAPI 应用入口"""

from fastapi import FastAPI
from app.api.v1.api import router as v1_router

app = FastAPI(
    title="My API",
    description="FastAPI 项目架构示例",
    version="1.0.0"
)

# 挂载版本化路由
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
def root():
    """根路径"""
    return {"message": "Welcome to FastAPI"}
