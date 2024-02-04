import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CombinedForm, QuestionForm, UploadFileForm
from .llm import process_uploaded_file, answer_question


def hello_world(request):
    return HttpResponse("Hello, World!")

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
    process_uploaded_file(file_path)        

# def answer_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.cleaned_data['question']

#             # Dummy logic to generate an answer
#             dummy_answer = f"Dummy answer to the question: '{question}'"

#             return render(request, 'answer_question.html', {'question': question, 'dummy_answer': dummy_answer})
#     else:
#         form = QuestionForm()

#     return render(request, 'ask_question.html', {'form': form})

def combined_view(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            handle_uploaded_file(request.FILES['file'])

            # Get the question
            question = form.cleaned_data['question']

            # Dummy logic to generate an answer
            dummy_answer = answer_question(question)

            return render(request, 'combined_result.html', {'question': question, 'dummy_answer': dummy_answer})
    else:
        form = CombinedForm()

    return render(request, 'combined_form.html', {'form': form})