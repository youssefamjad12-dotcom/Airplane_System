import flight
import csv
import uuid
from datetime import datetime

BOOKINGS_FILE = "bookings.csv"

class Booking:
    def __init__(self, customer_username: str, flight_id: str, seat_no: str):
        self.booking_id = str(uuid.uuid4())#tybe hent
        self.customer_username = customer_username
        self.flight_id = flight_id
        self.seat_no = seat_no
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class BookingManager:
    def __init__(self, file_path=BOOKINGS_FILE):
        self.file_path = file_path#csv file that stores bookings deals with hard
        self.bookings = []  # list of Booking نقدر نعمل عليها العمليات و بعدين نبقا نعدل في الcsv
        self.load_bookings()

    def load_bookings(self):
        try:
            with open(self.file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    b = Booking(row["customer_username"], row["flight_id"], row["seat_no"])
                    b.booking_id = row["booking_id"]
                    b.date = row["date"]
                    self.bookings.append(b)
        except FileNotFoundError:
            pass

    def save_bookings(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:#w delete all thing in csv for append the new data and last
            fieldnames = ["booking_id", "customer_username", "flight_id", "seat_no", "date"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for b in self.bookings:
                writer.writerow({
                    "booking_id": b.booking_id,
                    "customer_username": b.customer_username,
                    "flight_id": b.flight_id,
                    "seat_no": b.seat_no,
                    "date": b.date
                })

    def create_booking(self, customer_username, flight_manager, flight_id, seat_no):
        # التحقق من الرحلة
        if flight_id not in flight_manager.flights:
            print("Flight not found")
            return None

        flight = flight_manager.flights[flight_id]

        # التحقق من المقعد
        if seat_no not in flight.seats:
            print("Invalid seat number")
            return None

        if flight.seats[seat_no].is_reserved:
            print("Seat already reserved")
            return None

        # حجز المقعد
        flight.seats[seat_no].is_reserved = True

        # إنشاء booking
        booking = Booking(customer_username, flight_id, seat_no)
        self.bookings.append(booking)
        self.save_bookings()
        print(f"Booking successful for {customer_username} on seat {seat_no}")
        return booking

    def list_bookings(self, customer_username=None):
        for b in self.bookings:
            if customer_username is None or b.customer_username == customer_username:
                print(f"BookingID: {b.booking_id} | FlightID: {b.flight_id} | Seat: {b.seat_no} | Date: {b.date}")
