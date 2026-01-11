"""v1 路由总入口"""

from fastapi import APIRouter
from app.api.v1.hello import router as hello_router
from app.api.v1.counter import router as counter_router

router = APIRouter()

# 注册各模块路由
router.include_router(hello_router, tags=["Hello"])
router.include_router(counter_router, tags=["Counter"])