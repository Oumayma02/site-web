import os  # Import os module for path manipulation
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Purchase

def form_view(request):
    if request.method == 'POST':
        vm_name = request.POST.get('vm_name')
        vm_cores = request.POST.get('vm_cores')
        vm_memory = request.POST.get('vm_memory')
        disk_size = request.POST.get('disk_size')

        # Create a new Purchase object
        purchase = Purchase.objects.create(
            vm_name=vm_name,
            vm_cores=vm_cores,
            vm_memory=vm_memory,
            disk_size=disk_size,
        )

        # Store the purchase ID in session
        request.session['purchase_id'] = purchase.id

        return redirect('display_view')

    return render(request, 'form.html')

# inside views.py

def admin_confirm_purchase(request, purchase_id):
    # Your logic for admin to confirm a purchase
    pass

def display_view(request):
    purchase_id = request.session.get('purchase_id')
    if not purchase_id:
        return HttpResponse("No purchase information available")

    purchase = get_object_or_404(Purchase, id=purchase_id)

    context = {
        'vm_name': purchase.vm_name,
        'vm_cores': purchase.vm_cores,
        'vm_memory': purchase.vm_memory,
        'disk_size': purchase.disk_size,
    }
    return render(request, 'display.html', context)



def purchase_select_view(request):
    if request.method == 'GET':
        purchases = Purchase.objects.all()
        return render(request, 'select_purchase.html', {'purchases': purchases})
    elif request.method == 'POST':
        confirmed_purchases = request.POST.getlist('confirmed_purchases')
        action = request.POST.get('action')

        if action == 'confirm':
            Purchase.objects.filter(id__in=confirmed_purchases).update(confirmed=True)
            for purchase_id in confirmed_purchases:
                purchase = get_object_or_404(Purchase, id=purchase_id)
                trigger_jenkins_job(purchase)
        elif action == 'deny':
            Purchase.objects.filter(id__in=confirmed_purchases).update(confirmed=False)

        return redirect('purchase_select_view')

def trigger_jenkins_job(purchase):
    jenkins_url = 'http://192.168.254.158:8080/job/here/build?delay=0sec'
    jenkins_username = 'oumayma'
    jenkins_token = '117bb4845ab11896a8eed50eb9b9332f9a'  # Replace with your actual Jenkins token

    params = {
        'VM_NAME': purchase.vm_name,
        'VM_CORES': purchase.vm_cores,
        'VM_MEMORY': purchase.vm_memory,
        'DISK_SIZE': purchase.disk_size,
    }

    response = requests.post(jenkins_url, params=params, auth=(jenkins_username, jenkins_token))
    if response.status_code != 201:
        print(f"Failed to trigger Jenkins job: {response.status_code} - {response.text}")
    else:
        print("Jenkins job triggered successfully")
