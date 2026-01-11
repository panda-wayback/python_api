"""计数器 API 路由"""

from fastapi import APIRouter, Depends
from domain.models import CounterCreate, CounterUpdate, CounterRead
from domain.services.counter_service import CounterService
from domain.repositories.counter_repo import CounterRepository

router = APIRouter()

# 依赖注入：创建 Repository 和 Service 实例
def get_counter_service() -> CounterService:
    """获取计数器服务实例"""
    repo = CounterRepository()
    return CounterService(repo)


@router.post("/counters", response_model=CounterRead, status_code=201)
def create_counter(
    counter_data: CounterCreate,
    service: CounterService = Depends(get_counter_service)
):
    """创建计数器"""
    return service.create_counter(counter_data)


@router.get("/counters/{counter_id}", response_model=CounterRead)
def get_counter(
    counter_id: str,
    service: CounterService = Depends(get_counter_service)
):
    """获取计数器"""
    return service.get_counter(counter_id)


@router.get("/counters", response_model=list[CounterRead])
def get_all_counters(
    service: CounterService = Depends(get_counter_service)
):
    """获取所有计数器"""
    return service.get_all_counters()


@router.put("/counters/{counter_id}", response_model=CounterRead)
def update_counter(
    counter_id: str,
    counter_data: CounterUpdate,
    service: CounterService = Depends(get_counter_service)
):
    """更新计数器值"""
    return service.update_counter(counter_id, counter_data)


@router.post("/counters/{counter_id}/increment", response_model=CounterRead)
def increment_counter(
    counter_id: str,
    service: CounterService = Depends(get_counter_service)
):
    """增加计数器值（+1）"""
    return service.increment_counter(counter_id)


@router.delete("/counters/{counter_id}", status_code=204)
def delete_counter(
    counter_id: str,
    service: CounterService = Depends(get_counter_service)
):
    """删除计数器"""
    service.delete_counter(counter_id)
    return None
