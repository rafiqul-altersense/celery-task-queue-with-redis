from celery import shared_task
import time
import random

@shared_task
def process_file(file_content):
    random_int = random.randint(1000, 2000)
    for i in range(10):
        print(f"ID - {random_int} File Processing - {i}")
        time.sleep(3)
    return {"message": "File processed"}
