import random
from datetime import datetime, timedelta
from faker import Faker
from app import app, db
from models import User, Aircraft, Airport, Flight, Seat, Booking, BookingDetail, Payment
from sqlalchemy.orm import joinedload

faker = Faker()
CURRENT_DATE = datetime(2025, 3, 29)
print(CURRENT_DATE)
def generate_booking_reference():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

# Define default users
default_users = [
    ("johndoe", "john@example.com", "John", "Doe", "Gold", 25000, False),
    ("janedoe", "jane@example.com", "Jane", "Doe", "Silver", 12000, False),
    ("admin", "admin@example.com", "Admin", "User", "Platinum", 50000, True)
]

# Wrap the entire script in an application context
with app.app_context():
    # 1. Clear existing data
    db.drop_all()
    db.create_all()

    # 2. Insert Users (3 default users + 97 random users to make 100 total)
    users = []

    # Define date ranges
    start_date = datetime(2024, 12, 24)  # Start of the 3-month period
    last_week_start = datetime(2025, 3, 18)  # Start of the last week
    end_date = CURRENT_DATE  # End of the period (March 24, 2025)

    # Total users to create
    total_users = 100
    default_users_count = len(default_users)  # 3 default users
    random_users_count = total_users - default_users_count  # 97 random users

    # Distribute users: 70% in the first period, 30% in the last week
    users_in_first_period = int(total_users * 0.7)  # 70 users
    users_in_last_week = total_users - users_in_first_period  # 30 users

    # Split default users proportionally between the two periods
    default_users_in_first_period = int(default_users_count * 0.7)  # 2 default users
    default_users_in_last_week = default_users_count - default_users_in_first_period  # 1 default user

    # Split random users proportionally
    random_users_in_first_period = users_in_first_period - default_users_in_first_period  # 68 random users
    random_users_in_last_week = users_in_last_week - default_users_in_last_week  # 29 random users

    # Add default users
    default_users_first_period = default_users[:default_users_in_first_period]
    default_users_last_week = default_users[default_users_in_first_period:]

    # Add default users for the first period (Dec 24, 2024 - Mar 17, 2025)
    for username, email, first_name, last_name, frequent_flyer_status, frequent_flyer_miles, is_admin in default_users_first_period:
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=80),
            phone_number=faker.phone_number()[:20],
            address=faker.address()[:200],
            passport_number=faker.passport_number(),
            nationality=faker.country()[:50],
            frequent_flyer_status=frequent_flyer_status,
            frequent_flyer_miles=frequent_flyer_miles,
            date_joined=faker.date_time_between(start_date=start_date, end_date=last_week_start),
            is_admin=is_admin
        )
        user.set_password("password123")
        users.append(user)

    # Add default users for the last week (Mar 18, 2025 - Mar 24, 2025)
    for username, email, first_name, last_name, frequent_flyer_status, frequent_flyer_miles, is_admin in default_users_last_week:
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=80),
            phone_number=faker.phone_number()[:20],
            address=faker.address()[:200],
            passport_number=faker.passport_number(),
            nationality=faker.country()[:50],
            frequent_flyer_status=frequent_flyer_status,
            frequent_flyer_miles=frequent_flyer_miles,
            date_joined=faker.date_time_between(start_date=last_week_start, end_date=end_date),
            is_admin=is_admin
        )
        user.set_password("password123")
        users.append(user)

    # Add random users for the first period (Dec 24, 2024 - Mar 17, 2025)
    used_usernames = {user.username for user in users}
    for i in range(random_users_in_first_period):
        while True:
            username = faker.user_name()
            if username not in used_usernames:
                used_usernames.add(username)
                break
        user = User(
            username=username,
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=80),
            phone_number=faker.phone_number()[:20],
            address=faker.address()[:200],
            passport_number=faker.passport_number(),
            nationality=faker.country()[:50],
            frequent_flyer_status=random.choice(['Standard', 'Silver', 'Gold', 'Platinum']),
            frequent_flyer_miles=random.randint(0, 10000),
            date_joined=faker.date_time_between(start_date=start_date, end_date=last_week_start),
            is_admin=False  # First 2 random users are admins
        )
        user.set_password(faker.password())
        users.append(user)

    # Add random users for the last week (Mar 18, 2025 - Mar 24, 2025)
    for i in range(random_users_in_last_week):
        while True:
            username = faker.user_name()
            if username not in used_usernames:
                used_usernames.add(username)
                break
        user = User(
            username=username,
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=80),
            phone_number=faker.phone_number()[:20],
            address=faker.address()[:200],
            passport_number=faker.passport_number(),
            nationality=faker.country()[:50],
            frequent_flyer_status=random.choice(['Standard', 'Silver', 'Gold', 'Platinum']),
            frequent_flyer_miles=random.randint(0, 10000),
            date_joined=faker.date_time_between(start_date=last_week_start, end_date=end_date),
            is_admin=False
        )
        user.set_password(faker.password())
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # 3. Insert Aircrafts (10 aircrafts)
    aircrafts = []
    used_registrations = set()
    for i in range(10):
        while True:
            registration = faker.bothify(text='N####??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if registration not in used_registrations:
                used_registrations.add(registration)
                break
        aircraft = Aircraft(
            model=faker.bothify(text='Model-###'),
            registration=registration,
            economy_seats=random.randint(100, 150),
            business_seats=random.randint(20, 50),
            first_class_seats=random.randint(0, 20)
        )
        aircrafts.append(aircraft)
    db.session.add_all(aircrafts)
    db.session.commit()

    # 4. Insert Airports (using real airports_data)
    airports = []
    airports_data = [
        ("JFK", "John F. Kennedy International Airport", "New York", "USA"),
        ("LHR", "Heathrow Airport", "London", "United Kingdom"),
        ("NRT", "Narita International Airport", "Tokyo", "Japan"),
        ("SYD", "Sydney Kingsford Smith Airport", "Sydney", "Australia"),
        ("CDG", "Charles de Gaulle Airport", "Paris", "France"),
        ("DXB", "Dubai International Airport", "Dubai", "United Arab Emirates"),
        ("SIN", "Changi Airport", "Singapore", "Singapore"),
    ]
    for code, name, city, country in airports_data:
        airport = Airport(
            code=code,
            name=name,
            city=city,
            country=country
        )
        airports.append(airport)
    db.session.add_all(airports)
    db.session.commit()

    # 5. Insert Flights (189 flights over 4 months)
    flights = []
    for i in range(595):
        origin = random.choice(airports)
        destination = random.choice([a for a in airports if a != origin])
        departure_time = faker.date_time_between(start_date=datetime(2024, 12, 29), end_date=datetime(2025, 4, 29))
        duration = random.randint(1, 15)
        arrival_time = departure_time + timedelta(hours=duration)
        economy_base_price = float(random.randint(100, 500))
        business_base_price = economy_base_price * 2.5
        first_class_base_price = economy_base_price * 4.0
        status = "Scheduled" if departure_time > CURRENT_DATE else random.choices(["Completed", "Cancelled"], weights=[80, 20])[0]
        
        flight = Flight(
            flight_number=f"SW{i+100}",
            aircraft_id=random.randint(1, len(aircrafts)),
            origin_id=origin.id,
            destination_id=destination.id,
            departure_time=departure_time,
            arrival_time=arrival_time,
            economy_base_price=economy_base_price,
            business_base_price=business_base_price,
            first_class_base_price=first_class_base_price,
            status=status
        )
        flights.append(flight)
    db.session.add_all(flights)
    db.session.commit()

    # 5.1 Insert Seats for each Flight
    flights = Flight.query.all()
    for flight in flights:
        if Seat.query.filter_by(flight_id=flight.id).count() > 0:
            continue

        aircraft = Aircraft.query.get(flight.aircraft_id)

        # Economy Seats (3-3 configuration starting from row 10)
        for i in range(1, aircraft.economy_seats + 1):
            row = (i - 1) // 6 + 10
            col = chr(65 + ((i - 1) % 6))
            seat = Seat(
                flight_id=flight.id,
                seat_number=f"{row}{col}",
                seat_class="Economy",
                is_booked=False
            )
            db.session.add(seat)

        # Business Seats (2-2 configuration starting from row 3)
        for i in range(1, aircraft.business_seats + 1):
            row = (i - 1) // 4 + 3
            col = chr(65 + ((i - 1) % 4))
            seat = Seat(
                flight_id=flight.id,
                seat_number=f"{row}{col}",
                seat_class="Business",
                is_booked=False
            )
            db.session.add(seat)

        # First Class Seats (1-1 configuration starting from row 1)
        for i in range(1, aircraft.first_class_seats + 1):
            row = (i - 1) // 2 + 1
            col = chr(65 + ((i - 1) % 2) * 3)
            seat = Seat(
                flight_id=flight.id,
                seat_number=f"{row}{col}",
                seat_class="First Class",
                is_booked=False
            )
            db.session.add(seat)

    db.session.commit()

    # 6. Insert Bookings (5000 bookings over past 3 months)
    bookings = []
    booking_details = []
    payments = []
    seat_classes = ["Economy", "Business", "First Class"]
    statuses = ["Reserved", "Confirmed", "Cancelled"]
    used_booking_references = set()

    flights = Flight.query.options(joinedload(Flight.aircraft)).all()

    bookings_per_flight = 5000 // len(flights)
    remaining_bookings = 5000 % len(flights)

    flight_index = 0
    for i in range(5000):
        user_id = random.randint(1, len(users))
        flight_id = (flight_index % len(flights)) + 1
        flight = next(f for f in flights if f.id == flight_id)
        flight_index += 1

        booking_date = faker.date_time_between(start_date=datetime(2024, 12, 24), end_date=CURRENT_DATE)
        
        initial_status = random.choices(statuses, weights=[15, 80, 5])[0]
        
        if flight.status == "Cancelled" and flight.departure_time < CURRENT_DATE:
            status = "Cancelled"
        elif flight.departure_time < CURRENT_DATE and initial_status == "Reserved":
            status = "Cancelled"
        else:
            status = initial_status

        seat_class = random.choices(seat_classes, weights=[61, 32, 7])[0]
        days_before = (flight.departure_time - booking_date).days
        if days_before < 0:
            days_before = 0
        price = flight.calculate_price(seat_class, days_before)

        # Query an available seat for the selected class
        available_seat = Seat.query.filter_by(
            flight_id=flight.id,
            seat_class=seat_class,
            is_booked=False
        ).first()

        # If no seat is available in the preferred class, try another class
        if not available_seat:
            if seat_class == "First Class":
                seat_class = "Business"
                available_seat = Seat.query.filter_by(
                    flight_id=flight.id,
                    seat_class=seat_class,
                    is_booked=False
                ).first()
            if not available_seat:
                seat_class = "Economy"
                available_seat = Seat.query.filter_by(
                    flight_id=flight.id,
                    seat_class=seat_class,
                    is_booked=False
                ).first()
        
        if not available_seat:
            continue

        seat_id = available_seat.id
        price = flight.calculate_price(seat_class, days_before)

        while True:
            booking_ref = generate_booking_reference()
            if booking_ref not in used_booking_references:
                used_booking_references.add(booking_ref)
                break

        booking = Booking(
            booking_reference=booking_ref,
            user_id=user_id,
            flight_id=flight_id,
            booking_date=booking_date,
            status=status,
            total_price=price,
            payment_status="Paid" if status == "Confirmed" else "Pending"
        )
        bookings.append(booking)

        user = User.query.get(user_id)
        booking_detail = BookingDetail(
            booking_id=i + 1,
            seat_id=seat_id,
            passenger_first_name=user.first_name,
            passenger_last_name=user.last_name,
            passenger_dob=faker.date_of_birth(minimum_age=18, maximum_age=80),
            passenger_passport=faker.passport_number(),
            passenger_nationality=faker.country(),
            price=price
        )
        booking_details.append(booking_detail)

        if status != "Cancelled":
            available_seat.is_booked = True

        if status == "Confirmed":
            payment = Payment(
                booking_id=i + 1,
                amount=price,
                payment_date=booking_date,
                payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
                transaction_id=f"TXN{i+1000}",
                status="Completed"
            )
            payments.append(payment)

        if status == "Cancelled" and random.random() < 0.2:
            payment = Payment(
                booking_id=i + 1,
                amount=price,
                payment_date=booking_date,
                payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
                transaction_id=f"TXN{i+1000}",
                status="Refunded"
            )
            payments.append(payment)

    db.session.add_all(bookings)
    db.session.commit()

    for i, booking in enumerate(bookings):
        booking_detail = booking_details[i]
        booking_detail.booking_id = booking.id
        if i < len(payments):
            payments[i].booking_id = booking.id

    db.session.add_all(booking_details)
    db.session.add_all(payments)
    db.session.commit()

    print("Database seeded successfully!")