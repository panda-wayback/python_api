"""Hello World 示例路由 - 用于验证架构"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
def hello_world():
    """Hello World 示例接口"""
    return {"message": "Hello, World!"}


@router.get("/hello/{name}")
def hello_name(name: str):
    """带参数的 Hello 接口"""
    return {"message": f"Hello, {name}!"}
