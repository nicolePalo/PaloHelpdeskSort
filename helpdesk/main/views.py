from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Ticket

# Create your views here.

def quicksort(items, key=lambda x: x):
    """
    Perform quicksort on a list of items based on a key function.
    By default, sorts by the provided 'key' function, which is applied to each item.

    CALL THIS FUNCTION IN tickets()
    """
    if len(items) <= 1:
        return items
    pivot = items[0]
    left = [item for item in items[1:] if key(item) <= key(pivot)]
    right = [item for item in items[1:] if key(item) > key(pivot)]
    return quicksort(left, key) + [pivot] + quicksort(right, key)

def add_ticket(request):
    context = {
        'nav_selected': 'Employees',
        'employees' : Employee.objects.all()
    }
    if request.method == "POST":
        pk = request.POST.get('id_number')
        fa = request.POST.get('filedAgainst')
        tt = request.POST.get('ticketType')
        sv = request.POST.get('severity')
        daysOpen = request.POST.get('daysOpen')

        employee = get_object_or_404(Employee, pk=pk)

        Ticket.objects.create(employee=employee, filedAgainst=fa, ticketType=tt, severity_level=sv, daysOpen=daysOpen)

        return redirect('tickets')

    return render(request, 'main/add_ticket.html',context)

def resolve_ticket(request,pk):
    ticket =  get_object_or_404(Ticket,pk=pk)
    ticket.delete()

    return redirect('tickets')
    

def view_all_tickets(request):
    tickets = Ticket.objects.all()
    context = {'tickets':tickets}
    

    return render(request, 'main/view_all_tickets.html', context)

def view_ticket(request, pk):
    context = {}
    ticket = get_object_or_404(Ticket, pk=pk)

    return render(request, 'main/view_ticket.html')
    


