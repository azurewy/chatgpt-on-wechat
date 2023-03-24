import time
from datetime import datetime, timedelta

class ExpiredDict(dict):
    def __init__(self, expires_in_seconds):
        super().__init__()
        self.expires_in_seconds = expires_in_seconds

    def __getitem__(self, key):
        value, expiry_time = super().__getitem__(key)
        # 如果元素已过期，则从字典中删除该元素并抛出 KeyError 异常
        if time.monotonic() > expiry_time:
            del self[key]
            raise KeyError("expired {}".format(key))
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        expiry_time = datetime.now() + timedelta(seconds=self.expires_in_seconds)
        super().__setitem__(key, (value, expiry_time))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False
        
    def keys(self):
        keys=list(super().keys())
        return [key for key in keys if key in self]
    
    def items(self):
        return [(key, self[key]) for key in self.keys()]
    
    def __iter__(self):
        return self.keys().__iter__()