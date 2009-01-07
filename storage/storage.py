class storage:
    def create(self): pass
    def store(self, key, value, expires): pass
    def fetch(self, key): pass
    def expire(self, key): pass
    def gc(self): pass