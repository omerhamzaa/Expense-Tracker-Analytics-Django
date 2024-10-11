from django.db import models


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
        return f"{self.trigger_at} - {self.message} - {self.budget.user_id.username}"



