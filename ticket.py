from flight import FlightManager
from booking import BookingManager

class TicketSystem:
    def __init__(self, booking_manager: BookingManager, flight_manager: FlightManager):
        self.booking_manager = booking_manager
        self.flight_manager = flight_manager

    def print_ticket(self, booking_id: str):
        # البحث عن الحجز
        booking = None
        for b in self.booking_manager.bookings:
            if b.booking_id == booking_id:
                booking = b
                break

        if not booking:
            print("Booking not found")
            return

        # البحث عن الرحلة
        flight = self.flight_manager.flights.get(booking.flight_id)
        if not flight:
            print("Flight info not found")
            return

        # طباعة كل المعلومات
        print("----- TICKET -----")
        print(f"Booking ID: {booking.booking_id}")
        print(f"Customer: {booking.customer_username}")
        print(f"Flight Number: {flight.flight_number}")
        print(f"Airline: {flight.airline}")
        print(f"From: {flight.origin} To: {flight.destination}")
        print(f"Price: {flight.price}")
        print(f"Date: {flight.date} Departure: {flight.departure_time}")
        print(f"Duration: {flight.duration}")
        print(f"Seat: {booking.seat_no}")
        print(f"Booking Date: {booking.date}")
        print("------------------")

    def print_all_tickets_for_customer(self, customer_username: str):
        for b in self.booking_manager.bookings:
            if b.customer_username == customer_username:
                self.print_ticket(b.booking_id)
