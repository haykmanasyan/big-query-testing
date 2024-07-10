from flask import Flask, render_template, jsonify
from google.cloud import bigquery
import datetime

app = Flask(__name__)

# Initialize BigQuery client
client = bigquery.Client()
project_id = 'enduring-broker-426815-b2'
dataset_id = 'test_data'
table_id = 'test2'

# Function to fetch data from BigQuery
def fetch_data(client, project_id, dataset_id, table_id):
    table_ref = client.dataset(dataset_id, project=project_id).table(table_id)
    
    try:
        table = client.get_table(table_ref)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch table {dataset_id}.{table_id}: {e}")
        
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    rows = list(query_job.result())
    
    return rows

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get data as JSON
@app.route('/data')
def data():
    try:
        rows = fetch_data(client, project_id, dataset_id, table_id)
        print("Fetched rows:", rows)  # Debugging statement
    except Exception as e:
        return jsonify({"error": str(e)})

    # Convert timestamps to ISO format
    data = [{"time": row['time'].isoformat(), "volume": row['volume']} for row in rows]
    print("Formatted data:", data)  # Debugging statement
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
