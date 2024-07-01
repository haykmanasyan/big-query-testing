from google.cloud import bigquery

def main():
    client = bigquery.Client()

    # Define dataset and table IDs
    project_id = 'enduring-broker-426815-b2'
    dataset_id = 'test_data'
    table_id = 'test'

    while True:
        print("\nMenu:")
        print("1. Add data")
        print("2. View table")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            add_data(client, project_id, dataset_id, table_id)
        elif choice == '2':
            view_table(client, project_id, dataset_id, table_id)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def add_data(client, project_id, dataset_id, table_id):
    # Fetch table schema
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    table = client.get_table(table_ref)

    name = input("Enter name: ")
    age = int(input("Enter age: "))

    rows_to_insert = [{"name": name, "age": age}]
    errors = client.insert_rows(table, rows_to_insert)

    if not errors:
        print("Data added successfully.")
    else:
        print(f"Encountered errors while inserting data: {errors}")

def view_table(client, project_id, dataset_id, table_id):
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    rows = list(query_job.result())

    print("\nQuery results:")
    if not rows:
        print("No rows found.")
    else:
        for row in rows:
            print(f"Name: {row['name']}, Age: {row['age']}")

if __name__ == "__main__":
    main()
