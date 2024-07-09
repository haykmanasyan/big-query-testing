from flask import Flask, render_template
from google.cloud import bigquery
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Initialize Flask app
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
    try:
        rows = fetch_data(client, project_id, dataset_id, table_id)
    except Exception as e:
        return f"Error fetching data: {e}"
    
    timestamps = [row['time'] for row in rows]
    volumes = [row['volume'] for row in rows]
    
    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, volumes, marker='o', linestyle='-', color='b')
    plt.title('Volume vs Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
