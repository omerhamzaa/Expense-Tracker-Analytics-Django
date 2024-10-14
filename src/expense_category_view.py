from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import ExpenseCategory


def get(request):
    expense_category = ExpenseCategory.objects.all()
    data = [{"id": expense_category.id, "expense_category_name": expense_category.name} for expense_category in expense_category]
    return Response(data)


def post(request):
    expense_category = ExpenseCategory.objects.create(**request.data)
    return Response({"id": expense_category.id, "expense_category_name": expense_category.name}, status=status.HTTP_201_CREATED)


def put(request, pk):
    expense_category = get_object_or_404(ExpenseCategory, pk=pk)
    for attr, value in request.data.items():
        setattr(expense_category, attr, value)
    expense_category.save()
    return Response({"id": expense_category.id, "expense_category_name": expense_category.name})


def delete(request, pk):
    expense_category = get_object_or_404(ExpenseCategory, pk=pk)
    expense_category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)