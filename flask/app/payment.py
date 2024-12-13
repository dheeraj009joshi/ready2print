import requests
import hashlib
import json

class PhonePePaymentGateway:
    def __init__(self):
        """
        Initialize the PhonePePaymentGateway class.

        :param merchant_id: Merchant ID provided by PhonePe
        :param merchant_key: Merchant Key provided by PhonePe
        :param merchant_secret: Merchant Secret provided by PhonePe
        :param base_url: Base URL of PhonePe APIs
        """
        #Test details#
        self.merchant_id = "PGTESTPAYUAT"
        self.merchant_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
        # self.merchant_secret = merchant_secret
        self.base_url = "https://api-preprod.phonepe.com/apis/hermes/vi"

    def generate_checksum(self, payload):
        """
        Generate checksum using the payload and merchant secret.
        """
        data = json.dumps(payload)
        return hashlib.sha256((data + self.merchant_key).encode()).hexdigest()

    def initiate_payment(self, transaction_id, amount, customer_phone, customer_email, callback_url):
        """
        Initiate a payment transaction.
        
        :param order_id: Unique order ID
        :param amount: Amount in paise (100 paise = 1 INR)
        :param customer_phone: Customer phone number
        :param customer_email: Customer email
        :param callback_url: Callback URL for transaction status
        :return: Response from PhonePe
        """
        endpoint = f"{self.base_url}/transaction/initiate"
        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": transaction_id,
            "merchantUserId": customer_phone,
            "amount": amount,
            "currency": "INR",
            "redirectUrl": callback_url,
            "email": customer_email,
            "mobileNumber": customer_phone
        }
        checksum = self.generate_checksum(payload)
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": checksum,  # Correct checksum format (without the ###1 suffix)
            "X-MERCHANT-ID": self.merchant_key
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def check_status(self, order_id):
        """
        Check the status of a transaction.
        
        :param order_id: Order ID of the transaction
        :return: Response from PhonePe
        """
        endpoint = f"{self.base_url}/transaction/status/{order_id}"
        payload = {"merchantId": self.merchant_id, "merchantTransactionId": order_id}
        checksum = self.generate_checksum(payload)
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": f"{checksum}###1",
            "X-MERCHANT-ID": self.merchant_key
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def refund_payment(self, order_id, refund_amount):
        """
        Initiate a refund for a transaction.
        
        :param order_id: Order ID of the transaction
        :param refund_amount: Amount to refund in paise
        :return: Response from PhonePe
        """
        endpoint = f"{self.base_url}/transaction/refund"
        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": order_id,
            "amount": refund_amount,
            "currency": "INR"
        }
        checksum = self.generate_checksum(payload)
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": f"{checksum}###1",
            "X-MERCHANT-ID": self.merchant_key
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

# Example usage

