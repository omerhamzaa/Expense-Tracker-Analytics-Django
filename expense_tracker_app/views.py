from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Income, IncomeCategory, Expense, ExpenseCategory, BudgetAlert, Budget


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email, "date": user.date} for user in users]
        return Response(data)

    def post(self, request):
        user = User.objects.create(**request.data)
        return Response({"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email, "date": user.date}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        for attr, value in request.data.items():
            setattr(user, attr, value)
        user.save()
        return Response({"id": user.id, "name": user.name, "contact_number": user.contact_number, "email": user.email, "date": user.date})

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeView(APIView):
    def get(self, request):
        incomes = Income.objects.all()
        data = [{"id": income.id, "amount": income.amount, "description": income.description, "date": income.date, "user_id": income.user_id, "income_category": income.income_category} for income in incomes]
        return Response(data)

    def post(self, request):

        amount = request.data.get('amount')
        description = request.data.get('description')
        user_id = request.data.get('user_id')
        income_category_id = request.data.get('income_category')

        # Get the User instance
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the IncomeCategory instance
        try:
            income_category = IncomeCategory.objects.get(id=income_category_id)
        except IncomeCategory.DoesNotExist:
            return Response({"error": "Income category not found"}, status=status.HTTP_400_BAD_REQUEST)

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



    def put(self, request, pk):

        income = get_object_or_404(Income, pk=pk)

        # Loop through request data and update fields
        for attr, value in request.data.items():
            # Handle ForeignKey for user_id
            if attr == "user_id":
                try:
                    user = User.objects.get(id=value)
                    setattr(income, "user_id", user)  # Assign the User instance
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Handle ForeignKey for income_category
            elif attr == "income_category":
                try:
                    income_category = IncomeCategory.objects.get(id=value)
                    setattr(income, "income_category", income_category)
                except IncomeCategory.DoesNotExist:
                    return Response({"error": "Income category not found"}, status=status.HTTP_400_BAD_REQUEST)

            # For other attributes, directly set them
            else:
                setattr(income, attr, value)

        # Save the updated income instance
        income.save()

        # Return the updated response
        return Response({
            "id": income.id,
            "amount": income.amount,
            "description": income.description,
            "date": income.date,
            "user_id": income.user_id.id,
            "income_category": income.income_category.id
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        income = get_object_or_404(Income, pk=pk)
        income.delete()
        return Response({"message": "Income entry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class IncomeCategoryView(APIView):
    def get(self, request):
        income_category = IncomeCategory.objects.all()
        data = [{"id": income_category.id, "income_category_name": income_category.name} for income_category in income_category]
        return Response(data)

    def post(self, request):
        income_category = IncomeCategory.objects.create(**request.data)
        return Response({"id": income_category.id, "income_category_name": income_category.name}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        income_category = get_object_or_404(IncomeCategory, pk=pk)
        for attr, value in request.data.items():
            setattr(income_category, attr, value)
        income_category.save()
        return Response({"id": income_category.id, "income_category_name": income_category.name})

    def delete(self, request, pk):
        income_category = get_object_or_404(IncomeCategory, pk=pk)
        income_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExpenseCategoryView(APIView):
    def get(self, request):
        expense_category = ExpenseCategory.objects.all()
        data = [{"id": expense_category.id, "expense_category_name": expense_category.name} for expense_category in expense_category]
        return Response(data)

    def post(self, request):
        expense_category = ExpenseCategory.objects.create(**request.data)
        return Response({"id": expense_category.id, "expense_category_name": expense_category.name}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, pk=pk)
        for attr, value in request.data.items():
            setattr(expense_category, attr, value)
        expense_category.save()
        return Response({"id": expense_category.id, "expense_category_name": expense_category.name})

    def delete(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, pk=pk)
        expense_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseView(APIView):
    def get(self, request):
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


    def post(self, request):
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



    def put(self, request, pk):
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

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response({"message": "Expense entry deleted successfully"}, status=status.HTTP_204_NO_CONTENT)