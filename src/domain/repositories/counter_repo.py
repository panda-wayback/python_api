"""计数器数据访问层 - Repository 模式"""

from typing import Optional
from domain.models import CounterCreate, CounterUpdate, CounterRead


class CounterRepository:
    """计数器 Repository - 封装数据访问逻辑"""
    
    def __init__(self):
        # 使用内存字典模拟数据库
        self._counters: dict[str, dict] = {}
    
    def create(self, counter_data: CounterCreate, counter_id: str) -> CounterRead:
        """创建计数器"""
        counter_dict = {
            "id": counter_id,
            "name": counter_data.name,
            "value": 0
        }
        self._counters[counter_id] = counter_dict
        return CounterRead(**counter_dict)
    
    def get_by_id(self, counter_id: str) -> Optional[CounterRead]:
        """根据 ID 获取计数器"""
        counter = self._counters.get(counter_id)
        if counter:
            return CounterRead(**counter)
        return None
    
    def get_all(self) -> list[CounterRead]:
        """获取所有计数器"""
        return [CounterRead(**counter) for counter in self._counters.values()]
    
    def update(self, counter_id: str, counter_data: CounterUpdate) -> Optional[CounterRead]:
        """更新计数器"""
        if counter_id not in self._counters:
            return None
        
        self._counters[counter_id]["value"] = counter_data.value
        return CounterRead(**self._counters[counter_id])
    
    def increment(self, counter_id: str) -> Optional[CounterRead]:
        """增加计数器值"""
        if counter_id not in self._counters:
            return None
        
        self._counters[counter_id]["value"] += 1
        return CounterRead(**self._counters[counter_id])
    
    def delete(self, counter_id: str) -> bool:
        """删除计数器"""
        if counter_id in self._counters:
            del self._counters[counter_id]
            return True
        return False
