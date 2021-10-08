from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from django.http import JsonResponse, HttpResponse
import os
import glob
import cv2
import pytesseract

# Create your views here.
def index(request):
    # obj = Image.objects.get(pk=3)
    form = ImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'it works'})
    
    context = {'form': form}
    return render(request, 'images/index.html', context)

def toText(request):
    # get media directory using os
    path_for_license_plates = os.getcwd() + "/media/images/*"
    list_license_plates = []
    predicted_license_plates = []
    
    for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):
        
        # get the first file name including .jpg
        license_plate_file = path_to_license_plate.split("/")[-1]
        #splits the image name and .jpg file extension into two separate entities license_plate, _
        license_plate, _ = os.path.splitext(license_plate_file)
        
        list_license_plates.append(license_plate)
        
        img = cv2.imread(path_to_license_plate)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'    
        # pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'    
        predicted_result = pytesseract.image_to_string(img_rgb, lang='eng',config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        
        filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
        predicted_license_plates.append(filter_predicted_result)
        
        return HttpResponse(predicted_license_plates)
