from google.cloud import bigquery

# initialize the BigQuery client
client = bigquery.Client()

# define the dataset and table
dataset_id = 'enduring-broker-426815-b2.test_data'
table_id = 'test'

# construct a reference to the dataset and table
dataset_ref = client.dataset('test_data')
table_ref = dataset_ref.table('test')

# fetch the table
table = client.get_table(table_ref)

# print the table schema
print(f"Table {table_id} in dataset {dataset_id} schema:")
for schema_field in table.schema:
    print(f"  - {schema_field.name} ({schema_field.field_type})")

# query the table
query = f"SELECT * FROM `{dataset_id}.{table_id}`"
query_job = client.query(query)

# fetch the results
rows = list(query_job.result())

# print the results
print("Query results:")
if not rows:
    print("No rows found.")
else:
    for row in rows:
        print(row)