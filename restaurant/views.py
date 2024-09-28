from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, timedelta
import pytz  # Import pytz for time zone handling

# Define the menu items and their prices
menuItem = {
    'Pizza': 10,
    'Burger': 8,
    'Salad': 5,
    'Sandwich': 6.50,
}

# Daily specials available
daily_Special = ['Tacos', 'Pasta', 'Sushi', 'Falafel']

def main(request):
    """
    Render the main page of the restaurant.
    """
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    """
    Render the order page with menu items and a daily special.
    """
    template_name = 'restaurant/order.html'
    daily_special = random.choice(daily_Special)

    context = {
        'menu_items': menuItem,
        'daily_special': daily_special,
        'special_price': 7  
    }
    
    return render(request, template_name, context)

def confirmation(request):
    """
    Handle the confirmation of an order after the customer submits it.

    If the request method is GET, redirect to the order page. Otherwise,
    process the POST data to compile the ordered items and customer information.
    """
    ordered_items = []
    total_price = 0

    # Check for GET request and redirect to order page
    if request.method == 'GET':
        return redirect('order')

    template_name = 'restaurant/confirmation.html'

    # Process ordered items from the POST request
    for item, price in menuItem.items():
        if request.POST.get(item):
            ordered_items.append(item)
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
    random_minutes = random.randint(30, 60)  # Get a random number of minutes between 30 and 60
    ready_time = datetime.now() + timedelta(minutes=random_minutes)  # Add random minutes to current time

    # Localize the ready_time to Eastern Standard Time (EST)
    est = pytz.timezone('America/New_York')  # EST/EDT time zone
    ready_time = ready_time.astimezone(est)

    # Prepare context for rendering the confirmation page
    context = {
        'ordered_items': ordered_items,
        'customer_info': customer_info,
        'total_price': total_price,
        'ready_time': ready_time.strftime("%I:%M %p")  # Format the ready time in 12-hour clock format
    }
    
    return render(request, template_name, context)