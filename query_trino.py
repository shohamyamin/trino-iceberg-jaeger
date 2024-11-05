import trino
import random
import string
from concurrent.futures import ThreadPoolExecutor
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Trino Table Creation Script')
parser.add_argument('--catalog', required=True, help='The Trino catalog name to use')
args = parser.parse_args()

# Trino connection details
host = "localhost"
user = "admin"
catalog = args.catalog  # Get catalog from command-line argument
schema = "example"

# Trino connection
conn = trino.dbapi.connect(
    host=host,
    port=8080,
    user=user,
    catalog=catalog,
    schema=schema
)
cursor = conn.cursor()

# Create schema if not exists
get_all_columns = f"select * from {catalog}.information_schema.columns"
cursor.execute(get_all_columns)
results = cursor.fetchall()


# Trino connection
conn = trino.dbapi.connect(
    host=host,
    port=8081,
    user=user,
    catalog=catalog,
    schema=schema
)
cursor = conn.cursor()

# Create schema if not exists
get_all_columns = f"select * from {catalog}.information_schema.columns"
cursor.execute(get_all_columns)
results = cursor.fetchall()
