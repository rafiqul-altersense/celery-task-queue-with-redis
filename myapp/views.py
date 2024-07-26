from django.http import JsonResponse
from .tasks import process_file
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        task = process_file.delay(file.read())
        return JsonResponse({"task_id": task.id}, status=202)
    return JsonResponse({"error": "No file part"}, status=400)
