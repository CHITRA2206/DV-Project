import streamlit as st
import pandas as pd
import altair as alt
import uuid
from datetime import datetime, timedelta

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

# Function to generate invoice
def generate_invoice(order, customer_name):
    st.subheader(f"Invoice for Order #{order['order_id']}")
    st.write(f"**Customer Name**: {customer_name}")
    st.write(f"**Item**: {order['item']} ({order['size']})")
    st.write(f"**Quantity**: {order['quantity']}")
    st.write(f"**Price per Item**: ${order['price']:.2f}")
    st.write(f"**Total Cost**: ${order['total']:.2f}")
    
    # Optional: Add more order details or display custom thank you message
    st.write(f"**Add-ons**: {', '.join(order['addons']) if order['addons'] else 'None'}")
    st.write(f"**Estimated Pickup Time**: {order['prep_time']}")
    st.write("\n")
    st.write("Thank you for ordering at Starlit Sips!")
    st.write("We hope you enjoy your coffee! ☕")

# App title with emoji
st.markdown("<h1 style='text-align: center;'>☕ Welcome to Starlit Sips Coffee Shop App</h1>", unsafe_allow_html=True)

# Sidebar navigation
menu_option = st.sidebar.radio("Navigate", [
    "About", "Customer Order", "Inventory Management", 
    "Sales Report", "Feedback", "Promotions & Discounts"
])

# About Page Content
if menu_option == "About":
    st.header("About Starlit Sips Coffee Shop 🌟")
    st.write("""
    Welcome to **Starlit Sips**, a place where every cup of coffee tells a story.

    **Developed By**
    1) Jayaraj A/L Sivakumar (21002538)
    2) Chitra A/P Tamil Chelvan (21002368)
    3) Mohamad Yazid Bin Mohd Rawi (22002584)
    4) Wan Ilhan Haqeem Bin Wan Ahmad Idzham (20000503)
    5) Sudeskh A/L N. Kumar(20002012)

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
if menu_option == "Customer Order":
    st.header("Place Your Order 📋")
    st.write("Browse through our menu and place your order!")

    # Prompt for customer name
    customer_name = st.text_input("Enter Your Name", key="customer_name_input")

    if not customer_name:
        st.warning("Please enter your name before placing an order.")
    else:
        # Display items with images and details
        for item_name, details in inventory.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(details["image"], caption=item_name, width=200)  # Updated width to 150
            with col2:
                st.write(f"**{item_name}**")
                st.write(f"Price: ${details['price']:.2f}")
                st.write(f"Stock Available: {details['stock']} cups")

                # Allow customer to select size (small, medium, large)
                size = st.selectbox("Select Size", ["Small", "Medium", "Large"], key=f"size_{item_name}")
                add_ons = st.multiselect("Add-ons (Optional)", ["Extra Sugar", "Extra Milk", "Syrup", "Whipped Cream", "Vanilla Syrup", "Caramel Syrup", "Almond Milk", ""], key=f"addons_{item_name}")

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

                        # Notify the customer when the order is ready
                        st.session_state.customers[order_id] = {
                            "customer_name": customer_name,
                            "order": order,
                            "status": "Order Received"
                        }
                        # Generate and show the invoice
                        generate_invoice(order, customer_name)

# Display orders with status
# Sales Report with More Graphs
if menu_option == "Sales Report":
    st.header("Sales Report 📊")

    if len(st.session_state.orders) == 0:
        st.write("No orders have been placed yet.")
    else:
        # Create DataFrame from orders data
        orders_df = pd.DataFrame(st.session_state.orders)

        # Total sales per item
        total_sales_df = orders_df.groupby('item').agg({'total': 'sum'}).reset_index()

        # Display total sales table
        st.subheader("Total Sales by Item")
        st.dataframe(total_sales_df)

        # Sales Bar Chart by Item
        bar_chart = alt.Chart(total_sales_df).mark_bar().encode(
            x='item:N',
            y='total:Q',
            color='item:N',
            tooltip=['item:N', 'total:Q']
        ).properties(
            title="Total Sales per Item"
        )
        st.altair_chart(bar_chart, use_container_width=True)

        # Sales by Cup Size (Pie Chart or Bar Chart)
        if 'size' in orders_df.columns:
            sales_by_size_df = orders_df.groupby('size').agg({'total': 'sum'}).reset_index()

            # Pie chart for sales by cup size
            pie_chart = alt.Chart(sales_by_size_df).mark_arc().encode(
                theta='total:Q',
                color='size:N',
                tooltip=['size:N', 'total:Q']
            ).properties(
                title="Sales by Cup Size"
            )
            st.altair_chart(pie_chart, use_container_width=True)

            # Alternatively, a bar chart for sales by cup size
            bar_chart_size = alt.Chart(sales_by_size_df).mark_bar().encode(
                x='size:N',
                y='total:Q',
                color='size:N',
                tooltip=['size:N', 'total:Q']
            ).properties(
                title="Sales by Cup Size (Bar Chart)"
            )
            st.altair_chart(bar_chart_size, use_container_width=True)

        # Sales by Item and Size (Stacked Bar Chart)
        sales_by_item_size_df = orders_df.groupby(['item', 'size']).agg({'total': 'sum'}).reset_index()

        stacked_bar_chart = alt.Chart(sales_by_item_size_df).mark_bar().encode(
            x='item:N',
            y='total:Q',
            color='size:N',
            tooltip=['item:N', 'size:N', 'total:Q']
        ).properties(
            title="Sales by Item and Cup Size"
        )
        st.altair_chart(stacked_bar_chart, use_container_width=True)

        # Average Sales by Size (Bar Chart)
        avg_sales_by_size_df = orders_df.groupby('size').agg({'total': 'mean'}).reset_index()

        avg_sales_bar_chart = alt.Chart(avg_sales_by_size_df).mark_bar().encode(
            x='size:N',
            y='total:Q',
            color='size:N',
            tooltip=['size:N', 'total:Q']
        ).properties(
            title="Average Sales per Cup Size"
        )
        st.altair_chart(avg_sales_bar_chart, use_container_width=True)



# Inventory Management for Admin
if menu_option == "Inventory Management":
    st.header("Inventory Management 🛒")
    st.write("Admin controls to manage inventory and track product stock.")

    # Only show this section if user is admin
    admin_password = st.text_input("Enter Admin Password", type="password", key="admin_password")
    
    # Check admin password
    if admin_password == "admin2024":  # A simple password check (use a more secure method in real apps)
        
        # To display updated inventory after each update
        updated_inventory = inventory.copy()  # Create a copy to store updated inventory
        
        # Show inventory table
        st.subheader("Current Inventory Stock")
        inventory_data = []
        for item_name, details in updated_inventory.items():
            inventory_data.append([item_name, details["price"], details["stock"]])
        
        inventory_df = pd.DataFrame(inventory_data, columns=["Item", "Price ($)", "Stock Available (cups)"])
        st.dataframe(inventory_df)

        # Section to update inventory
        st.subheader("Update Inventory")
        
        # Update stock for each item
        for item_name, details in updated_inventory.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(details["image"], caption=item_name, width=150)
            with col2:
                st.write(f"**{item_name}**")
                st.write(f"Price: ${details['price']:.2f}")
                st.write(f"Stock Available: {details['stock']} cups")
                st.write(f"Ingredients: {', '.join(details['ingredients'].keys())}")

                # Allow updating stock
                new_stock = st.number_input(f"Update Stock for {item_name}", min_value=0, max_value=200, value=details["stock"], key=f"new_stock_{item_name}")
                
                # Update stock when button clicked
                if st.button(f"Update Stock for {item_name}"):
                    updated_inventory[item_name]["stock"] = new_stock
                    inventory[item_name]["stock"] = new_stock  # Update the original inventory
                    st.success(f"Updated stock for {item_name} to {new_stock} cups.")

# Admin Access for Promotions and Discounts
if menu_option == "Promotions & Discounts":
    st.header("🎉 Special Offers & Exclusive Discounts 🎉")
    st.write("Administrators can create, edit, and apply exclusive discounts for loyal customers.")

    st.subheader("Create a Discount Code")
    admin_password = st.text_input("Enter Admin Password to Access", type="password", key="admin_password")

    if admin_password == "admin123":  # Admin password for validation
        st.success("Admin access granted!")
        discount_code = st.text_input("Create a New Discount Code", key="new_discount_code")
        discount_percentage = st.slider("Select Discount Percentage", min_value=5, max_value=50, step=5)
        st.write(f"Discount Code: **{discount_code.upper()}** for **{discount_percentage}%** off.")

        if st.button("Save Discount"):
            if discount_code:
                st.success(f"Discount code **{discount_code.upper()}** for **{discount_percentage}%** has been saved!")
            else:
                st.warning("Please enter a valid discount code.")
    else:
        st.warning("Admin access required. Please enter the correct password to proceed.")

    st.divider()

    # Customer Discount Section
    st.subheader("Redeem Your Discount")
    customer_discount_code = st.text_input("Enter Discount Code", key="customer_discount_code")
    if customer_discount_code.upper() == "50OFF":
        st.success("Congratulations! You've unlocked a **50% discount** on your next purchase. 🎉")
    elif customer_discount_code:
        st.error("Invalid discount code. Please try again.")

# Feedback Section
if menu_option == "Feedback":
    st.header("💬 We Value Your Feedback!")
    st.write("Your thoughts help us brew better experiences. Share your feedback and let us know how we’re doing!")

    feedback_options = ["Quality of Coffee", "Customer Service", "Ambiance", "Other"]
    feedback_category = st.selectbox("What would you like to provide feedback on?", feedback_options, key="feedback_category")
    feedback_details = st.text_area(f"Tell us more about your experience with {feedback_category.lower()}:")

    # Option to attach an image
    attach_image = st.checkbox("Attach an image or screenshot?")
    if attach_image:
        uploaded_image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit Feedback"):
        if feedback_details:
            feedback_entry = {
                "category": feedback_category,
                "details": feedback_details,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if uploaded_image:
                feedback_entry["image"] = uploaded_image.name
            st.session_state.feedback.append(feedback_entry)
            st.success("Thank you for your valuable feedback! 💖")
        else:
            st.warning("Please fill in the feedback details before submitting.")


