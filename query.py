from google.cloud import bigquery

def main():
    client = bigquery.Client()

    # define dataset and table IDs

    project_id = 'enduring-broker-426815-b2'
    dataset_id = 'test_data'
    table_id = 'test'

    # simple menu
    # options for add data, view the table, or quit

    while True:

        print("\nMenu:")
        print("1. Add data")
        print("2. View table")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        # pass in relevant info
        # break if quit
        # catch invalid option

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

    # fetch table
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    table = client.get_table(table_ref)

    # grab input
    # table schema 1: name (STRING)
    # table schema 2: age (INTEGER)

    name = input("Enter name: ")
    age = int(input("Enter age: "))
    
    # set up row to insert from input
    rows_to_insert = [{"name": name, "age": age}]
    errors = client.insert_rows(table, rows_to_insert)

    # check for an error
    if not errors:

        print("Data added successfully.")
    else:

        print(f"Encountered errors while inserting data: {errors}")

def view_table(client, project_id, dataset_id, table_id):

    # reference the table
    # create a new query job
    # grab each row from the query job

    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    rows = list(query_job.result())

    # check if the table is empty
    # if not, list the name and age from the table
    print("\nQuery results:")
    if not rows:
        print("No rows found.")
    else:
        for row in rows:
            print(f"Name: {row['name']}, Age: {row['age']}")

if __name__ == "__main__":
    main()
