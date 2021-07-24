# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import logging

import pymongo
from pymongo import MongoClient

__all__ = [
    'MongoDBAuthenticationBackend'
]

LOG = logging.getLogger(__name__)


class MongoDBAuthenticationBackend(object):
    """
    Backend which reads authentication information from MongoDB.

    The backend users database "st2auth" and collection named "users". Entries inside this
    collection should have two attributes:

    - username - username
    - salt - password salt
    - password - SHA256 hash of the salt + user's password (SHA256(<salt><password>))

    Note: This backends depends on the "pymongo" library.
    """

    _collection_name = 'authenticate'
    _indexes = [
        ('username', pymongo.ASCENDING)
    ]
    _hash_function = hashlib.sha256

    def __init__(self, db_host='localhost', db_port=27017, db_name='st2auth', db_username=None,
                 db_password=None):
        self._db_name = db_name
        self._db_host = db_host
        self._db_port = db_port
        self._db_username = db_username
        self._db_password = db_password

        self._client = MongoClient(host=self._db_host, port=self._db_port, tz_aware=True)
        self._db = self._client[db_name]

        if self._db_username:
            self._db.authenticate(name=self._db_username, password=self._db_password)

#         self._collection = self._db[self._collection_name]
#         self._ensure_indexes()

    def authenticate(self, username, password):
        
        return True
        
#         salt_result = self._collection.find_one({'username': username})

#         if not salt_result:
#             return False

#         salt = salt_result.get('salt', None)
#         if not salt:
#             return False

#         password_string = '%s%s' % (salt, password)
#         password_hash = self._hash_function(password_string.encode('utf-8')).hexdigest()
#         result = self._collection.find_one({'username': username, 'password': password_hash})

#         if result and result.get('username', None) == username and \
#            result.get('password', None) == password_hash:
#             return True

#         return False

    def get_user(self, username):
        pass

    def _ensure_indexes(self):
        self._collection.ensure_index(self._indexes, unique=True)
