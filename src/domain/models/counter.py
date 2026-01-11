"""计数器相关数据模型"""

from pydantic import BaseModel, Field


class CounterCreate(BaseModel):
    """创建计数器请求模型"""
    name: str = Field(..., min_length=1, max_length=50, description="计数器名称")


class CounterRead(BaseModel):
    """计数器响应模型"""
    id: str
    name: str
    value: int = Field(..., description="计数器当前值")

    class Config:
        from_attributes = True


class CounterUpdate(BaseModel):
    """更新计数器请求模型"""
    value: int = Field(..., description="设置计数器值")
