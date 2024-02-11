import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CombinedForm, UploadFileForm, UploadFileForm
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
    print(1)
    if request.method == 'POST':
        print(2)
        form = UploadFileForm(request.POST, request.FILES)
        print(3)
        if form.is_valid():
            print(4)
            qa = handle_uploaded_file(request.FILES['file'])
            print(5)
            request.session['qa'] = qa
            print("qa is None:")
            print(qa is None)
            return HttpResponse('File uploaded successfully!')
    else:
        form = UploadFileForm()
    return render(request, 'about.html', {'form': form})

def handle_uploaded_file(request):
    file = request.FILES['file']
    file_path = os.path.join('uploads', file.name)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # Handle other file types (e.g., text files)
    return process_uploaded_file(file_path)
    
def combined_view(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST, request.FILES)
        if form.is_valid():
            qa = handle_uploaded_file(request)
            # question = form.cleaned_data['question']
            question = request.POST.get('question', '')
            answer = answer_question(qa, question)
            return render(request, 'combined_form.html', {'question': question, 'answer': answer})
    #changed from combined_results.html to combined_form.html
    else:
        form = UploadFileForm()
    return render(request, 'combined_form.html', {'form': form})
