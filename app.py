from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/objects', methods=['POST'])
def list_objects():
    access_key = request.form['access_key']
    secret_access_key = request.form['secret_access_key']
    bucket_name = request.form['bucket_name']

    # Authenticate with AWS
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )
    s3_client = session.client('s3')

    # List objects in S3 bucket
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
    except Exception as e:
        return f"Error listing objects: {str(e)}"

    return render_template('objects.html', objects=objects, bucket_name=bucket_name)
    

@app.route('/logs', methods=['POST'])
def display_logs():
    access_key = request.form['access_key']
    secret_access_key = request.form['secret_access_key']
    bucket_name = request.form['bucket_name']
    object_key = request.form['object_key']

    # Authenticate with AWS
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )
    s3_client = session.client('s3')

    # Retrieve logs from S3 object
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        logs = response['Body'].read().decode('utf-8')
    except Exception as e:
        logs = f"Error retrieving logs: {str(e)}"

    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)