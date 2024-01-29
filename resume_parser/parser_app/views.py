from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm
from django.core.files.base import ContentFile
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
import os
import requests
import uuid

def upload_resume(request):
    if request.method == 'POST':
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()

                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.email              = data.get('email')
                    resume.mobile_number      = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education      = ', '.join(data.get('degree'))
                    else:
                        resume.education      = None
                    resume.company_names      = data.get('company_names')
                    resume.college_name       = data.get('college_name')
                    resume.designation        = data.get('designation')
                    resume.total_experience   = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills         = ', '.join(data.get('skills'))
                    else:
                        resume.skills         = None
                    if data.get('experience') is not None:
                        resume.experience     = ', '.join(data.get('experience'))
                    else:
                        resume.experience     = None
                    resume.save()
                except IntegrityError:
                    return JsonResponse({'error': 'Duplicate resume found'})
            resumes = Resume.objects.all()
            return JsonResponse({'success': 'Resumes uploaded!', 'resumes': resumes_data})
        else:
            return JsonResponse({'error': 'Invalid form data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
# def upload_resume_link(request):
#     if request.method == 'POST':
#         Resume.objects.all().delete()
#         link_form = UploadResumeLinkModelForm(request.POST)
#         links = request.POST.getlist('resume_link')
#         resumes_data = []
#         if link_form.is_valid():
#             for link in links:
#                 try:
#                     # download the file
#                     response = requests.get(link)
#                     if response.status_code == 200:
#                         # save the file
#                         file_name = f"{uuid.uuid4()}.pdf"  # Change '.pdf' to the appropriate file extension
#                         # save the file
#                         file_content = ContentFile(response.content, name=file_name)
#                         resume = Resume(resume=file_content)
#                         resume.save()

#                         # extracting resume entities
#                         parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                        
#                         data = parser.get_extracted_data()
#                         resumes_data.append(data)
#                         resume.name               = data.get('name')
#                         resume.email              = data.get('email')
#                         resume.mobile_number      = data.get('mobile_number')
#                         if data.get('degree') is not None:
#                             resume.education      = ', '.join(data.get('degree'))
#                         else:
#                             resume.education      = None
#                         resume.company_names      = data.get('company_names')
#                         resume.college_name       = data.get('college_name')
#                         resume.designation        = data.get('designation')
#                         resume.total_experience   = data.get('total_experience')
#                         if data.get('skills') is not None:
#                             resume.skills         = ', '.join(data.get('skills'))
#                         else:
#                             resume.skills         = None
#                         if data.get('experience') is not None:
#                             resume.experience     = ', '.join(data.get('experience'))
#                         else:
#                             resume.experience     = None
#                         # ... (Assign other extracted data to corresponding fields in the Resume model)
#                         resume.save()
                        
#                         os.remove(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
#                     else:
#                         return JsonResponse({'error': f'Failed to download file from {link}'})

#                 except IntegrityError:
#                     return JsonResponse({'error': 'Duplicate resume found'})
#             resumes = Resume.objects.all()
#             return JsonResponse({'success': 'Resumes uploaded!', 'resumes': resumes_data})
#         else:
#             return JsonResponse({'error': 'Invalid form data'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})
