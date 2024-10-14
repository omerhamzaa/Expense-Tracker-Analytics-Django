from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import User


def get_users(request):
    users = User.objects.all()
    data = [{"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email,
             "date": user.date} for user in users]
    return Response(data)

def create_user(request):
    user = User.objects.create(**request.data)
    return Response({"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email,
                     "date": user.date}, status=status.HTTP_201_CREATED)


def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    for attr, value in request.data.items():
        setattr(user, attr, value)
    user.save()
    return Response({"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email,
                     "date": user.date})


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)