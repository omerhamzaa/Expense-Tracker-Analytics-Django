import csv
from decimal import Decimal
from email.message import EmailMessage
from io import StringIO
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class IncomeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class ExpenseCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Income(models.Model):
    id = models.AutoField(primary_key = True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    income_category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.name} - {self.amount}"


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.name} - {self.amount} - {self.date}"


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    period = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} - {self.amount} - {self.expense_category.name}"


class BudgetAlert(models.Model):
    id = models.AutoField(primary_key=True)
    trigger_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=150)
    format = models.CharField(max_length=10, choices=[('CSV', 'CSV'), ('Excel', 'Excel')])
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trigger_at} - {self.message} - {self.budget_id.user_id.name}"


@receiver(post_save, sender=Expense)
def budget_tracking(sender, instance, **kwargs):
    """
    Signal to track expenses against the budget and trigger an alert
    when users exceed or approach their budget limit.
    """
    budgets = Budget.objects.filter(user_id=instance.user_id, expense_category=instance.expense_category)

    if budgets.exists():
        budget = budgets.first()

        # Calculate total expenses for the same user and category
        total_expenses = Expense.objects.filter(
            user_id=instance.user_id,
            expense_category=instance.expense_category
        ).aggregate(total=Sum('amount'))['total'] or Decimal(0)

        # Check if total expenses exceed or approach the budget amount
        if total_expenses >= budget.amount:
            # Create a BudgetAlert when the budget is exceeded
            BudgetAlert.objects.create(
                message=f"Warning: You've exceeded your budget for {instance.expense_category.name}!",
                format='CSV',  # or any other format
                budget_id=budget
            )
        elif total_expenses >= (budget.amount * Decimal(0.8)):
            # Create a BudgetAlert when 80% of the budget is spent
            BudgetAlert.objects.create(
                message=f"Alert: You've spent 80% of your budget for {instance.expense_category.name}.",
                format='Excel',
                budget_id=budget
            )


@receiver(post_save, sender=BudgetAlert)
def generate_report(sender, instance, **kwargs):
    """
    Signal to generate a detailed report when a BudgetAlert is triggered.
    The report includes the budget amount and all expenses under that budget category.
    """
    if not kwargs.get('created', False):
        return

    # Get the associated budget
    budget = instance.budget_id

    # Fetch all expenses for the same user and expense category
    expenses = Expense.objects.filter(
        user_id=budget.user_id,
        expense_category=budget.expense_category
    ).values('description', 'amount', 'date')

    # Calculate the total expense amount
    total_expenses = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or Decimal(0)

    # Create a CSV report
    if instance.format == 'CSV':
        output = StringIO()
        writer = csv.writer(output)

        # Write the report header
        writer.writerow(['User', 'Category', 'Budget Amount', 'Total Expenses', 'Trigger Time'])
        writer.writerow([budget.user_id.name, budget.expense_category.name, budget.amount, total_expenses, instance.trigger_at])

        # Write the details of all expenses
        writer.writerow([])  # Empty row for separating headers
        writer.writerow(['Expense Description', 'Amount', 'Date'])
        for expense in expenses:
            writer.writerow([expense['description'], expense['amount'], expense['date']])

        # Save the CSV content to the 'file' field in BudgetAlert
        instance.file.save(f'report_{instance.id}.csv', output)


@receiver(post_save, sender=Expense)
def deduct_expense_from_budget(sender, instance, created, **kwargs):
    if created:
        try:
            budget = Budget.objects.get(
                user_id=instance.user_id,
                expense_category=instance.expense_category
            )
            budget.amount -= instance.amount
            budget.save()
        except Budget.DoesNotExist:
            print("No budget found for this user and category.")


@receiver(post_save, sender=Budget)
def update_existing_budget(sender, instance, created, **kwargs):
    # If a new entry is created
    if created:
        # Look for existing budgets with the same user, category, and period, excluding the new one
        existing_budgets = Budget.objects.filter(
            user_id=instance.user_id,
            expense_category=instance.expense_category,
            period=instance.period
        ).exclude(id=instance.id)

        # If an existing budget is found, update its amount
        if existing_budgets.exists():
            existing_budget = existing_budgets.first()

            # Add the new amount to the existing budget
            existing_budget.amount += instance.amount
            existing_budget.save()

            # Delete the newly created budget entry since its amount is now added to the existing one
            instance.delete()

