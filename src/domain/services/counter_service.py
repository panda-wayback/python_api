"""计数器业务逻辑层 - Service 层"""

from typing import List
from fastapi import HTTPException, status
from domain.models import CounterCreate, CounterUpdate, CounterRead
from domain.repositories.counter_repo import CounterRepository
import uuid


class CounterService:
    """计数器 Service - 处理计数器相关业务逻辑"""
    
    def __init__(self, counter_repo: CounterRepository):
        self.counter_repo = counter_repo
    
    def create_counter(self, counter_data: CounterCreate) -> CounterRead:
        """创建计数器"""
        counter_id = str(uuid.uuid4())
        return self.counter_repo.create(counter_data, counter_id)
    
    def get_counter(self, counter_id: str) -> CounterRead:
        """获取计数器"""
        counter = self.counter_repo.get_by_id(counter_id)
        if not counter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"计数器 ID {counter_id} 不存在"
            )
        return counter
    
    def get_all_counters(self) -> List[CounterRead]:
        """获取所有计数器"""
        return self.counter_repo.get_all()
    
    def update_counter(self, counter_id: str, counter_data: CounterUpdate) -> CounterRead:
        """更新计数器值"""
        updated_counter = self.counter_repo.update(counter_id, counter_data)
        if not updated_counter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"计数器 ID {counter_id} 不存在"
            )
        return updated_counter
    
    def increment_counter(self, counter_id: str) -> CounterRead:
        """增加计数器值（业务逻辑：每次加1）"""
        counter = self.counter_repo.increment(counter_id)
        if not counter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"计数器 ID {counter_id} 不存在"
            )
        return counter
    
    def delete_counter(self, counter_id: str) -> None:
        """删除计数器"""
        success = self.counter_repo.delete(counter_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"计数器 ID {counter_id} 不存在"
            )
