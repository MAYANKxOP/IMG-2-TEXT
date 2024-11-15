

# Create your views here.

from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage
import pytesseract
from PIL import Image



# Set the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            # Extract text using pytesseract
            image_path = uploaded_image.image.path
            extracted_text = pytesseract.image_to_string(Image.open(image_path))
            uploaded_image.extracted_text = extracted_text
            uploaded_image.save()
            return redirect('view_image', uploaded_image.id)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def view_image(request, image_id):
    image = UploadedImage.objects.get(id=image_id)
    return render(request, 'view_image.html', {'image': image})

def home(request):
    return redirect('upload_image')