import csv
import uuid
from datetime import datetime
from customer import Customer
from flight import Flight

PAYMENTS_FILE = "payments.csv"

class Payment:
    def __init__(self, customer_username: str, flight_id: str, amount: float):
        self.payment_id = str(uuid.uuid4())
        self.customer_username = customer_username
        self.flight_id = flight_id
        self.amount = amount
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



class PaymentManager:
    def __init__(self, file_path=PAYMENTS_FILE):
        self.file_path = file_path
        self.payments = []
        self.load_payments()

    def load_payments(self):
        try:
            with open(self.file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p = Payment(row["customer_username"], row["flight_id"], float(row["amount"]))
                    p.payment_id = row["payment_id"]
                    p.date = row["date"]
                    self.payments.append(p)
        except FileNotFoundError:
            pass

    def save_payments(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["payment_id", "customer_username", "flight_id", "amount", "date"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.payments:
                writer.writerow({
                    "payment_id": p.payment_id,
                    "customer_username": p.customer_username,
                    "flight_id": p.flight_id,
                    "amount": p.amount,
                    "date": p.date
                })

    def make_payment(self, customer: Customer, flight: Flight):
        if customer.wallet < flight.price:
            print("Insufficient balance")
            return None

        customer.wallet -= flight.price
        payment = Payment(customer.username, flight.flight_id, flight.price)
        self.payments.append(payment)
        self.save_payments()
        print(f"Payment successful: {flight.price} deducted from {customer.username}")
        return payment

    def list_payments(self, customer_username=None):
        for p in self.payments:
            if customer_username is None or p.customer_username == customer_username:
                print(f"PaymentID: {p.payment_id} | FlightID: {p.flight_id} | Amount: {p.amount} | Date: {p.date}")
