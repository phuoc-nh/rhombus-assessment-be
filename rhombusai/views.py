from django.shortcuts import render
from django.http import HttpResponse
from .models import ExampleModel
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import FileTypeModel

import pandas as pd
from .infer_data_types import infer_and_convert_data_types

from django.conf import settings

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            
            # Save file to the "files" folder
            file_path = os.path.join(file.name)
            path = default_storage.save(file_path, ContentFile(file.read()))
            
            # Save the file path to the database
            fileEntity = FileTypeModel(file=path)
            fileEntity.save()

            return Response({"id": fileEntity.id, "success": "true"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        file = FileTypeModel.objects.get(id=request.GET['file_id'])
        limit = int(request.GET.get('limit', 10))
        page = int(request.GET.get('page', 1))
        
        print('limit', limit)
        print('page', page)
        
        media_root = settings.MEDIA_ROOT
        absolute_path = os.path.join(media_root, file.file)
        df = pd.read_csv(absolute_path)
        total_pages = len(df) // limit + 1
        df = df.iloc[(page-1)*limit:page*limit]
        
        df = infer_and_convert_data_types(df)
        inferred_types = {} 
        for col in df.columns:
            case = {
				"int64": "integer",
				"float64": "number",
				"datetime64[ns]": "dateTime",
				"category": "category",
				"object": "text",
                "bool": "boolean"
			}
            if str(df[col].dtype) in case:
                inferred_types[col] = case[str(df[col].dtype)]
            
        # if file has custom types, override the inferred types
        if file.type:
            inferred_types = file.type
        # otherwise, save inferred types to the database
        else:
            file.type = inferred_types
            file.save()
            
        data = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            # Convert Timestamp objects to strings
            for key, value in row_dict.items():
                if isinstance(value, pd.Timestamp):
                    row_dict[key] = value.isoformat()
                elif value is pd.NaT:
                    row_dict[key] = 'NaT'
            data.append(row_dict)
        
        return Response(
            {
           		"file_id": file.id,
				"data": json.dumps(data),
				"types": inferred_types,
				"page": page,
				"limit": limit,
				"total_pages": total_pages
            },
			status=status.HTTP_200_OK
		)

    def put(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        file_id = body['file_id']
        types = body['types']
            
        entity = FileTypeModel.objects.get(id=file_id)
        entity.type = types
        entity.save()
        
        return Response({"success": "true"}, status=status.HTTP_200_OK)
def index(request):
    examples = ExampleModel.objects.all()
    # for example in examples:
    #     print('>>>', example.name)
    return HttpResponse('Hello World')