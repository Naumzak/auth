from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import testApp.dbconnect as dbconnect
from bson.objectid import ObjectId


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main_page.html')


def basket(request):
    if request.method == 'GET':
        basket_data = request.session.get('basket', {})
        return render(request, 'basket.html', {"basket": basket_data})


def user_admin(request):
    if request.method == 'GET':
        return render(request, 'user_admin.html')


def login_users(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(f'{username} logged')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse(f'{username} created')


def category(request, category_name):
    if request.method == 'GET':
        res = dbconnect.get_data("products", params={"category": category_name}, all=True)
        return render(request, 'category.html', {"category": category_name, "products": res})


def item(request, item_id):
    if request.method == "GET":
        res = dbconnect.get_data("products", params={"_id": ObjectId(item_id)})
        return render(request, 'item.html', {"product": res})
    elif request.method == "POST":
        basket_data = request.session.get('basket', {})
        item_count = basket_data.get(str(item_id), 0)
        basket_data[str(item_id)] = item_count + 1
        request.session["basket"] = basket_data
        return redirect(f'/item/{item_id}/')
    pass


def search(request):
    pass


def contacts(request):
    pass


@login_required(login_url='/login')
def complete_purchase(request):
    if request.method == "POST":
        basket_data = request.session.get('basket', {})
        dbconnect.write_data('complete_purchases', basket_data)
        request.session["basket"] = {}
        return redirect('/basket')
    pass


@login_required(login_url='/login')
def logout_users(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    else:
        logout(request)
