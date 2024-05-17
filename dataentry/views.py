from django.conf import settings
from django.shortcuts import redirect, render
from . utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.contrib import messages
from .tasks import import_data_task

def import_data(request):
    if request.method == 'POST':
        file_path =request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        print('file_path=>', file_path)
        print('model_name=>', model_name)

        upload = Upload.objects.create(file = file_path, model_name = model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        
        file_path = base_url + relative_path


        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        import_data_task.delay(file_path, model_name)
        
        messages.success(request, 'Your data is being imported, once it is done you will be notified.')

        
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importdata.html', context)
