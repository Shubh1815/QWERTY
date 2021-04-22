from django.shortcuts import render, redirect, reverse
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from users.permissions import is_manager
from core.models import Product, Transaction
from users.forms import UserProfileChangeForm
from qwerty.settings import LOGIN_URL

import json
# Create your views here.


@is_manager(login_url=LOGIN_URL)
def dashboard(request, category):
    if request.method == 'GET':
        if category == Product.CANTEEN:
            return render(request, 'manager/canteen.html')
        if category == Product.STATIONARY:
            return render(request, 'manager/stationary.html')
        if category == Product.TRANSPORTATION:
            return render(request, 'manager/transportation.html')

        return HttpResponse(status=404)


@is_manager(login_url=LOGIN_URL)
def profile(request):
    user = request.user
    if request.method == 'GET':
        form = UserProfileChangeForm(instance=user)

    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect(reverse('manager:profile'))

    context = {
        'form': form
    }

    return render(request, 'manager/profile.html', context=context)


@is_manager(login_url=LOGIN_URL)
def products(request, category):
    if request.method == 'GET':
        canteen_products = Product.objects.filter(category=category)

        return JsonResponse(serializers.serialize('json', canteen_products), safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if not Transaction.process_transactions(data):
            return HttpResponse('Student does not have enough money!', status=400)

        return HttpResponse('Successful!', status=200)

