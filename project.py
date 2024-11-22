import streamlit as st
import pandas as pd
import altair as alt
import uuid
from datetime import datetime, timedelta
from fpdf import FPDF

# Set page configuration
st.set_page_config(
    page_title="Coffee Shop App",
    page_icon="☕",
    layout="wide"
)

# Background styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f7f5f2;
    background-image: linear-gradient(to bottom, #f7f5f2, #d9cbb6);
}
[data-testid="stSidebar"] {
    background-color: #ebe7e1;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Simulated data for inventory and sales
inventory = {
    "Signature Coffee": {"price": 10.00, "stock": 50, "image": "https://www.shutterstock.com/image-photo/coffee-mug-grinded-beans-concept-600nw-2500190129.jpg", "ingredients": {"coffee_beans": 0.1, "milk": 0.05}},
    "Americano": {"price": 5.00, "stock": 100, "image": "https://www.oddbeans.in/cdn/shop/articles/image1_9a1a2488-7d3e-49e6-ae4a-babcc1c17218.jpg?v=1721478108&width=1100", "ingredients": {"coffee_beans": 0.1, "milk": 0.05}},
    "Cappuccino": {"price": 6.00, "stock": 50, "image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Cappuccino_at_Sightglass_Coffee.jpg", "ingredients": {"coffee_beans": 0.1, "milk": 0.1}},
    "Latte": {"price": 6.50, "stock": 75, "image": "https://media.istockphoto.com/id/1152767411/photo/cup-of-coffee-latte-isolated-on-white-background-with-clipping-path.jpg?s=612x612&w=0&k=20&c=24HBAvkahjo8LKV-6DRUklQzPJUqxjmVlBFtV5BG4tU=", "ingredients": {"coffee_beans": 0.1, "milk": 0.2}},
    "Caramel Macchiato": {"price": 7.00, "stock": 30, "image": "https://cooktoria.com/wp-content/uploads/2016/02/Caramel-Macchiato-Recipe-sq-1.jpg", "ingredients": {"coffee_beans": 0.1, "milk": 0.1, "syrup": 0.05}},
    "Espresso": {"price": 5.00, "stock": 30, "image": "https://pizza-boy.co.uk/wp-content/uploads/2024/01/expresso-324x243.jpg", "ingredients": {"coffee_beans": 0.1, "milk": 0.1, "syrup": 0.05}}
}

# Initialize session state
if "sales" not in st.session_state:
    st.session_state.sales = []
if "orders" not in st.session_state:
    st.session_state.orders = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "customers" not in st.session_state:
    st.session_state.customers = {}

# App title with emoji
st.markdown("<h1 style='text-align: center;'>☕ Welcome to Starlit Sips Coffee Shop App</h1>", unsafe_allow_html=True)

# Sidebar navigation
menu_option = st.sidebar.radio("Navigate", [
    "About", "Customer Order", "Inventory Management", 
    "Sales Report", "Admin Access", "Feedback", "Promotions & Discounts"
])

# About Page Content
if menu_option == "About":
    st.header("About Starlit Sips Coffee Shop 🌟")
    st.write("""
    Welcome to **Starlit Sips**, a place where every cup of coffee tells a story.
    
    **Our Mission**:
    At Starlit Sips, we are committed to providing the finest quality coffee, crafted with care and passion. Our mission is to offer a warm and inviting atmosphere where you can enjoy freshly brewed coffee, delicious pastries, and a variety of beverages to suit every taste.

    **What Makes Us Unique?**
    - **Locally Sourced Beans**: We believe in supporting local farmers and sustainable practices. Our beans are sourced from the best local coffee producers.
    - **Expertly Crafted**: Our baristas are coffee aficionados who take pride in perfecting every cup.
    - **Comfortable Ambience**: Whether you're here to relax, work, or meet friends, Starlit Sips offers a cozy, modern space to unwind.
    - **Customizable Drinks**: We offer a range of customizable options to make your coffee just the way you like it.
    
    **Our Story**:
    Founded in 2024, Starlit Sips began as a small local coffee shop with a big dream — to share the joy of high-quality coffee with our community. What started as a humble endeavor has now grown into a beloved spot for coffee lovers, students, and professionals alike.
    
    Come visit us and experience the perfect cup of coffee, made just for you. Whether it's your first time or you're a regular, you're always welcome at Starlit Sips.
    """)
    
    # Adding an image to the About page
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://www.shutterstock.com/image-photo/coffee-mug-grinded-beans-concept-600nw-2500190129.jpg" style="width: 50%; border-radius: 10px;" alt="Coffee Mug">
            <p style="font-size: 20px; font-weight: bold; margin-top: 10px;">Our Signature Coffee: Starlit Sips Brew</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Customer Order Process
elif menu_option == "Customer Order":
    st.header("Place Your Order 📋")
    st.write("Browse through our menu and place your order!")
    
    # Display items with images and details
    for item_name, details in inventory.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(details["image"], caption=item_name, width=400)  # Updated width to 150
        with col2:
            st.write(f"**{item_name}**")
            st.write(f"Price: ${details['price']:.2f}")
            st.write(f"Stock Available: {details['stock']} cups")

            # Allow customer to select size (small, medium, large)
            size = st.selectbox("Select Size", ["Small", "Medium", "Large"], key=f"size_{item_name}")
            add_ons = st.multiselect("Add-ons (Optional)", ["Extra Sugar", "Extra Milk", "Syrup","Whipped Cream","Vanilla Syrup","Caramel Syrup","Almond Milk",""], key=f"addons_{item_name}")

            # Allow user to select quantity
            qty = st.number_input(
                f"Select Quantity for {item_name}",
                min_value=0,
                max_value=details["stock"],
                step=1,
                key=f"qty_{item_name}"
            )

            if st.button(f"Add {item_name} to Order", key=f"btn_{item_name}"):
                if qty > 0:
                    order_id = str(uuid.uuid4())  # Generate unique order ID
                    prep_time = datetime.now() + timedelta(minutes=5)  # Set prep time
                    order = {
                        "order_id": order_id,
                        "item": item_name,
                        "size": size,
                        "addons": add_ons,
                        "quantity": qty,
                        "price": details["price"],
                        "total": qty * details["price"],
                        "prep_time": prep_time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.orders.append(order)
                    inventory[item_name]["stock"] -= qty  # Update stock
                    st.success(f"Order #{order_id} placed! Estimated pickup time: {prep_time.strftime('%H:%M:%S')}")
                else:
                    st.warning(f"Please select a valid quantity for {item_name}.")

    # Order History for Registered Customers
    st.subheader("Order History")
    customer_name = st.text_input("Enter your name (for repeat customers)")
    if customer_name:
        if customer_name in st.session_state.customers:
            order_history = st.session_state.customers[customer_name]
            st.write("Previous Orders:")
            st.write(order_history)
        else:
            st.warning(f"No previous orders found for {customer_name}.")

# Inventory Management
elif menu_option == "Inventory Management":
    st.header("Manage Inventory 📦")

    # Display current inventory
    inventory_df = pd.DataFrame(inventory).T
    st.write("Current Inventory Status:")
    st.dataframe(inventory_df)

    # Admin update inventory
    st.subheader("Update Inventory:")
    item_to_update = st.selectbox("Select Item to Update", list(inventory.keys()))
    new_stock = st.number_input(f"New Stock for {item_to_update}", min_value=0)
    new_price = st.number_input(f"New Price for {item_to_update}", min_value=0.01)
    
    if st.button(f"Update {item_to_update} Inventory"):
        if new_stock >= 0 and new_price > 0:
            inventory[item_to_update]["stock"] = new_stock
            inventory[item_to_update]["price"] = new_price
            st.success(f"Updated {item_to_update} inventory.")
        else:
            st.error("Invalid input. Please check the values.")

# Sales Report
elif menu_option == "Sales Report":
    st.header("Sales Report 📊")

    # Generating a simple sales summary
    total_sales = sum(order["total"] for order in st.session_state.orders)
    st.write(f"Total Sales: ${total_sales:.2f}")

    # Display sales details in a table
    if st.session_state.orders:
        sales_df = pd.DataFrame(st.session_state.orders)
        st.dataframe(sales_df)

# Admin Access (Hidden)
elif menu_option == "Admin Access":
    st.header("Admin Access 🔑")
    password = st.text_input("Enter Admin Password", type="password")
    if password == "admin123":  # Simple admin check
        st.write("Admin Access Granted.")
    else:
        st.warning("Incorrect password.")

# Feedback
elif menu_option == "Feedback":
    st.header("Customer Feedback 📝")
    feedback_text = st.text_area("Please share your feedback about our coffee shop!")
    if st.button("Submit Feedback"):
        if feedback_text:
            st.session_state.feedback.append(feedback_text)
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter some feedback before submitting.")

# Promotions & Discounts
elif menu_option == "Promotions & Discounts":
    st.header("Promotions & Discounts 🎉")
    st.write("""
    - **Happy Hour Special**: 20% off on all drinks from 4 PM to 6 PM.
    - **Loyalty Program**: Get a free drink after every 10 purchases!
    - **Student Discount**: Show your student ID and get 10% off on all drinks.
    """)



