__name__ = 'PyCache'
__version__ = '0.2.0'
__description__ = 'A simple caching mechanism'
__author__ = 'Jake Wharton'
__author_email__ = 'JakeWharton@GMail.com'
__url__ = 'http://mine.jakewharton.com/projects/show/pycache'
__revision__ = "$Rev$"[6:-2]
__license__ = '''
Copyright 2009 Jake Wharton

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

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