from django.contrib import admin
from .models import User, Income,IncomeCategory,ExpenseCategory,Expense,Budget,BudgetAlert


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_number', 'email', 'date')


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'description', 'date', 'user_id', 'income_category')


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'description', 'date', 'user_id', 'expense_category')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'period', 'created_at', 'expense_category', 'user_id')


@admin.register(BudgetAlert)
class BudgetAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger_at', 'message', 'format', 'file', 'budget_id')
