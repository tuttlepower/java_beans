from django.http import JsonResponse
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


@api_view(['GET', 'POST', 'PUT'])
def todo_list(request):

    # Get all
    if request.method == 'GET':
        todos = Todo.objects.all()
        serialized = TodoSerializer(todos, many=True)
        return JsonResponse(serialized.data, safe=False)

    # PUT with body {name: 'cleaning'}
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # PUT with body {'id':1}. Flips completed bool.
    if request.method == 'PUT':
        try:
            body = request.body.decode('utf-8')
            body = json.loads(body)['id']
            todo = Todo.objects.get(id=body)
            current = todo.completed
            todo.completed = not current
            todo.save()
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
