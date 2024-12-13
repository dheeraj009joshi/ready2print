from flask import (
    Blueprint,
    Response,
    request,
    render_template,
    session,
    flash,
    redirect,
    url_for,
)
import requests
from app.DB.Db_config import (
    USER_collection,
    PrintOwner_collection,
    PrintRequest_collection,
)
from app.function import current_user, login_required, serialize
from ..payment import PhonePePaymentGateway
from phonepe import PhonePe
from ..config import PHONE_PE_MERCHANT, PHONE_PE_MERCHANT_KEY

checkout_bp = Blueprint("checkout_bp", __name__)


@checkout_bp.route("/checkout")
@login_required
def index():
    """
    Render the checkout page with payment details.
    """
    print_request_id = request.args.get("print_request_id")
    if not print_request_id:
        flash("Print request ID is missing.", "error")
        return redirect(url_for("general_bp.index"))

    print_request = PrintRequest_collection.find_one({"_id": print_request_id})
    if not print_request:
        flash("Print request not found.", "error")
        return redirect(url_for("general_bp.index"))

    # Generate transaction ID if not present
    transaction_id = print_request.get("transaction_id", None)

    return render_template(
        "home/checkout-page.html",
        segment="index",
        user=current_user(),
        request=print_request,
        transaction_id=transaction_id,
    )


@checkout_bp.route("/pay-now", methods=["POST"])
@login_required
def pay_now():
    """
    Initiate a payment using the PhonePe API.
    """
    transaction_id = request.form.get("transaction_id")
    print_request_id = request.form.get("print_request_id")
    amount = request.form.get("price")  # Ensure this is in paise (1 INR = 100 paise)

    if not transaction_id or not print_request_id or not amount:
        flash("Missing transaction ID, print request ID, or amount.", "error")
        return redirect(url_for("checkout_bp.index", print_request_id=print_request_id))

    print_request = PrintRequest_collection.find_one({"_id": print_request_id})

    # Send the request to PhonePe to initiate the payment
    # response = payment.create_order(
    #     order_id=transaction_id,
    #     amount=amount,
    #     user=print_request['user'],
    #     rediurl_for('checkout_bp.verify_payment', transaction_id=transaction_id, print_request_id=print_request_id, _external=True)
    # )
    payment = PhonePe(
        PHONE_PE_MERCHANT,
        PHONE_PE_MERCHANT_KEY,
        "https://api.phonepe.com/apis/hermes",
        url_for(
            "checkout_bp.verify_payment",
            transaction_id=transaction_id,
            print_request_id=print_request_id,
            _external=True,
        ),
        url_for(
            "checkout_bp.verify_payment",
            transaction_id=transaction_id,
            print_request_id=print_request_id,
            _external=True,
        ),
    )
    response = payment.create_txn(
        transaction_id, amount.split(".")[0], print_request["user"]["_id"]
    )
    print(response)
    if response.get("success"):
        flash("Redirecting to payment gateway...", "success")
        return redirect(response["data"]["instrumentResponse"]["redirectInfo"]["url"])
    else:
        flash("Failed to initiate payment. Please try again.", "error")
        return redirect(url_for("checkout_bp.index", print_request_id=print_request_id))


@checkout_bp.route("/verify-payment", methods=["POST"])
@login_required
def verify_payment():
    """
    Verify the payment status and update the database if successful.
    """
    transaction_id = request.args.get("transaction_id")
    print_request_id = request.args.get("print_request_id")

    if not transaction_id or not print_request_id:
        flash("Missing transaction ID or print request ID.", "error")
        return redirect(url_for("checkout_bp.index", print_request_id=print_request_id))

    # Check the payment status
    payment = PhonePe(
        PHONE_PE_MERCHANT,
        PHONE_PE_MERCHANT_KEY,
        "https://api.phonepe.com/apis/hermes",
        url_for(
            "checkout_bp.verify_payment",
            transaction_id=transaction_id,
            print_request_id=print_request_id,
        ),
        url_for(
            "checkout_bp.verify_payment",
            transaction_id=transaction_id,
            print_request_id=print_request_id,
        ),
    )
    response = payment.check_txn_status(transaction_id)
    print(response)
    if response.get("success"):
        # Update the database with payment success
        # Insert the print request into the collection
        print_request_id = print_request_id

        # Update the user document to append the new print request ID
        USER_collection.update_one(
            {"_id": session["user_id"]},  # Assuming users is a dict with an _id field
            {"$addToSet": {"print_requests": print_request_id}},
        )
        print_request = PrintRequest_collection.find_one({"_id": print_request_id})

        PrintRequest_collection.update_one(
            {"_id": print_request_id},
            {
                "$set": {"transaction_complete": True}
            },
        )

        try:
            printer_credits = print_request["printerOwner"]["printer_credits"]
            total_credits = print_request["printerOwner"]["printer_total_credits"]
        except:
            printer_credits = 0
            total_credits = 0

        # Update the printer owner document to append the new print request ID
        PrintOwner_collection.update_one(
            {"_id": session["printer_id"]},  # Filter criteria
            {
                "$addToSet": {"print_requests": print_request_id},  # Add print request
                "$set": {
                    "printer_credits": printer_credits
                    + print_request["documentPrintCostP"],
                    "printer_total_credits": total_credits
                    + print_request["documentPrintCostP"],
                },
            },
            upsert=True,  # Upsert option
        )
        flash("Payment verified successfully.", "success")
    else:
        flash(f"Payment failed or pending. Status: {response.get('status')}", "error")

    return redirect(url_for("checkout_bp.index", print_request_id=print_request_id))
