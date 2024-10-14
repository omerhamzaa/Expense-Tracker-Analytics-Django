from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import User, Budget, ExpenseCategory


def get_budget(request):
    budgets = Budget.objects.all()
    data = [{
        "id": budget.id,
        "amount": budget.amount,
        "period": budget.period,
        "created_at": budget.created_at,
        "user_id": budget.user_id.id,
        "expense_category": budget.expense_category.id
    } for budget in budgets]
    return Response(data)


def create_budget(request):
    amount = request.data.get('amount')
    period = request.data.get('period')
    user_id = request.data.get('user_id')
    expense_category_id = request.data.get('expense_category')

    # Validate required fields
    if not all([amount, period, user_id, expense_category_id]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if expense category exists
    try:
        expense_category = ExpenseCategory.objects.get(id=expense_category_id)
    except ExpenseCategory.DoesNotExist:
        return Response({"error": "Expense category not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the budget
    budget = Budget.objects.create(
        amount=amount,
        period=period,
        user_id=user,
        expense_category=expense_category
    )

    return Response({
        "id": budget.id,
        "amount": budget.amount,
        "period": budget.period,
        "created_at": budget.created_at,
        "user_id": budget.user_id.id,
        "expense_category": budget.expense_category.id
    }, status=status.HTTP_201_CREATED)


def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)

    for attr, value in request.data.items():
        if attr == "user_id":
            try:
                user = User.objects.get(id=value)
                setattr(budget, "user_id", user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif attr == "expense_category":
            try:
                expense_category = ExpenseCategory.objects.get(id=value)
                setattr(budget, "expense_category", expense_category)
            except ExpenseCategory.DoesNotExist:
                return Response({"error": "Expense category not found"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            setattr(budget, attr, value)

    budget.save()

    return Response({
        "id": budget.id,
        "amount": budget.amount,
        "period": budget.period,
        "created_at": budget.created_at,
        "user_id": budget.user_id.id,
        "expense_category": budget.expense_category.id
    }, status=status.HTTP_200_OK)


def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    budget.delete()
    return Response({"message": "Budget entry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)