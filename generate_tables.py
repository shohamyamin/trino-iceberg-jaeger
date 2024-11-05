import trino
import random
import string

# Trino connection details
host = "localhost"
port = 8080
user = "admin"
catalog = "nessie_catalog"
schema = "example"

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

# Create tables and insert data
for table_num in range(1, 501):
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

    # Generate and insert 10 records
    for _ in range(10):
        values = ", ".join([generate_random_data() for _ in range(10)])
        insert_query = f"INSERT INTO {catalog}.{schema}.{table_name} VALUES ({values})"
        cursor.execute(insert_query)

    print(f"10 records inserted into {table_name}")

print("All tables created with records inserted.")
cursor.close()
conn.close()
