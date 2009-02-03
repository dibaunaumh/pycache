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

class storage:
    def create(self): pass
    def store(self, key, value, expires): pass
    def fetch(self, key): pass
    def expire(self, key): pass
    def gc(self): pass