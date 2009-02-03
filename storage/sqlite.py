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

import sqlite3
from pycache import PyCache
from storage import storage
from time import time

class SQLite(storage):
    def __init__(self, **kwargs):
        if 'file' in kwargs:
            self.file = kwargs['file']
        else:
            self.file = 'PyCache.db'
        self.conn = sqlite3.connect(self.file)
        self.curs = self.conn.cursor()
        
        if 'table' in kwargs:
            self.table = kwargs['table'] + '_' + PyCache.TABLE
        else:
            self.table = PyCache.TABLE
    
    def create(self):
        self.curs.execute("CREATE TABLE %s (%s VARCHAR(32) PRIMARY KEY, %s TEXT, %s INTEGER)" % (self.table, PyCache.KEY, PyCache.VALUE, PyCache.EXPIRES))
        self.curs.execute("CREATE INDEX %s_%s ON %s (%s)" % (self.table, PyCache.EXPIRES, self.table, PyCache.EXPIRES))
    
    def store(self, key, value, expires):
        self.curs.execute("REPLACE INTO %s (%s, %s, %s) VALUES (?, ?, ?)" % (self.table, PyCache.KEY, PyCache.VALUE, PyCache.EXPIRES), (key, value, expires))
    
    def fetch(self, key):
        self.curs.execute("SELECT %s, %s FROM %s WHERE %s=?" % (PyCache.VALUE, PyCache.EXPIRES, self.table, PyCache.KEY), (key,))
        result = self.curs.fetchone()
        if not result:
            return False
        return {PyCache.VALUE: result[0], PyCache.EXPIRES: int(result[1])}
        
    def expire(self, key):
        self.curs.execute("REPLACE INTO %s (%s, %s) VALUES (?, ?)" % (self.table, PyCache.KEY, PyCache.EXPIRES), (key, time()))
    
    def gc(self):
        self.curs.execute("DELETE FROM %s WHERE %s < ?" % (self.table, PyCache.EXPIRES), (time(),))