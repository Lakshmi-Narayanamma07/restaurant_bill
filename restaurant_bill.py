import streamlit as st
from datetime import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Restaurant Bill Generator",
    page_icon="🍔",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .bill-card {
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }

    .total-card {
        padding: 25px;
        border-radius: 20px;
        background: linear-gradient(135deg, #111827, #374151);
        color: white;
        text-align: center;
    }

    .grand-total {
        font-size: 38px;
        font-weight: 800;
    }

    .restaurant-header {
        text-align: center;
        border-bottom: 2px dashed #d1d5db;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        margin-top: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------
MENU = {
    "🍕 Margherita Pizza": 249,
    "🍔 Veg Burger": 149,
    "🍝 White Sauce Pasta": 199,
    "🍟 French Fries": 99,
    "🥪 Club Sandwich": 129,
    "🌮 Mexican Tacos": 179,
    "🍚 Fried Rice": 159,
    "🥤 Cold Drink": 59,
    "☕ Coffee": 79,
    "🍰 Chocolate Cake": 119
}

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">🍔 Restaurant Bill Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create a professional restaurant bill in seconds</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("🧾 Bill Settings")

customer_name = st.sidebar.text_input(
    "👤 Customer Name",
    placeholder="Enter customer name"
)

table_number = st.sidebar.text_input(
    "🪑 Table Number",
    placeholder="Example: T-05"
)

tax_rate = st.sidebar.number_input(
    "Tax (%)",
    min_value=0.0,
    max_value=30.0,
    value=5.0,
    step=0.5
)

discount_rate = st.sidebar.number_input(
    "Discount (%)",
    min_value=0.0,
    max_value=50.0,
    value=0.0,
    step=1.0
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Select the quantity of each item. "
    "Keep quantity as 0 if you don't want an item."
)

# ---------------------------------------------------------
# ITEM SELECTION
# ---------------------------------------------------------
st.subheader("🍽️ Select Food Items")

selected_items = []

columns = st.columns(2)

for index, (item, price) in enumerate(MENU.items()):

    with columns[index % 2]:

        quantity = st.number_input(
            f"{item} — ₹{price}",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"quantity_{index}"
        )

        if quantity > 0:

            selected_items.append({
                "item": item,
                "price": price,
                "quantity": quantity,
                "amount": price * quantity
            })

# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------
subtotal = sum(item["amount"] for item in selected_items)

discount_amount = subtotal * discount_rate / 100

amount_after_discount = subtotal - discount_amount

tax_amount = amount_after_discount * tax_rate / 100

grand_total = amount_after_discount + tax_amount

total_quantity = sum(
    item["quantity"] for item in selected_items
)

# ---------------------------------------------------------
# BILL
# ---------------------------------------------------------
st.divider()

if not selected_items:

    st.info(
        "🛒 Your bill is empty. "
        "Select at least one food item to generate the bill."
    )

else:

    st.subheader("🧾 Final Bill")

    bill_col, total_col = st.columns([2.2, 1])

    # -----------------------------------------------------
    # BILL DETAILS
    # -----------------------------------------------------
    with bill_col:

        st.markdown('<div class="bill-card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="restaurant-header">
                <h2>🍴 TASTY BITES RESTAURANT</h2>
                <p>Fresh Food • Great Taste • Happy Moments</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Customer:** "
                f"{customer_name.strip() if customer_name.strip() else 'Guest'}"
            )

        with col2:
            st.write(
                f"**Table:** "
                f"{table_number.strip() if table_number.strip() else 'N/A'}"
            )

        st.write(
            f"**Date:** {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
        )

        st.divider()

        # Table header
        h1, h2, h3, h4 = st.columns([3, 1, 1.3, 1.4])

        h1.write("**Item**")
        h2.write("**Qty**")
        h3.write("**Price**")
        h4.write("**Amount**")

        for item in selected_items:

            r1, r2, r3, r4 = st.columns([3, 1, 1.3, 1.4])

            r1.write(item["item"])
            r2.write(item["quantity"])
            r3.write(f"₹{item['price']:,.2f}")
            r4.write(f"₹{item['amount']:,.2f}")

        st.divider()

        s1, s2 = st.columns(2)

        with s1:

            st.write(f"**Total Items:** {total_quantity}")

            st.write(
                f"**Subtotal:** ₹{subtotal:,.2f}"
            )

            st.write(
                f"**Discount:** − ₹{discount_amount:,.2f}"
            )

        with s2:

            st.write(
                f"**Tax:** + ₹{tax_amount:,.2f}"
            )

            st.write(
                f"**Tax Rate:** {tax_rate:g}%"
            )

            st.write(
                f"**Discount Rate:** {discount_rate:g}%"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------
    with total_col:

        st.markdown(
            f"""
            <div class="total-card">
                <div>GRAND TOTAL</div>
                <div class="grand-total">
                    ₹{grand_total:,.2f}
                </div>
                <div>{total_quantity} item(s)</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("✅ Bill generated successfully!")

        if discount_amount > 0:

            st.metric(
                "💰 You Saved",
                f"₹{discount_amount:,.2f}"
            )

        st.metric(
            "🧾 Subtotal",
            f"₹{subtotal:,.2f}"
        )

        st.metric(
            "💵 Tax",
            f"₹{tax_amount:,.2f}"
        )

        st.divider()

        if st.button(
            "🔄 Start New Bill",
            use_container_width=True
        ):

            for index in range(len(MENU)):
                st.session_state[f"quantity_{index}"] = 0

            st.rerun()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        🍴 Thank you for dining with us! <br>
        Built with Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)