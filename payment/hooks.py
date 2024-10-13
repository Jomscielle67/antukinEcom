from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Order
import logging

# Set up a logger to capture issues
logger = logging.getLogger(__name__)

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    paypal_obj = sender

    # Add a try-except block to catch issues
    try:
        invoice_number = str(paypal_obj.invoice)
        # Log the IPN details
        logger.info(f"IPN received for invoice: {invoice_number}")

        # Retrieve the matching order
        order = Order.objects.get(invoice=invoice_number)

        # Update the order status
        if paypal_obj.payment_status == ST_PP_COMPLETED:
            order.paid = True
            order.save()
            logger.info(f"Order {order.id} marked as paid.")
        else:
            logger.warning(f"Payment not completed for order {order.id}.")

    except Order.DoesNotExist:
        logger.error(f"No order found with invoice: {paypal_obj.invoice}")

    except Exception as e:
        logger.exception(f"Error processing IPN: {str(e)}")
