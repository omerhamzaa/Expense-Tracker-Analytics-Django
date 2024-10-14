from rest_framework.views import APIView
from src.user_view import get_users, create_user, update_user, delete_user
from src.income_view import get_income,put_income,create_income,delete_income
from src.budget_view import get_budget, create_budget, update_budget, delete_budget
from src.budget_alert_view import get_alert, create_alert, update_alert, delete_alert
from src.income_category_view import get_income_category, create_income_category, update_income_category, delete_income_category
from src.expense_category_view import get, post, put, delete
from src.expense_view import get, post, put, delete

class UserView(APIView):
    def get(self, request):
        return get_users(request)

    def post(self, request):
        return create_user(request)

    def put(self, request, pk):
        return update_user(request, pk)

    def delete(self, request, pk):
        return delete_user(request, pk)


class IncomeView(APIView):

    def get(self, request):
        return get_income(request)

    def post(self, request):
        return create_income(request)

    def put(self, request, pk):
        return put_income(request, pk)

    def delete(self, request, pk):
        return delete_income(request, pk)


class IncomeCategoryView(APIView):
    def get(self, request):
        return get_income_category(request)

    def post(self, request):
        return create_income_category(request)

    def put(self, request, pk):
        return update_income_category(request, pk)

    def delete(self, request, pk):
        return delete_income_category(request, pk)

class ExpenseCategoryView(APIView):

    def get(self, request):
        return get(request)

    def post(self, request):
        return post(request)

    def put(self, request, pk):
        return put(request, pk)

    def delete(self, request, pk):
        return delete(request, pk)



class ExpenseView(APIView):

    def get(self, request):
        return get(request)

    def post(self, request):
        return post(request)

    def put(self, request, pk):
        return put(request, pk)

    def delete(self, request, pk):
        return delete(request, pk)



class BudgetView(APIView):

    def get(self, request):
        return get_budget(request)

    def post(self, request):
        return create_budget(request)

    def put(self, request, pk):
        return update_budget(request, pk)

    def delete(self, request, pk):
        return delete_budget(request, pk)


class BudgetAlertView(APIView):

    def get(self, request):
        return get_alert(request)

    def post(self, request):
        return create_alert(request)

    def put(self, request, pk):
        return update_alert(request, pk)

    def delete(self, request, pk):
        return delete_alert(request, pk)


