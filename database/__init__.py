import os
from .graph_db import GraphDatabaseService


db = GraphDatabaseService(os.getenv('NEO4J_DB_URI'))
