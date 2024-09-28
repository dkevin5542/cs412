from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  

# Define the menu items and their prices
menuItem = {
    'Pizza': 10,
    'Burger': 8,
    'Salad': 5,
    'Sandwich': 6.50,
}

pizza_toppings = {
    'Pepperoni': 1.50,
    'Mushrooms': 1.00,
    'Onions': 0.75,
    'Sausage': 2.00,
    'Bacon': 2.50,
    'Extra cheese': 1.25,
    'Black olives': 1.00,
    'Green peppers': 0.75,
    'Pineapple': 1.50,
    'Spinach': 1.25,
}

def order(request):
    """
    Render the order page with menu items, daily special, and pizza toppings.
    """
    template_name = 'restaurant/order.html'
    daily_special = random.choice(daily_Special)

    context = {
        'menu_items': menuItem,
        'daily_special': daily_special,
        'special_price': 7,
        'pizza_toppings': pizza_toppings, 
    }
    
    return render(request, template_name, context)

# Daily specials available
daily_Special = ['Tacos', 'Pasta', 'Sushi', 'Falafel']

def main(request):
    """
    Render the main page of the restaurant.
    """
    template_name = 'restaurant/main.html'
    return render(request, template_name)


def confirmation(request):
    """
    Handle the confirmation of an order after the customer submits it.
    """
    ordered_items = []
    total_price = 0
    selected_toppings = []

    # Check for GET request and redirect to order page
    if request.method == 'GET':
        return redirect('order')

    template_name = 'restaurant/confirmation.html'

    # Process ordered items from the POST request
    for item, price in menuItem.items():
        if request.POST.get(item):
            ordered_items.append(item)
            total_price += price

    # Check if the pizza was ordered and process its toppings
    if request.POST.get('Pizza'):
        for topping, price in pizza_toppings.items():
            if request.POST.get(topping):
                selected_toppings.append(topping)
                total_price += price

    # Check if the daily special was added
    if request.POST.get('Daily Special'):
        ordered_items.append(request.POST['daily_special_name'])
        total_price += 7

    # Collect customer information
    customer_info = {
        'name': request.POST.get('name'),
        'phone': request.POST.get('phone'),
        'email': request.POST.get('email')
    }

    # Calculate ready time for the order randomly between 30 and 60 minutes
    random_minutes = random.randint(30, 60)
    ready_time = datetime.now() + timedelta(minutes=random_minutes)

    # Localize the ready_time to Eastern Time (EST/EDT using zoneinfo)
    eastern_time = ready_time.astimezone(ZoneInfo("America/New_York"))

    # Prepare context for rendering the confirmation page
    context = {
        'ordered_items': ordered_items,
        'customer_info': customer_info,
        'total_price': total_price,
        'ready_time': eastern_time.strftime("%I:%M %p"),
        'selected_toppings': selected_toppings  
    }
    
    return render(request, template_name, context)