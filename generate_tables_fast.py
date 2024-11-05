import trino
import random
import string
from concurrent.futures import ThreadPoolExecutor
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Trino Table Creation Script')
parser.add_argument('--catalog', required=True, help='The Trino catalog name to use')
parser.add_argument('--num_tables', type=int, required=True, help='The number of tables to create')
args = parser.parse_args()

# Trino connection details
host = "localhost"
port = 8081
user = "admin"
catalog = args.catalog  # Get catalog from command-line argument
schema = "example"
num_tables = args.num_tables  # Get number of tables from command-line argument

# Trino connection
conn = trino.dbapi.connect(
    host=host,
    port=port,
    user=user,
    catalog=catalog,
    schema=schema
)
cursor = conn.cursor()

# Create schema if not exists
create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}"
cursor.execute(create_schema_query)
print(f"Schema {schema} checked/created.")

# Function to generate random column names
def generate_columns(n):
    return [f"col_{i}" for i in range(n)]

# Function to generate random string data for each row
def generate_random_data():
    return "'" + ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + "'"

# Function to create a table and insert data
def create_and_populate_table(table_num):
    table_name = f"table_{table_num}"

    # Generate column names and types
    columns = generate_columns(10)
    columns_with_types = ", ".join([f"{col} VARCHAR" for col in columns])

    # Create table query
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {catalog}.{schema}.{table_name} (
        {columns_with_types}
    )
    """
    cursor.execute(create_table_query)
    print(f"Table {table_name} created.")

    # Uncomment to insert 10 records
    # for _ in range(10):
    #     values = ", ".join([generate_random_data() for _ in range(10)])
    #     insert_query = f"INSERT INTO {catalog}.{schema}.{table_name} VALUES ({values})"
    #     cursor.execute(insert_query)

    # print(f"10 records inserted into {table_name}")

# Create a ThreadPoolExecutor to manage concurrent tasks
with ThreadPoolExecutor(max_workers=20) as executor:
    # Submit tasks to the executor
    for table_num in range(1, num_tables + 1):
        executor.submit(create_and_populate_table, table_num)

print("All tables created with records inserted.")
cursor.close()
conn.close()
