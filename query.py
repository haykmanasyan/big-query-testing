from google.cloud import bigquery
from datetime import datetime
import time

def main():
    client = bigquery.Client()

    # Define dataset and table IDs
    project_id = 'enduring-broker-426815-b2'
    dataset_id = 'test_data'
    table_id = 'test2'

    # Simple menu
    while True:
        print("\nMenu:")
        print("1. Add data")
        print("2. View table")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            add_data(client, project_id, dataset_id, table_id)
        elif choice == '2':
            try:
                view_table(client, project_id, dataset_id, table_id)
            except Exception as e:
                print(f"Error viewing table: {e}")
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def add_data(client, project_id, dataset_id, table_id):
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    table = client.get_table(table_ref)

    # Prompt for input
    volume = int(input("Enter volume (integer): "))

    # Prepare rows to insert
    rows_to_insert = [{"time": datetime.utcnow(), "volume": volume}]
    errors = client.insert_rows(table, rows_to_insert)

    if not errors:
        print("Data added successfully.")
    else:
        print(f"Encountered errors while inserting data: {errors}")

    # Introduce a short delay before querying to allow for data availability
    time.sleep(1)

def view_table(client, project_id, dataset_id, table_id):
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    
    # Check if table exists
    try:
        table = client.get_table(table_ref)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch table {dataset_id}.{table_id}: {e}")
        
    # Query table
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    rows = list(query_job.result())

    print("\nQuery results:")
    if not rows:
        print("No rows found.")
    else:
        for row in rows:
            print(f"Timestamp: {row['time']}, Volume: {row['volume']}")

if __name__ == "__main__":
    main()
