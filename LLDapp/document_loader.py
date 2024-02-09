# # LLDapp/document_loader.py
# import os
# import docx
# from pyPDF2 import PdfFileReader

# def load_document(file_path):
#     file_extension = os.path.splitext(file_path)[1].lower()

#     if file_extension == '.pdf':
#         return load_pdf(file_path)
#     elif file_extension == '.docx':
#         return load_docx(file_path)
#     else:
#         raise ValueError("Unsupported file format")

# def load_pdf(file_path):
#     with open(file_path, 'rb') as file:
#         reader = PdfFileReader(file)
#         text = ''
#         for page_num in range(reader.numPages):
#             text += reader.getPage(page_num).extractText()
#         return text

# def load_docx(file_path):
#     doc = docx.Document(file_path)
#     text = ''
#     for para in doc.paragraphs:
#         text += para.text + '\n'
#     return text
