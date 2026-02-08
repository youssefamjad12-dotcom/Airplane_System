import uuid
import csv
import os
from datetime import datetime
from typing import Dict

import hashlib
from admin import AdminManager as User

class Seat:
    def __init__(self, seat_no):
        self.seat_no = seat_no
        self.is_reserved = False


class Flight:
    def __init__(self, flight_number, origin, destination,
                 price: float,
                 date: str,
                 departure_time: str,
                 duration: str,
                 airline: str = "Unknown",
                 seat_count: int = 150):

        self.flight_id = str(uuid.uuid4())
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.price = price
        self.date = date
        self.departure_time = departure_time
        self.duration = duration
        self.airline = airline

        self.seats = {f"S{n}": Seat(f"S{n}") for n in range(1, seat_count + 1)}


class FlightManager:
    def __init__(self, file_path="flights.csv"):
        self.file_path = file_path
        self.flights: Dict[str, Flight] = {}
        self.load_flights()

    def load_flights(self):
        try:
            with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    flight = Flight(
                        flight_number=row["flight_number"],
                        origin=row["origin"],
                        destination=row["destination"],
                        price=float(row["price"]),
                        date=row["date"],
                        departure_time=row["departure_time"],
                        duration=row["duration"],
                        airline=row["airline"]
                    )
                    flight.flight_id = row["flight_id"]
                    self.flights[flight.flight_id] = flight
        except FileNotFoundError:
            pass

    def save_flights(self):
        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = [
                "flight_id","flight_number","origin","destination",
                "price","date","departure_time","duration","airline"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for f in self.flights.values():
                writer.writerow({
                    "flight_id": f.flight_id,
                    "flight_number": f.flight_number,
                    "origin": f.origin,
                    "destination": f.destination,
                    "price": f.price,
                    "date": f.date,
                    "departure_time": f.departure_time,
                    "duration": f.duration,
                    "airline": f.airline
                })

    def add_flight(self, admin: User, flight: Flight):
        if admin.role != "admin":
            print("Access denied. Admin only.")
            return False

        self.flights[flight.flight_id] = flight
        self.save_flights()
        print("Flight added successfully")
        return True

    def edit_flight(self, admin: User, flight_id: str, **updates):
        if admin.role != "admin":
            print("Access denied. Admin only.")
            return False

        if flight_id not in self.flights:
            print("Flight not found")
            return False

        flight = self.flights[flight_id]

        for key, value in updates.items():
            if hasattr(flight, key):
                setattr(flight, key, value)

        self.save_flights()
        print("Flight updated successfully")
        return True

    def delete_flight(self, admin: User, flight_id: str):
        if admin.role != "admin":
            print("Access denied. Admin only.")
            return False

        if flight_id in self.flights:
            del self.flights[flight_id]
            self.save_flights()
            print("Flight deleted")
            return True

        print("Flight not found")
        return False

    def list_flights(self):
        for f in self.flights.values():
            print(f"{f.flight_number} | {f.origin} -> {f.destination} | {f.price} | {f.date} {f.departure_time}")

