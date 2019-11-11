import os
from dotenv import load_dotenv
from pathlib import Path


user = 'postgres'
password = '123'
host = 'localhost'
database = 'twitter'
port = '5432'
SQLALCHEMY_DATABASE_URI_TEST = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'