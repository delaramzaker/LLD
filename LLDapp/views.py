import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CombinedForm, UploadFileForm
from .llm import process_uploaded_file, answer_question

def hello_world(request):
    return HttpResponse("Hello, World!")

def news(request):
    return render(request, 'news.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def PWS_world(request):
    return render(request, 'PWS_world.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('File uploaded successfully!')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def handle_uploaded_file(file):
    file_path = os.path.join('uploads', file.name)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    if file.name.endswith('.doc'):
        # Handle .doc file processing
        process_doc_file(file_path)
    elif file.name.endswith('.pdf'):
        # Handle PDF file processing
        process_pdf_file(file_path)
    else:
        # Handle other file types (e.g., text files)
        process_uploaded_file(file_path)

def process_doc_file(file_path):
    # Logic to process .doc files
    pass

def process_pdf_file(file_path):
    # Logic to process PDF files
    pass

def combined_view(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            question = form.cleaned_data['question']
            dummy_answer = answer_question(question)
            return render(request, 'combined_result.html', {'question': question, 'dummy_answer': dummy_answer})
    else:
        form = CombinedForm()
    return render(request, 'combined_form.html', {'form': form})
