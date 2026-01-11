"""v1 路由总入口"""

from fastapi import APIRouter
from .hello import router as hello_router

router = APIRouter()

# 注册各模块路由
router.include_router(hello_router, tags=["Hello"])
