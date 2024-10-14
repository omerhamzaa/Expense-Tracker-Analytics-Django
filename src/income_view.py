from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import Income, User, IncomeCategory


def get_income(request):
    incomes = Income.objects.all()
    data = [
        {
            "id": income.id,
            "amount": income.amount,
            "description": income.description,
            "date": income.date,
            "user_id": income.user_id.id,  # Assuming user_id is a ForeignKey
            "income_category": income.income_category.id  # Assuming income_category is a ForeignKey
        }
        for income in incomes
    ]
    return Response(data)


def create_income(request):
    amount = request.data.get('amount')
    description = request.data.get('description')
    user_id = request.data.get('user_id')
    income_category_id = request.data.get('income_category')

    # Get the User instance
    user = get_object_or_404(User, id=user_id)

    # Get the IncomeCategory instance
    income_category = get_object_or_404(IncomeCategory, id=income_category_id)

    # Create the Income instance
    income = Income.objects.create(
        amount=amount,
        description=description,
        user_id=user,  # Assign the User instance
        income_category=income_category  # Assign the IncomeCategory instance
    )

    return Response({
        "id": income.id,
        "amount": income.amount,
        "description": income.description,
        "date": income.date,
        "user_id": income.user_id.id,  # Return the user ID
        "income_category": income.income_category.id  # Return the income category ID
    }, status=status.HTTP_201_CREATED)


def put_income(request, pk):
    income = get_object_or_404(Income, pk=pk)

    # Loop through request data and update fields
    for attr, value in request.data.items():
        if attr == "user_id":
            user = get_object_or_404(User, id=value)
            income.user_id = user  # Assign the User instance
        elif attr == "income_category":
            income_category = get_object_or_404(IncomeCategory, id=value)
            income.income_category = income_category  # Assign the IncomeCategory instance
        else:
            setattr(income, attr, value)

    # Save the updated income instance
    income.save()

    return Response({
        "id": income.id,
        "amount": income.amount,
        "description": income.description,
        "date": income.date,
        "user_id": income.user_id.id,
        "income_category": income.income_category.id
    }, status=status.HTTP_200_OK)


def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return Response({"message": "Income entry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)