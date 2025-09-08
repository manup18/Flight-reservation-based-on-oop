class Flight:
    def __init__(self, num="", dep="", dest="", seats=0, price=0.0):
        self.flight_number = num
        self.departure = dep
        self.destination = dest
        self.available_seats = seats
        self.seat_price = price

    def display_flight_details(self):
        print(f"FLIGHT_NUMBER: {self.flight_number}")
        print(f"DEPARTURE: {self.departure}")
        print(f"DESTINATION: {self.destination}")
        print(f"AVAILABLE SEATS: {self.available_seats}")
        print(f"PRICE: {self.seat_price}")

    def check_availability(self, seats_requested):
        return seats_requested <= self.available_seats

    def book_seats(self, seats):
        self.available_seats -= seats

    def get_flight_number(self):
        return self.flight_number

    def get_seat_price(self):
        return self.seat_price


class LocalFlight(Flight):
    def __init__(self, num, dep, dest, seats, price):
        super().__init__(num, dep, dest, seats, price)

    def display_flight_details(self):
        print("LOCAL FLIGHT")
        super().display_flight_details()


class InternationalFlight(Flight):
    def __init__(self, num, dep, dest, seats, price, passport="Required"):
        super().__init__(num, dep, dest, seats, price)
        self.passport = passport

    def display_flight_details(self):
        print("INTERNATIONAL FLIGHT")
        super().display_flight_details()
        print(f"Passport required: {self.passport}")


class Passenger:
    def __init__(self, name, mail, passenger_id, mobile=None):
        self.passenger_name = name
        self.passenger_email = mail
        self.passenger_id = passenger_id
        self.mobile_number = mobile

    def get_passenger_id(self):
        return self.passenger_id

    def display_passenger_info(self):
        print(f"PASSENGER_ID: {self.passenger_id}")
        print(f"PASSENGER_NAME: {self.passenger_name}")


class Reservation:
    def __init__(self, flight, passenger, seats, reservation_id):
        self.flight = flight
        self.passenger = passenger
        self.num_seats = seats
        self.reservation_id = reservation_id

    def confirm_reservation(self):
        if self.flight.check_availability(self.num_seats):
            self.flight.book_seats(self.num_seats)
            print(f"Reservation confirmed for {self.num_seats} seats on flight {self.flight.get_flight_number()}")
            return True
        else:
            print("Not enough seats available!")
            return False

    def display_reservation_details(self):
        print(f"Reservation ID: {self.reservation_id}")
        print(f"Customer: {self.passenger.get_passenger_id()}")
        print(f"Flight: {self.flight.get_flight_number()}")
        print(f"Seats: {self.num_seats}")


class Payment:
    def __init__(self, amount=0.0):
        self.amount = amount
        self.payment_status = False

    def process_payment(self):
        raise NotImplementedError("Subclasses must implement process_payment method")

    def is_payment_successful(self):
        return self.payment_status


class CreditCardPayment(Payment):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.card_number = card_number

    def process_payment(self):
        print(f"Processing credit card payment of ${self.amount} with card: {self.card_number}...")
        self.payment_status = True
        print("Payment successful!")


class OnlinePayment(Payment):
    def __init__(self, amount, account):
        super().__init__(amount)
        self.online_account = account

    def process_payment(self):
        print(f"Processing online payment of Rs.{self.amount} using Online account: {self.online_account}...")
        self.payment_status = True
        print("Payment successful!")


class Ticket:
    def __init__(self, ticket_id, reservation):
        self.ticket_id = ticket_id
        self.reservation = reservation

    def generate_ticket(self):
        print("\n------ Ticket Generated ------")
        print(f"Ticket ID: {self.ticket_id}")
        self.reservation.display_reservation_details()
        print("-----------------------------")


# -------- Main Menu Driven Program --------
if __name__ == "__main__":
    # Predefined flights
    flights = [
        LocalFlight("AI101", "Mumbai", "Delhi", 50, 5000),
        InternationalFlight("AI202", "Pune", "Dubai", 30, 15000),
        LocalFlight("AI303", "Chennai", "Bangalore", 40, 3000),
    ]

    print("Welcome to Flight Reservation System ✈️\n")
    print("Available Flights:")
    for i, f in enumerate(flights, start=1):
        print(f"\nOption {i}:")
        f.display_flight_details()

    choice = int(input("\nEnter the option number of the flight you want to book: ")) - 1
    selected_flight = flights[choice]

    # Passenger info
    name = input("Enter passenger name: ")
    email = input("Enter passenger email: ")
    pid = input("Enter passenger ID: ")
    seats = int(input("Enter number of seats to book: "))

    passenger = Passenger(name, email, pid)

    reservation = Reservation(selected_flight, passenger, seats, "R001")
    if reservation.confirm_reservation():
        total_amount = seats * selected_flight.get_seat_price()
        print(f"Total Amount: {total_amount}")

        print("\nChoose Payment Method:")
        print("1. Credit Card")
        print("2. Online Payment")
        pay_choice = int(input("Enter choice: "))

        if pay_choice == 1:
            card = input("Enter credit card number: ")
            payment = CreditCardPayment(total_amount, card)
        else:
            acc = input("Enter online account ID: ")
            payment = OnlinePayment(total_amount, acc)

        payment.process_payment()

        if payment.is_payment_successful():
            ticket = Ticket("T001", reservation)
            ticket.generate_ticket()
        else:
            print("Payment failed, reservation not completed.")
