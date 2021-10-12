from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from django.http import JsonResponse
import os, shutil
import glob
import cv2
import pytesseract

# Create your views here.
def index(request):
    # obj = Image.objects.get(pk=3)
    form = ImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
            # get media directory using os
        path = os.getcwd() + "/media/images/*"
        
        for path_to_license_plate in glob.glob(path, recursive=True):
            
            img = cv2.imread(path_to_license_plate)
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'    
            pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'    
            predicted_result = pytesseract.image_to_string(img, lang='eng',config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            
            filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
            
            context = { 'filter_predicted_result' : filter_predicted_result }
            
        delete()
      
        return JsonResponse({'message': 'it works', 'context' : context})
    context = {'form': form}
    return render(request, 'images/index.html', context)

def delete(): 
    folder = os.getcwd() + '/media/images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    