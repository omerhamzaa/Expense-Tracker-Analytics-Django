from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import IncomeCategory


def get_income_category(request):
    income_category = IncomeCategory.objects.all()
    data = [{"id": income_category.id, "income_category_name": income_category.name} for income_category in
            income_category]
    return Response(data)


def create_income_category(request):
    income_category = IncomeCategory.objects.create(**request.data)
    return Response({"id": income_category.id, "income_category_name": income_category.name},
                    status=status.HTTP_201_CREATED)


def update_income_category(request, pk):
    income_category = get_object_or_404(IncomeCategory, pk=pk)
    for attr, value in request.data.items():
        setattr(income_category, attr, value)
    income_category.save()
    return Response({"id": income_category.id, "income_category_name": income_category.name})


def delete_income_category(request, pk):
    income_category = get_object_or_404(IncomeCategory, pk=pk)
    income_category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
