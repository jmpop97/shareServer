from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os

# Create your views here.
class FileUploader(APIView):
    def get(self, request):
        # The request object is used to handle the incoming HTTP request
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            files = os.listdir(media_path)
            return Response({'files': files}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Media directory not found'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
        print("post")
        files = request.FILES.getlist('files')
        print(files)
        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        media_path = settings.MEDIA_ROOT
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        uploaded_files = []
        for file in files:
            file_path = os.path.join(media_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            uploaded_files.append(file.name)
        return Response("Test")

        # return Response({'message': 'Files uploaded successfully', 'files': uploaded_files}, status=status.HTTP_201_CREATED)