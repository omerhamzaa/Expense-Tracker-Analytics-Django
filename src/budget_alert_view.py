from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from expense_tracker_app.models import Budget, BudgetAlert



def get_alert(request):
    alerts = BudgetAlert.objects.all()
    data = [{
        "id": alert.id,
        "trigger_at": alert.trigger_at,
        "message": alert.message,
        "format": alert.format,
        "file": alert.file.url if alert.file else None,
        "budget_id": alert.budget_id.id
    } for alert in alerts]
    return Response(data)

def create_alert(request):
    message = request.data.get('message')
    format = request.data.get('format')
    budget_id = request.data.get('budget_id')
    file = request.FILES.get('file', None)  # Optional file upload

    # Validate required fields
    if not all([message, format, budget_id]):
        return Response({"error": "Message, format, and budget ID are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate format choice
    if format not in ['CSV', 'Excel']:
        return Response({"error": "Invalid format. Choose either 'CSV' or 'Excel'."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if budget exists
    try:
        budget = Budget.objects.get(id=budget_id)
    except Budget.DoesNotExist:
        return Response({"error": "Budget not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the budget alert
    budget_alert = BudgetAlert.objects.create(
        message=message,
        format=format,
        file=file,
        budget_id=budget
    )

    return Response({
        "id": budget_alert.id,
        "trigger_at": budget_alert.trigger_at,
        "message": budget_alert.message,
        "format": budget_alert.format,
        "file": budget_alert.file.url if budget_alert.file else None,
        "budget_id": budget_alert.budget_id.id
    }, status=status.HTTP_201_CREATED)

def update_alert(request, pk):
    budget_alert = get_object_or_404(BudgetAlert, pk=pk)

    for attr, value in request.data.items():
        if attr == "budget_id":
            try:
                budget = Budget.objects.get(id=value)
                setattr(budget_alert, "budget_id", budget)
            except Budget.DoesNotExist:
                return Response({"error": "Budget not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif attr == "file":
            # Handle file upload separately
            file = request.FILES.get('file')
            if file:
                budget_alert.file = file
        else:
            setattr(budget_alert, attr, value)

    budget_alert.save()

    return Response({
        "id": budget_alert.id,
        "trigger_at": budget_alert.trigger_at,
        "message": budget_alert.message,
        "format": budget_alert.format,
        "file": budget_alert.file.url if budget_alert.file else None,
        "budget_id": budget_alert.budget_id.id
    }, status=status.HTTP_200_OK)

def delete_alert(request, pk):
    budget_alert = get_object_or_404(BudgetAlert, pk=pk)
    budget_alert.delete()
    return Response({"message": "Budget alert deleted successfully"}, status=status.HTTP_204_NO_CONTENT)