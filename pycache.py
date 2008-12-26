import sqlite3
from time import time

class PyCache:
    def __init__(self, **kwargs):
        if 'file' in kwargs:
            self.file = kwargs['file']
        else:
            self.file = 'PyCache.db'
        self.conn = sqlite3.connect(self.file)
        self.curs = self.conn.cursor()
        
        if 'table' in kwargs:
            self.table = kwargs['table'] + '_PyCache'
        else:
            self.table = 'PyCache'
        
        #One hour default expiration
        self.default_length = 3600
    
    def create_table(self):
        self.curs.execute("CREATE TABLE %s (PyCache_key VARCHAR(32) PRIMARY KEY, PyCache_value TEXT, PyCache_expires INTEGER)" % self.table)
        self.curs.execute("CREATE INDEX %s_PyCache_expires ON %s (PyCache_expires)" % (self.table, self.table))
    
    def store(self, key, value, expires):
        self.curs.execute("REPLACE INTO %s (PyCache_key, PyCache_value, PyCache_expires) VALUES (?, ?, ?)" % self.table, (key, value, expires))

    def get(self, key):
        count = self.curs.execute("SELECT PyCache_value, PyCache_expires FROM %s WHERE PyCache_key=?" % self.table, (key,))
        if count == 0:
            return False
        
        result = self.curs.fetchone()
        if int(result[1]) < time():
            return False
        return result[0]
    
    def expire(self, key):
        self.curs.execute("REPLACE INTO %s (PyCache_key, PyCache_value) VALUES (?, ?)" % self.table, (key, time()))
    
    def __setitem__(self, key, value):
        self.store(key, value, time() + self.default_length)
    def __getitem__(self, key):
        return self.get(key)
    def __delitem__(self , key):
        return self.expire(key)

    def gc(self):
        self.curs.execute("DELETE FROM %s WHERE PyCache_expires < ?" % self.table (time(),))