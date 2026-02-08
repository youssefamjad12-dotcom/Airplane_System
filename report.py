import csv
from flight import FlightManager
from booking import BookingManager

class ReportManager:
    def __init__(self, user_file="users.csv", admin_file="admins.csv",
                 flight_manager: FlightManager = None, booking_manager: BookingManager = None):
        self.user_file = user_file
        self.admin_file = admin_file
        self.flight_manager = flight_manager
        self.booking_manager = booking_manager

    def load_customers_count(self):
        try:
            with open(self.user_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader if row["role"] == "customer")
                return count
        except FileNotFoundError:
            return 0

    def load_admins_count(self):
        try:
            with open(self.admin_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                count = sum(1 for row in reader)
                return count
        except FileNotFoundError:
            return 0

    def flights_count(self):
        if not self.flight_manager:
            return 0
        return len(self.flight_manager.flights)

    def bookings_count(self):
        if not self.booking_manager:
            return 0
        return len(self.booking_manager.bookings)

    def bookings_per_flight(self):
        if not self.flight_manager or not self.booking_manager:
            return {}

        result = {}
        for flight_id, flight in self.flight_manager.flights.items():
            count = sum(1 for b in self.booking_manager.bookings if b.flight_id == flight_id)
            result[flight.flight_number] = count
        return result

    def generate_report(self):
        print("===== SYSTEM REPORT =====")
        print(f"Total Customers: {self.load_customers_count()}")
        print(f"Total Admins: {self.load_admins_count()}")
        print(f"Total Flights: {self.flights_count()}")
        print(f"Total Bookings: {self.bookings_count()}")
        print("\nBookings per Flight:")
        for flight_number, count in self.bookings_per_flight().items():
            print(f"Flight {flight_number}: {count} bookings")
        print("=========================")
