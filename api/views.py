# api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
import stripe

# Set your Stripe secret key: remember to switch to your live secret key in production
stripe.api_key = 'sk_test_51OxeVwFlmGUmehSxkjrfa6mPOwiiJ3LsAmviAInPdoPEGqQ0yC3kgRLBG9wWsdrvp0W6elWOEqape5BxYPvbo06Z00dNwrl0ni'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['POST'])
def process_payment(request, order_id):
    # Retrieve the payment token from the request
    payment_token = request.data.get('paymentToken')

    # Retrieve the order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Charge the customer
        charge = stripe.Charge.create(
            amount=int(order.get_total_price() * 100), # Convert amount to cents
            currency='usd',
            source=payment_token,
            description=f'Charge for Order {order.id}'
        )

        # Update the order with payment status and transaction id
        order.payment_status = 'Completed' if charge['paid'] else 'Failed'
        order.transaction_id = charge['id']
        order.save()

        return Response({'status': order.payment_status, 'transaction_id': order.transaction_id}, status=status.HTTP_200_OK)

    except stripe.error.StripeError as e:
        # Handle Stripe error
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle general error
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
