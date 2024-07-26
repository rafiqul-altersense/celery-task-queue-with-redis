from flask import Flask, request, jsonify
from celery import Celery
import os
from celery import shared_task
import time
import random

app = Flask(__name__)
app.config['broker_url'] = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
app.config['result_backend'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(result_backend=app.config['result_backend'])


# @shared_task(ignore_result=False)
@celery.task
def process_file(file_content):
    random_int = random.randint(1000, 2000)
    for i in range(10):
        print(f"ID - {random_int} File Processing - {i}")
        time.sleep(3)
    return {"message": "File processed"}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    task = process_file.delay(file.read())
    return jsonify({"task_id": task.id}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
