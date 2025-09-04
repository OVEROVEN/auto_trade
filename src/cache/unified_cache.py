"""統一快取系統"""

import time
from typing import Dict, Any, Optional

class UnifiedCache:
    """統一的快取管理系統"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, tuple] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """獲取快取數據"""
        if key in self.cache:
            timestamp, data = self.cache[key]
            if time.time() - timestamp < self.default_ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """設置快取數據"""
        self.cache[key] = (time.time(), data)
    
    def delete(self, key: str) -> bool:
        """刪除快取項目"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """清除所有快取"""
        self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """獲取快取統計"""
        current_time = time.time()
        valid_items = 0
        expired_items = 0
        
        for timestamp, _ in self.cache.values():
            if current_time - timestamp < self.default_ttl:
                valid_items += 1
            else:
                expired_items += 1
        
        return {
            "total_items": len(self.cache),
            "valid_items": valid_items,
            "expired_items": expired_items,
            "cache_size_mb": len(str(self.cache)) / (1024 * 1024)
        }

# 全局快取實例
_cache_instance = None

def get_cache() -> UnifiedCache:
    """獲取全局快取實例"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = UnifiedCache()
    return _cache_instance