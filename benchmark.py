import trino
import time
import matplotlib.pyplot as plt

def benchmark_query(catalog_name, conn):
    query = "select * from " + catalog_name + ".information_schema.columns"
    start_time = time.time()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()
    num_columns = len(result[0])  # Count the number of columns in the first row
    return end_time - start_time, num_columns

def main():
    trino_host = "localhost"  # Replace with your Trino host
    trino_port = 8080  # Replace with your Trino port
    catalogs = ["nessie_catalog", "rest_catalog"]
    results = {}

    for catalog in catalogs:
        conn = trino.dbapi.connect(host=trino_host, port=trino_port,user="admin", catalog=catalog)
        results[catalog] = benchmark_query(catalog, conn)
        conn.close()

    # Create a bar graph
    labels = [f"{catalog} ({results[catalog][1]} columns)" for catalog in catalogs]
    plt.bar(labels, [result[0] for result in results.values()])
    plt.xlabel("Catalog")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Benchmark Results")
    plt.savefig("benchmark_results.png")

if __name__ == "__main__":
    main()