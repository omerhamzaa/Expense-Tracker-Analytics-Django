from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import Expense, User, ExpenseCategory


def get(request):
    expenses = Expense.objects.all()
    data = [{
        "id": expense.id,
        "amount": expense.amount,
        "description": expense.description,
        "date": expense.date,
        "user_id": expense.user_id.id,
        "expense_category": expense.expense_category.id
    } for expense in expenses]
    return Response(data)


def post(request):
    amount = request.data.get('amount')
    description = request.data.get('description')
    user_id = request.data.get('user_id')
    expense_category_id = request.data.get('expense_category')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        expense_category = ExpenseCategory.objects.get(id=expense_category_id)
    except ExpenseCategory.DoesNotExist:
        return Response({"error": "Expense category not found"}, status=status.HTTP_400_BAD_REQUEST)


    expense = Expense.objects.create(
        amount=amount,
        description=description,
        user_id=user,  # Assign the User instance
        expense_category=expense_category  # Assign the ExpenseCategory instance
    )

    return Response({
        "id": expense.id,
        "amount": expense.amount,
        "description": expense.description,
        "date": expense.date,
        "user_id": expense.user_id.id,
        "expense_category": expense.expense_category.id
    }, status=status.HTTP_201_CREATED)


def put(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    for attr, value in request.data.items():
        if attr == "user_id":
            try:
                user = User.objects.get(id=value)
                setattr(expense, "user_id", user)  # Assign the User instance
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif attr == "expense_category":
            try:
                expense_category = ExpenseCategory.objects.get(id=value)
                setattr(expense, "expense_category", expense_category)
            except ExpenseCategory.DoesNotExist:
                return Response({"error": "Expense category not found"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            setattr(expense, attr, value)

    expense.save()

    return Response({
        "id": expense.id,
        "amount": expense.amount,
        "description": expense.description,
        "date": expense.date,
        "user_id": expense.user_id.id,
        "expense_category": expense.expense_category.id
    }, status=status.HTTP_200_OK)


def delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return Response({"message": "Expense entry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
