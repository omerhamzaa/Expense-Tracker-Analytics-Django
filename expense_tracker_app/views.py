from datetime import timezone, timedelta

from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from expense_tracker_app.models import User, BudgetAlert, Expense
from src.user_view import get_users, create_user, update_user, delete_user
from src.income_view import get_income,put_income,create_income,delete_income
from src.budget_view import get_budget, create_budget, update_budget, delete_budget
from src.budget_alert_view import get_alert, create_alert, update_alert, delete_alert
from src.income_category_view import get_income_category, create_income_category, update_income_category, delete_income_category
from src.expense_category_view import get, post, put, delete
from src.expense_view import get, post, put, delete


def download_report(request, user_id):
    """
    View to download the report for a given user ID.
    """
    try:
        # Fetch the latest BudgetAlert for the given user ID
        user = get_object_or_404(User, id=user_id)
        budget_alert = BudgetAlert.objects.filter(budget_id__user_id=user).latest('trigger_at')

        # Check if the report file exists
        if budget_alert.file and default_storage.exists(budget_alert.file.path):
            # Serve the file for download
            with open(budget_alert.file.path, 'rb') as report_file:
                response = HttpResponse(report_file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename={budget_alert.file.name}'
                return response
        else:
            raise Http404("No report file available for download.")
    except BudgetAlert.DoesNotExist:
        raise Http404("No report found for this user.")


def expense_summary(request, period=None):
    user_id = request.user.id  # Get the ID of the logged-in user

    # Filter expenses by user_id
    expenses = Expense.objects.filter(user_id=user_id)  # Use user_id here

    # Filter by custom period if provided
    if period == 'daily':
        expenses = expenses.filter(date__date=timezone.now().date())
    elif period == 'weekly':
        week_start = timezone.now() - timedelta(days=7)
        expenses = expenses.filter(date__gte=week_start)
    elif period == 'monthly':
        month_start = timezone.now().replace(day=1)
        expenses = expenses.filter(date__gte=month_start)
    # You can add more periods or custom date ranges as needed

    # Aggregate total expenses by category
    expense_summary_by_category = (
        expenses.values('expense_category__name')
        .annotate(total=Sum('amount'))
    )

    # Aggregate total expenses by date (day/month/year)
    expense_summary_by_date = (
        expenses.values('date__date')
        .annotate(total=Sum('amount'))
        .order_by('date__date')
    )

    context = {
        'expense_summary_by_category': expense_summary_by_category,
        'expense_summary_by_date': expense_summary_by_date,
    }

    return render(request, 'expense_tracker_app/template/expense.html', context)


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


