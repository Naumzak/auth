import testApp.dbconnect as dbconnect


def basket_data(request):
    basket_list = []
    for item, count in request.session.get('basket', {}).items():
        product = dbconnect.get_data('products', {'UniqId': item})
        product['Count'] = count
        basket_list.append(product)
    return basket_list


def total_price(request):
    items_in_basket = request.session.get('basket', {})
    total_price = sum([float(dbconnect.get_data('products', {'UniqId': p})['Price'][1:])*items_in_basket[p] for p in items_in_basket])
    total_price = "{:.2f}".format(total_price)
    return total_price
