import json
from django.db import reset_queries
from django.http import response
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TeacherSerializer, QuestionSerializer
from .models import Teacher, Question
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .functions.index import calculateNDaysAgo

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data

@api_view(['GET', 'POST', 'DELETE'])
def getAllTeachers(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            teachers = teachers.filter(title__icontains=title)
        
        serializer_class = TeacherSerializer(teachers, many=True)
        return JsonResponse(serializer_class.data, safe=False)
        # 'safe=False' for objects serialization

@api_view(['GET', 'POST', 'DELETE'])
def questionsList(request):
    if request.method == 'GET':
        questions = list(Question.objects.all().order_by('createdAt'))
        
        serializer_class = QuestionSerializer(questions, many=True)
        dict = serializer_class.data
        res = []
        for element in dict:
            element = json.loads(json.dumps(element))
            element["nDaysAgo"] = calculateNDaysAgo(element.get('createdAt'))
            res.append(element)
            
        return JsonResponse(res, safe=False)
    
    elif request.method == 'POST':
        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializer(data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JsonResponse(question_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST', 'DELETE'])
def questionDetail(request, id):
    if request.method == 'GET':
        question = Question.objects.get(id=id)
        question_serializer = QuestionSerializer(question) 
        dict = question_serializer.data
        res = []
        element = json.loads(json.dumps(dict))
        element["askedDate"] = calculateNDaysAgo(element.get('createdAt'))
        res.append(element)
        return JsonResponse(res, safe=False) 
            