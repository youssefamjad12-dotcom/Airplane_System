import streamlit as st
import pandas as pd
import csv
from datetime import datetime

from admin import AdminManager
from customer import Customer
from flight import FlightManager, Flight
from booking import BookingManager
from ticket import TicketSystem
from payment import PaymentManager
from report import ReportManager

manager = AdminManager()
manager.add_admin("admin", "adminpass", "Primary Admin")

def get_existing_users():
    """Returns a list of dictionaries containing all registered users."""
    users = []
    try:
        with open("users.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        pass
    return users

if 'initialized' not in st.session_state:
    st.session_state.flight_mgr = FlightManager()
    st.session_state.admin_mgr = AdminManager()
    st.session_state.booking_mgr = BookingManager()
    st.session_state.payment_mgr = PaymentManager()
    st.session_state.ticket_sys = TicketSystem(st.session_state.booking_mgr, st.session_state.flight_mgr)
    st.session_state.user = None
    st.session_state.role = None 
    st.session_state.initialized = True

st.set_page_config(page_title="Airline Management System", layout="wide")

st.markdown("""
    <style>
      .stApp {
        background-color: #001f3f;
        }
    /* 1. Sidebar Styling: Deep Blue Background */
    [data-testid="stSidebar"] {
        background-color: #0d1b2a; 
        color: white;
    }
    
    /* Ensure all sidebar text, headers, and labels are white */
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3, 
    [data-testid="stSidebar"] .stMarkdown h4, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio p {
        color: white !important;
    }

    /* 2. Metric Styling: Professional Light Cards (Main Area) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 8px; /* Slightly rounder for a modern look */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stMetric"] label { 
        color: #333 !important; 
        font-weight: 600; 
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { 
        color: #007bff !important; /* Blue text for the actual dollar amount */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Airline Management System")

with st.sidebar:
    st.header("System Access")
    if st.session_state.user is None:
        login_type = st.radio("Access Level:", ["Customer", "Administrator"])
        
        user_name = st.text_input("Full Name (For Registration)")
        email_input = st.text_input("Email / Username")
        password_input = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                if login_type == "Administrator":
                    res = st.session_state.admin_mgr.login(email_input, password_input)
                    if res:
                        st.session_state.user = res
                        st.session_state.role = "admin"
                        # Consistency fix: ensure admin has a role attribute
                        st.session_state.user.role = "admin"
                        st.rerun()
                    else:
                        st.error("Authentication failed: Invalid administrator credentials.")
                else:
                    res = Customer.login(email_input, password_input)
                    if res:
                        st.session_state.user = res
                        st.session_state.role = "customer"
                        if not hasattr(st.session_state.user, 'wallet'):
                            st.session_state.user.wallet = 10000.0 
                        st.rerun()
                    else:
                        st.error("Authentication failed: User not found or incorrect password.")
        
        with col2:
            if login_type == "Customer":
                if st.button("Register", use_container_width=True):
                    if not user_name or not email_input or not password_input:
                        st.warning("All fields are required for registration.")
                    else:
                        existing_users = get_existing_users()
                        name_exists = any(u['name'].lower() == user_name.lower() for u in existing_users)
                        email_exists = any(u['email'].lower() == email_input.lower() for u in existing_users)
                        
                        if name_exists:
                            st.error("Registration Error: This name is already registered.")
                        elif email_exists:
                            st.error("Registration Error: This email address is already in use.")
                        else:
                            Customer.register(user_name, email_input, password_input)
                            st.success("Account created successfully. You may now login.")
    else:
        st.info(f"Session Active: {st.session_state.user.name}")
        if st.button("Terminate Session", use_container_width=True):
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

if st.session_state.user is None:
    st.info("Please provide valid credentials via the sidebar to access system modules.")

elif st.session_state.role == "admin":
    st.subheader("Administrative Control Panel")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Reports", "Active Flights", "Add Flight", "Modify Flight", "Bookings","Delete Flight"])
    
    with tab1:
        st.markdown("#### System Statistics")
        rep = ReportManager(flight_manager=st.session_state.flight_mgr, booking_manager=st.session_state.booking_mgr)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Registered Customers", rep.load_customers_count())
        c2.metric("Total Administrators", rep.load_admins_count())
        c3.metric("Available Flights", rep.flights_count())
        c4.metric("Active Bookings", rep.bookings_count())

    with tab2:
        st.markdown("#### Active Flight List")
        flights = st.session_state.flight_mgr.flights
        if flights:
            for f_id, f in flights.items():
                with st.expander(f"Flight {f.flight_number}: {f.origin} to {f.destination}"):
                
                    # Unique key fixed
                    if st.button("View Details", key=f"view_flight_{f_id}"):
                        st.write(f"**Flight Number:** {f.flight_number}")
                        st.write(f"**Origin:** {f.origin}")
                        st.write(f"**Destination:** {f.destination}")
                        st.write(f"**Price:** ${f.price}")
                        st.write(f"**Scheduled Date:** {f.date}")
                        st.write(f"**Scheduled Time:** {f.duration}")
                        st.write(f"**Airline:** {f.airline}")
        else:
            st.info("No flight records available.")

    with tab3:
        st.markdown("#### Define New Flight Path")
        with st.form("new_flight"):
            c1, c2 = st.columns(2)
            f_num = c1.text_input("Flight ID")
            f_air = c2.text_input("Carrier Name")
            f_org = c1.text_input("Departure City")
            f_dest = c2.text_input("Arrival City")
            f_price = c1.number_input("Unit Price ($)", min_value=0.0)
            f_dur = c2.time_input("Estimated Duration")
            f_date = c1.date_input("Scheduled Date")
            f_time = c2.time_input("Scheduled Time")
            if st.form_submit_button("Submit to Registry"):
                new_f = Flight(f_num, f_org, f_dest, f_price, str(f_date), str(f_time), f_dur, f_air)
                st.session_state.user.role = "admin"
                st.session_state.flight_mgr.add_flight(st.session_state.user, new_f)
                st.success("New flight entry successfully recorded.")

    with tab4:
        st.markdown("#### Modify Existing Records")
        flights = st.session_state.flight_mgr.flights
        if flights:
            target = st.selectbox("Select Flight ID", options=list(flights.keys()), format_func=lambda x: flights[x].flight_number)
            f = flights[target]
            with st.form("edit_flight"):
                n_price = st.number_input("Update Price", value=float(f.price))
                n_dur = st.text_input("Update Duration", value=f.duration)
                n_orig = st.text_input("Update Origin", value=f.origin)
                n_dest = st.text_input("Update Destination", value=f.destination)
                if st.form_submit_button("Apply Updates"):
                    st.session_state.user.role = "admin"
                    st.session_state.flight_mgr.edit_flight(st.session_state.user, target, price=n_price, duration=n_dur, origin=n_orig, destination=n_dest)
                    st.success("Record updated.")
                    st.rerun()
        else:
            st.info("No flight records available for modification.")

    with tab5:
        st.markdown("#### Booking Registry Management")
    
        if not st.session_state.booking_mgr.bookings:
            st.info("No booking records available.")
        else:
            # Column headers for the "Labels" look
            h1, h2, h3, h4 = st.columns([1, 2, 1, 1])
            h1.caption("BOOKING ID")
            h2.caption("CUSTOMER EMAIL")
            h3.caption("SEAT")
            h4.caption("ACTIONS")
            st.divider()

            for b in st.session_state.booking_mgr.bookings:
                cols = st.columns([1, 2, 1, 1])
                with cols[0]:
                    st.markdown(f"`{b.booking_id}`")
                with cols[1]:
                    st.markdown(f"**{b.customer_username}**")
                with cols[2]:
                    st.markdown(f"🏷️ `{b.seat_no}`")
                with cols[3]:
                    # Unique key fixed to avoid DuplicateWidgetID
                    if st.button("Cancel", key=f"cancel_bk_{b.booking_id}", type="secondary", use_container_width=True):
                        # Add your cancellation logic here if needed
                        st.session_state.booking_mgr.bookings.remove(b)
                        st.session_state.booking_mgr.save_bookings()
                        st.success(f"Booking {b.booking_id} has been cancelled.")

                st.divider()
        
    with tab6:
        st.markdown("### Terminate Flight Registry")
        active_flights = st.session_state.flight_mgr.flights
    
        if not active_flights:
            st.info("No records available for deletion.")
        else:
            st.warning("Action Warning: Deleting a flight is permanent.")
        
            for f_id, f in active_flights.items():
                with st.container(border=True):
                    col_info, col_action = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"**Flight Number:** `{f.flight_number}`")
                        st.write(f"**Route:** {f.origin} ➝ {f.destination}")
                        st.caption(f"Carrier: {f.airline} | Scheduled: {f.date}")
                
                    with col_action:
                        if st.button("Delete Record", key=f"tab6_del_{f_id}", type="primary", use_container_width=True):
                            if not hasattr(st.session_state.user, 'role'):
                                st.session_state.user.role = "admin"
                            success = st.session_state.flight_mgr.delete_flight(st.session_state.user, f_id)
                            if success:
                                st.success(f"Flight {f.flight_number} removed.")
                                st.rerun()
                            else:
                                st.error("Failed to delete.")

elif st.session_state.role == "customer":
    st.subheader(f"Welcome {st.session_state.user.name}.")
    tab1, tab2, tab3 = st.tabs(["Flight Search", "My Reservations", "Financial History"])
    
    user_booked_ids = [
        b.flight_id for b in st.session_state.booking_mgr.bookings 
        if b.customer_username == st.session_state.user.email
    ]
    
    with tab1:
        st.markdown("#### Available Flight Schedules")
        for f_id, f in st.session_state.flight_mgr.flights.items():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"**{f.origin} to {f.destination}** ({f.airline})")
                c2.write(f"Price: ${f.price}")
                
                is_booked = f_id in user_booked_ids
                
                if is_booked:
                    c3.button("Already Booked", key=f"btn_{f_id}", disabled=True)
                else:
                    if c3.button("Confirm Booking", key=f"cust_bk_{f_id}"):
                        if not hasattr(st.session_state.user, 'username'):
                            st.session_state.user.username = st.session_state.user.email
                        
                        if st.session_state.payment_mgr.make_payment(st.session_state.user, f):
                            st.session_state.booking_mgr.create_booking(
                                st.session_state.user.email, 
                                st.session_state.flight_mgr, 
                                f_id, 
                                "S1"
                            )
                            st.success("Reservation confirmed.")
                            st.rerun()
                        else:
                            st.error("Insufficient funds.")
        else:
            st.warning("No flights available for booking.")

    with tab2:
        st.markdown("#### Active Boarding Passes")
        has_bookings = False
        for b in st.session_state.booking_mgr.bookings:
            if b.customer_username == st.session_state.user.email:
                f = st.session_state.flight_mgr.flights.get(b.flight_id)
                if f:
                    with st.expander(f"Booking ID: {b.booking_id} | Flight: {f.flight_number}"):
                        st.write(f"**Route:** {f.origin} ➝ {f.destination}")
                        st.write(f"**Date:** {f.date} | **Time:** {f.duration}")
                        st.write(f"**Seat Number:** {b.seat_no}")
                        st.write(f"**Price Paid:** ${f.price}")
                has_bookings = True
        st.warning("Note: Contact the airline for any changes.")
        if not has_bookings:
            st.write("No active reservations found.")

    with tab3:
        st.markdown("#### Wallet Balance")
        st.metric("Available Funds", f"${st.session_state.user.wallet:,.2f}")