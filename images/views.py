from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from django.http import JsonResponse

# Create your views here.
def index(request):
    # obj = Image.objects.get(pk=3)
    form = ImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'it works'})
    
    context = {'form': form}
    return render(request, 'images/index.html', context)

