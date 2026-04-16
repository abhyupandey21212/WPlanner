# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:27:20 2026

@author: abhyu
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://abhyupandey21212_db_user:tc6XUA5PLpexwoJQ@wplanner.pq6idpt.mongodb.net/?appName=WPlanner"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))