from django.urls import path
from . import views
from .views import UserView, IncomeView, IncomeCategoryView, ExpenseCategoryView, ExpenseView, BudgetView, BudgetAlertView


urlpatterns = [

    path('users/', UserView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),

    path('income/', IncomeView.as_view(), name='Income-detail'),
    path('income/<int:pk>/', IncomeView.as_view(), name='Income-update'),

    path('Expense/', ExpenseView.as_view(), name='Expense-detail'),
    path('Expense/<int:pk>/', ExpenseView.as_view(), name='Expense-update'),

    path('income_category/', IncomeCategoryView.as_view(), name='Income_category-detail'),
    path('income_category/<int:pk>/', IncomeCategoryView.as_view(), name='Income_category-update'),

    path('expense_category/', ExpenseCategoryView.as_view(), name='Expense_category-detail'),
    path('expense_category/<int:pk>/', ExpenseCategoryView.as_view(), name='Expense_category-update'),

    path('budget/', BudgetView.as_view(), name='BudgetView-detail'),
    path('budget/<int:pk>/', BudgetView.as_view(), name='BudgetView-update'),

    path('budget_alert/', BudgetAlertView.as_view(), name='Budget_alert_View-detail'),
    path('budget_alert/<int:pk>/', BudgetAlertView.as_view(), name='Budget_alert_View-update'),

]