from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import testApp.dbconnect as dbconnect
import testApp.my_funcs as my_funcs
import re
import testApp.made_basket as made_basket

def main_page(request):
    if request.method == 'GET':
        total_price = made_basket.total_price(request)
        all_categories = dbconnect.get_data('info', params={'name': 'category'})
        return render(request, 'main_page.html', {'all_categories': all_categories, 'total_price': total_price})


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


def category(request, category_name, page_num):
    if request.method == 'GET':
        rgx = re.compile(f'.*{category_name}.*', re.IGNORECASE)
        res = dbconnect.get_data("products", params={"Category": rgx}, all=True)
        all_categories = dbconnect.get_data('info', params={'name': 'category'})
        total_price = made_basket.total_price(request)
        object_in_page = 18
        try:
            product_on_page = res[page_num*object_in_page-object_in_page: page_num*object_in_page]
        except:
            product_on_page = res[page_num * object_in_page - object_in_page:]
        if page_num < 3:
            list_page_num = [1, 2, 3, 4, 5]
        else:
            list_page_num = [page_num -2, page_num - 1, page_num, page_num + 1, page_num +2]
        return render(request, 'category.html', {
            "category": category_name,
            "products": product_on_page,
            'page_num': list_page_num,
            'all_categories': all_categories,
            'total_price': total_price
        })


def item(request, item_id):
    if request.method == "GET":
        basket_list = made_basket.basket_data(request)
        total_price = made_basket.total_price(request)
        product = dbconnect.get_data("products", params={"UniqId": item_id})
        all_categories = dbconnect.get_data('info', params={'name': 'category'})
        try:
            details = product['Product Specification'].split('|')
            specification = my_funcs.list_to_dict(details)
            minidescription = my_funcs.upadate_minidescription(product['TechnicalDetails'])
        except:
            specification, minidescription ='', ''
        return render(request, 'item.html', {
            "product": product,
            'specification': specification,
            'minidescription': minidescription,
            'all_categories': all_categories,
            'basket_list': basket_list,
            'total_price': total_price
        })
    elif request.method == "POST":
        basket_data = request.session.get('basket', {})
        item_count = basket_data.get(str(item_id), 0)
        basket_data[str(item_id)] = item_count + 1
        request.session["basket"] = basket_data
        return redirect(f'/item/{item_id}/')
    pass


def search(request, page_num):
    if request.method == 'GET':
        total_price = made_basket.total_price(request)
        keyword = request.GET.get('keyword', '')
        search_in_category = request.GET.get('search_in_category')
        min_price = request.GET.get('min_price', '0')
        max_price = request.GET.get('max_price', '10000000')
        if min_price > max_price:
            max_price = min_price
            min_price = 0
        category_name = search_in_category
        if search_in_category == 'All':
            search_in_category = ''
        rgx_for_category = re.compile(f'.*{search_in_category}.*', re.IGNORECASE)
        rgx_for_name = re.compile(f'.*{keyword}.*', re.IGNORECASE)
        res = dbconnect.get_data("products", params={
            "Category": rgx_for_category,
            "ProductName":rgx_for_name,
            "&and":[{'Price': {'$gt': int(min_price)}}, {'Price': {'$lt': int(max_price)}}]},
                                 all=True)
        all_categories = dbconnect.get_data('info', params={'name': 'category'})
        try:
            product_on_page = res[page_num*9-9: page_num*9]
        except:
            product_on_page = res[page_num * 9 - 9:]
        if page_num < 3:
            list_page_num = [1, 2, 3, 4, 5]
        else:
            list_page_num = [page_num -2, page_num - 1, page_num, page_num + 1, page_num +2]
        return render(request, 'category.html', {
            "category": category_name,
            "products": product_on_page,
            'page_num': list_page_num,
            'all_categories': all_categories,
            'total_price': total_price
        })



def contacts(request):
    pass


@login_required(login_url='/login')
def complete_purchase(request):
    if request.method == "POST":
        basket_data = request.session.get('basket', {})
        dbconnect.write_data('complete_purchases', basket_data)
        request.session["basket"] = {}
        return redirect('/')
    pass


@login_required(login_url='/login')
def logout_users(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    else:
        logout(request)
