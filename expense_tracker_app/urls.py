from django.urls import path
from . import views
from .views import UserView, IncomeView, IncomeCategoryView, ExpenseCategoryView, ExpenseView


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

]