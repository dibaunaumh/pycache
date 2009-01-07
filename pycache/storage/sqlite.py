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