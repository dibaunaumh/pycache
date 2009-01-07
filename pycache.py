from time import time

class PyCache:
    TABLE = 'PyCache'
    KEY = 'PyCache_key'
    VALUE = 'PyCache_value'
    EXPIRES = 'PyCache_expires'
    
    def __init__(self, **kwargs):
        if 'engine' in kwargs:
            self.storage = kwargs['engine'](**kwargs)
        
        #One hour default expiration
        self.default_length = 3600
    
    def create(self):
        self.storage.create()
    
    def gc(self):
        self.storage.gc()
    
    def store(self, key, value, expires):
        self.storage.store(key, value, expires)
    
    def expire(self, key):
        self.storage.expire(key)

    def get(self, key):
        result = self.storage.fetch(key)
        if not result or result[PyCache.EXPIRES] < time():
            return False
        return result[PyCache.VALUE]
    
    def __setitem__(self, key, value):
        self.store(key, value, time() + self.default_length)
    def __getitem__(self, key):
        return self.get(key)
    def __delitem__(self, key):
        return self.storage.expire(key)