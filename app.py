# import streamlit as st
# import pandas as pd
# import pickle
# import datetime

# # -------------------- Load model --------------------
# with open('medical_stock_data.pkl', 'rb') as f:
#     model, model_features = pickle.load(f)

# # -------------------- Initialize Session --------------------
# if 'stock_df' not in st.session_state:
#     st.session_state.stock_df = pd.read_csv('medical_stock_data.csv')
#     st.session_state.stock_df['Date'] = pd.to_datetime(st.session_state.stock_df['Date'], format='mixed')
#     st.session_state.stock_df['Expiry_Date'] = pd.to_datetime(st.session_state.stock_df['Expiry_Date'], format='mixed')

# if 'customers' not in st.session_state:
#     st.session_state.customers = {}

# if 'sales' not in st.session_state:
#     st.session_state.sales = {}

# # -------------------- App Title --------------------
# st.set_page_config(page_title="Medical Stock Manager", layout="wide")
# st.title("💊 Medical Store Stock & Sales System")

# menu = st.sidebar.radio("Choose Operation:", [
#     "📥 Add Stock", "📤 Sell / Out Stock", "📉 Predict Shortage", "📋 Invoice", "📦 View All Stock"
# ])

# # -------------------- 1. Add Stock --------------------
# if menu == "📥 Add Stock":
#     st.subheader("➕ Add New Stock Item")
#     with st.form("add_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("Medicine Name")
#             category = st.selectbox("Category", ["Antibiotic", "Antacid", "Antidiabetic", "Antihistamine", "Painkiller"])
#             supplier = st.text_input("Supplier")
#             purchase_price = st.number_input("Purchase Price (per unit)", min_value=0.0)
#         with col2:
#             units = st.number_input("Units Purchased", min_value=1)
#             expiry = st.date_input("Expiry Date", value=datetime.date.today() + datetime.timedelta(days=365))
#             date = datetime.datetime.now().date()

#         add_submit = st.form_submit_button("✅ Add Stock")
#         if add_submit:
#             new_row = {
#                 "Date": date,
#                 "Medicine_Name": name,
#                 "Category": category,
#                 "Supplier": supplier,
#                 "Units_Purchased": units,
#                 "Units_Sold": 0,
#                 "Current_Stock": units,
#                 "Expiry_Date": expiry,
#                 "Purchase_Price": purchase_price,
#                 "Is_Shortage": 0
#             }
#             st.session_state.stock_df = pd.concat(
#                 [st.session_state.stock_df, pd.DataFrame([new_row])], ignore_index=True
#             )
#             st.success(f"{name} added successfully to stock!")

# # -------------------- 2. Sell / Out Stock --------------------
# elif menu == "📤 Sell / Out Stock":
#     st.subheader("➖ Stock Out & Customer Details")
#     with st.form("sell_form"):
#         phone = st.text_input("Customer Phone Number")
#         name = st.text_input("Customer Name") if phone not in st.session_state.customers else st.session_state.customers[phone]
#         med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
#         quantity = st.number_input("Quantity to Sell", min_value=1)
#         sale_price = st.number_input("Sale Price (per unit)", min_value=0.0)
#         sell_btn = st.form_submit_button("💸 Sell")

#     if sell_btn:
#         st.session_state.customers[phone] = name
#         stock_index = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].index[-1]
#         st.session_state.stock_df.at[stock_index, 'Units_Sold'] += quantity
#         st.session_state.stock_df.at[stock_index, 'Current_Stock'] -= quantity

#         sale_entry = {
#             "medicine": med_name,
#             "quantity": quantity,
#             "sale_price": sale_price,
#             "total": quantity * sale_price,
#             "date": datetime.datetime.now()
#         }

#         if phone not in st.session_state.sales:
#             st.session_state.sales[phone] = []
#         st.session_state.sales[phone].append(sale_entry)
#         st.success(f"Sold {quantity} units of {med_name} to {name}.")

# # -------------------- 3. Predict Shortage --------------------
# elif menu == "📉 Predict Shortage":
#     st.subheader("📊 Predict Shortage for Medicine")
#     med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
#     predict_btn = st.button("⚠️ Predict Shortage")

#     if predict_btn:
#         latest = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].iloc[-1].copy()
#         latest['Purchase_Month'] = latest['Date'].month
#         latest['Purchase_Year'] = latest['Date'].year
#         latest['Days_to_Expiry'] = (latest['Expiry_Date'] - latest['Date']).days
#         input_df = latest.drop(['Date', 'Expiry_Date', 'Is_Shortage']).to_frame().T
#         input_df = pd.get_dummies(input_df)
#         for col in model_features:
#             if col not in input_df.columns:
#                 input_df[col] = 0
#         input_df = input_df[model_features]

#         result = model.predict(input_df)[0]
#         if result == 1:
#             st.error(f"🔴 {med_name} is at risk of shortage!")
#         else:
#             st.success(f"🟢 {med_name} has sufficient stock.")

# # -------------------- 4. Invoice --------------------
# elif menu == "📋 Invoice":
#     st.subheader("📄 Generate Invoice")
#     phone = st.text_input("Enter Customer Phone Number")

#     if phone in st.session_state.customers and phone in st.session_state.sales:
#         name = st.session_state.customers[phone]
#         sales = st.session_state.sales[phone]
#         invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

#         st.write(f"🧾 **Invoice #:** {invoice_no}")
#         st.write(f"👤 **Customer Name:** {name}")
#         st.write(f"📞 **Phone:** {phone}")
#         st.write(f"📅 **Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         st.markdown("---")

#         df_sales = pd.DataFrame(sales)
#         df_sales.index += 1
#         st.write("### 🧾 Purchased Items:")
#         st.dataframe(df_sales[['medicine', 'quantity', 'sale_price', 'total']])

#         grand_total = sum(item['total'] for item in sales)
#         st.markdown(f"### 💰 **Total Amount:** Rs. {grand_total:.2f}")

#         # Create invoice text for download
#         invoice_text = f"""
#         Invoice #: {invoice_no}
#         Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#         Customer Name: {name}
#         Phone: {phone}

#         Items:
#         ------------------------------------------
#         {"No.":<4} {"Medicine":<15} {"Qty":<5} {"Price":<10} {"Total":<10}
#         ------------------------------------------
#         """
#         for i, item in enumerate(sales, start=1):
#             invoice_text += f"{i:<4} {item['medicine']:<15} {item['quantity']:<5} Rs.{item['sale_price']:<9.2f} Rs.{item['total']:<9.2f}\n"

#         invoice_text += f"\nGrand Total: Rs. {grand_total:.2f}\n"
#         invoice_text += "------------------------------------------\nThank you for your purchase!"

#         st.download_button("⬇️ Download Invoice", invoice_text, file_name=f"{invoice_no}.txt")
#     else:
#         st.warning("❗ Customer or sale record not found. Please ensure a sale was made.")

# # -------------------- 5. View Stock --------------------
# elif menu == "📦 View All Stock":
#     st.subheader("📦 Current Stock Overview")

#     # Ensure datetime compatibility for display
#     df_display = st.session_state.stock_df.copy()
#     df_display['Expiry_Date'] = pd.to_datetime(df_display['Expiry_Date'], errors='coerce')
#     df_display['Date'] = pd.to_datetime(df_display['Date'], errors='coerce')

#     st.dataframe(df_display[['Medicine_Name', 'Current_Stock', 'Category', 'Supplier', 'Expiry_Date']])

#     st.markdown("### 🚨 Medicines With Shortage")
#     shortage = df_display[df_display['Current_Stock'] <= 0]
#     st.dataframe(shortage[['Medicine_Name', 'Current_Stock', 'Supplier']])

# import streamlit as st
# import pandas as pd
# import pickle
# import datetime

# # -------------------- Load model --------------------
# with open('medical_stock_data.pkl', 'rb') as f:
#     model, model_features = pickle.load(f)

# # -------------------- Initialize Session --------------------
# if 'stock_df' not in st.session_state:
#     st.session_state.stock_df = pd.read_csv('medical_stock_data.csv')
#     st.session_state.stock_df['Date'] = pd.to_datetime(st.session_state.stock_df['Date'], format='mixed')
#     st.session_state.stock_df['Expiry_Date'] = pd.to_datetime(st.session_state.stock_df['Expiry_Date'], format='mixed')

# if 'customers' not in st.session_state:
#     st.session_state.customers = {}

# if 'sales' not in st.session_state:
#     st.session_state.sales = {}

# # -------------------- App Title --------------------
# st.set_page_config(page_title="Tounsvi Medical Store by Suleman", layout="wide")
# st.markdown("<h1 style='text-align: center; color: green;'>🏥 Tounsvi Medical Store by Suleman</h1>", unsafe_allow_html=True)
# st.title("💊 Stock & Sales Management System")

# menu = st.sidebar.radio("Choose Operation:", [
#     "📥 Add Stock", "📤 Sell / Out Stock", "📉 Predict Shortage", "📋 Invoice", "📦 View All Stock"
# ])

# # -------------------- 1. Add Stock --------------------
# if menu == "📥 Add Stock":
#     st.subheader("➕ Add New Stock Item")
#     with st.form("add_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("Medicine Name")
#             category = st.selectbox("Category", ["Antibiotic", "Antacid", "Antidiabetic", "Antihistamine", "Painkiller"])
#             supplier = st.text_input("Supplier")
#             purchase_price = st.number_input("Purchase Price (per unit)", min_value=0.0)
#         with col2:
#             units = st.number_input("Units Purchased", min_value=1)
#             expiry = st.date_input("Expiry Date", value=datetime.date.today() + datetime.timedelta(days=365))
#             date = datetime.datetime.now().date()

#         add_submit = st.form_submit_button("✅ Add Stock")
#         if add_submit:
#             new_row = {
#                 "Date": date,
#                 "Medicine_Name": name,
#                 "Category": category,
#                 "Supplier": supplier,
#                 "Units_Purchased": units,
#                 "Units_Sold": 0,
#                 "Current_Stock": units,
#                 "Expiry_Date": expiry,
#                 "Purchase_Price": purchase_price,
#                 "Is_Shortage": 0
#             }
#             st.session_state.stock_df = pd.concat(
#                 [st.session_state.stock_df, pd.DataFrame([new_row])], ignore_index=True
#             )
#             st.success(f"{name} added successfully to stock!")

# # -------------------- 2. Sell / Out Stock --------------------
# elif menu == "📤 Sell / Out Stock":
#     st.subheader("➖ Stock Out & Customer Details")
#     with st.form("sell_form"):
#         phone = st.text_input("Customer Phone Number")
#         name = st.text_input("Customer Name") if phone not in st.session_state.customers else st.session_state.customers[phone]
#         med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
#         quantity = st.number_input("Quantity to Sell", min_value=1)
#         sale_price = st.number_input("Sale Price (per unit)", min_value=0.0)
#         sell_btn = st.form_submit_button("💸 Sell")

#     if sell_btn:
#         st.session_state.customers[phone] = name
#         stock_index = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].index[-1]
#         st.session_state.stock_df.at[stock_index, 'Units_Sold'] += quantity
#         st.session_state.stock_df.at[stock_index, 'Current_Stock'] -= quantity

#         sale_entry = {
#             "medicine": med_name,
#             "quantity": quantity,
#             "sale_price": sale_price,
#             "total": quantity * sale_price,
#             "date": datetime.datetime.now()
#         }

#         if phone not in st.session_state.sales:
#             st.session_state.sales[phone] = []
#         st.session_state.sales[phone].append(sale_entry)
#         st.success(f"Sold {quantity} units of {med_name} to {name}.")

# # -------------------- 3. Predict Shortage --------------------
# elif menu == "📉 Predict Shortage":
#     st.subheader("📊 Predict Shortage for Medicine")
#     med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
#     predict_btn = st.button("⚠️ Predict Shortage")

#     if predict_btn:
#         latest = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].iloc[-1].copy()
#         latest['Purchase_Month'] = latest['Date'].month
#         latest['Purchase_Year'] = latest['Date'].year
#         latest['Days_to_Expiry'] = (latest['Expiry_Date'] - latest['Date']).days
#         input_df = latest.drop(['Date', 'Expiry_Date', 'Is_Shortage']).to_frame().T
#         input_df = pd.get_dummies(input_df)
#         for col in model_features:
#             if col not in input_df.columns:
#                 input_df[col] = 0
#         input_df = input_df[model_features]

#         result = model.predict(input_df)[0]
#         if result == 1:
#             st.error(f"🔴 {med_name} is at risk of shortage!")
#         else:
#             st.success(f"🟢 {med_name} has sufficient stock.")

# # -------------------- 4. Invoice --------------------
# elif menu == "📋 Invoice":
#     st.subheader("📄 Generate Invoice")
#     phone = st.text_input("Enter Customer Phone Number")

#     if phone in st.session_state.customers and phone in st.session_state.sales:
#         name = st.session_state.customers[phone]
#         sales = st.session_state.sales[phone]
#         invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

#         st.markdown(f"<h3 style='color:#004d00;'>🧾 Tounsvi Medical Store by Suleman</h3>", unsafe_allow_html=True)
#         st.write(f"**Invoice #:** {invoice_no}")
#         st.write(f"**Customer Name:** {name}")
#         st.write(f"**Phone:** {phone}")
#         st.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         st.markdown("---")

#         df_sales = pd.DataFrame(sales)
#         df_sales.index += 1
#         st.write("### 🧾 Purchased Items:")
#         st.dataframe(df_sales[['medicine', 'quantity', 'sale_price', 'total']])

#         grand_total = sum(item['total'] for item in sales)
#         st.markdown(f"### 💰 **Total Amount:** Rs. {grand_total:.2f}")

#         invoice_text = f"""
#         🏥 Tounsvi Medical Store by Suleman
#         ------------------------------------------
#         Invoice #: {invoice_no}
#         Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#         Customer Name: {name}
#         Phone: {phone}

#         Items:
#         ------------------------------------------
#         {"No.":<4} {"Medicine":<15} {"Qty":<5} {"Price":<10} {"Total":<10}
#         ------------------------------------------
#         """
#         for i, item in enumerate(sales, start=1):
#             invoice_text += f"{i:<4} {item['medicine']:<15} {item['quantity']:<5} Rs.{item['sale_price']:<9.2f} Rs.{item['total']:<9.2f}\n"

#         invoice_text += f"\nGrand Total: Rs. {grand_total:.2f}\n"
#         invoice_text += "------------------------------------------\nThank you for choosing Tounsvi Medical Store!"

#         st.download_button("⬇️ Download Invoice", invoice_text, file_name=f"{invoice_no}.txt")
#     else:
#         st.warning("❗ Customer or sale record not found. Please ensure a sale was made.")

# # -------------------- 5. View Stock --------------------
# elif menu == "📦 View All Stock":
#     st.subheader("📦 Current Stock Overview")

#     df_display = st.session_state.stock_df.copy()
#     df_display['Expiry_Date'] = pd.to_datetime(df_display['Expiry_Date'], errors='coerce')
#     df_display['Date'] = pd.to_datetime(df_display['Date'], errors='coerce')

#     st.dataframe(df_display[['Medicine_Name', 'Current_Stock', 'Category', 'Supplier', 'Expiry_Date']])

#     st.markdown("### 🚨 Medicines With Shortage")
#     shortage = df_display[df_display['Current_Stock'] <= 0]
#     st.dataframe(shortage[['Medicine_Name', 'Current_Stock', 'Supplier']])
import streamlit as st
import pandas as pd
import pickle
import datetime

# -------------------- Load model --------------------
with open('medical_stock_data.pkl', 'rb') as f:
    model, model_features = pickle.load(f)

# -------------------- Initialize Session --------------------
if 'stock_df' not in st.session_state:
    st.session_state.stock_df = pd.read_csv('medical_stock_data.csv')
    st.session_state.stock_df['Date'] = pd.to_datetime(st.session_state.stock_df['Date'], format='mixed')
    st.session_state.stock_df['Expiry_Date'] = pd.to_datetime(st.session_state.stock_df['Expiry_Date'], format='mixed')

if 'customers' not in st.session_state:
    st.session_state.customers = {}

if 'sales' not in st.session_state:
    st.session_state.sales = {}

# -------------------- App Title --------------------
st.set_page_config(page_title="Medical Stock Manager", layout="wide")
st.title("💊 Tounsvi Medical Store by Suleman")

menu = st.sidebar.radio("📍 Navigate to:", [
    "🏠 Home", "📥 Add Stock", "📤 Sell / Out Stock", "📉 Predict Shortage", "📋 Invoice", "📦 View All Stock"
])

# -------------------- 🏠 Home --------------------
if menu == "🏠 Home":
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f0f8ff; border-radius: 12px;'>
        <h1 style='color: #2e86c1;'>🏥 Welcome to <span style='color: #c0392b;'>Tounsvi Medical Store</span></h1>
        <h3 style='color: #1f618d;'>by Suleman</h3>
        <p style='font-size: 18px;'>Your trusted companion for efficient stock management, customer sales tracking, and medicine shortage predictions.</p>
        <hr style='margin: 20px 0;'>
        <p style='font-size: 16px;'>Use the sidebar to add or sell stock, generate invoices, or predict stock shortages instantly.</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- 1. Add Stock --------------------
elif menu == "📥 Add Stock":
    st.subheader("➕ Add New Stock Item")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Medicine Name")
            category = st.selectbox("Category", ["Antibiotic", "Antacid", "Antidiabetic", "Antihistamine", "Painkiller"])
            supplier = st.text_input("Supplier")
            purchase_price = st.number_input("Purchase Price (per unit)", min_value=0.0)
        with col2:
            units = st.number_input("Units Purchased", min_value=1)
            expiry = st.date_input("Expiry Date", value=datetime.date.today() + datetime.timedelta(days=365))
            date = datetime.datetime.now().date()

        add_submit = st.form_submit_button("✅ Add Stock")
        if add_submit:
            new_row = {
                "Date": date,
                "Medicine_Name": name,
                "Category": category,
                "Supplier": supplier,
                "Units_Purchased": units,
                "Units_Sold": 0,
                "Current_Stock": units,
                "Expiry_Date": expiry,
                "Purchase_Price": purchase_price,
                "Is_Shortage": 0
            }
            st.session_state.stock_df = pd.concat(
                [st.session_state.stock_df, pd.DataFrame([new_row])], ignore_index=True
            )
            st.success(f"{name} added successfully to stock!")

# -------------------- 2. Sell / Out Stock --------------------
elif menu == "📤 Sell / Out Stock":
    st.subheader("➖ Stock Out & Customer Details")
    with st.form("sell_form"):
        phone = st.text_input("Customer Phone Number")
        name = st.text_input("Customer Name") if phone not in st.session_state.customers else st.session_state.customers[phone]
        med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
        quantity = st.number_input("Quantity to Sell", min_value=1)
        sale_price = st.number_input("Sale Price (per unit)", min_value=0.0)
        sell_btn = st.form_submit_button("💸 Sell")

    if sell_btn:
        st.session_state.customers[phone] = name
        stock_index = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].index[-1]
        st.session_state.stock_df.at[stock_index, 'Units_Sold'] += quantity
        st.session_state.stock_df.at[stock_index, 'Current_Stock'] -= quantity

        sale_entry = {
            "medicine": med_name,
            "quantity": quantity,
            "sale_price": sale_price,
            "total": quantity * sale_price,
            "date": datetime.datetime.now()
        }

        if phone not in st.session_state.sales:
            st.session_state.sales[phone] = []
        st.session_state.sales[phone].append(sale_entry)
        st.success(f"Sold {quantity} units of {med_name} to {name}.")

# -------------------- 3. Predict Shortage --------------------
elif menu == "📉 Predict Shortage":
    st.subheader("📊 Predict Shortage for Medicine")
    med_name = st.selectbox("Select Medicine", st.session_state.stock_df['Medicine_Name'].unique())
    predict_btn = st.button("⚠️ Predict Shortage")

    if predict_btn:
        latest = st.session_state.stock_df[st.session_state.stock_df['Medicine_Name'] == med_name].iloc[-1].copy()
        latest['Purchase_Month'] = latest['Date'].month
        latest['Purchase_Year'] = latest['Date'].year
        latest['Days_to_Expiry'] = (latest['Expiry_Date'] - latest['Date']).days
        input_df = latest.drop(['Date', 'Expiry_Date', 'Is_Shortage']).to_frame().T
        input_df = pd.get_dummies(input_df)
        for col in model_features:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[model_features]

        result = model.predict(input_df)[0]
        if result == 1:
            st.error(f"🔴 {med_name} is at risk of shortage!")
        else:
            st.success(f"🟢 {med_name} has sufficient stock.")

# -------------------- 4. Invoice --------------------
elif menu == "📋 Invoice":
    st.subheader("📄 Generate Invoice")
    phone = st.text_input("Enter Customer Phone Number")

    if phone in st.session_state.customers and phone in st.session_state.sales:
        name = st.session_state.customers[phone]
        sales = st.session_state.sales[phone]
        invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        st.markdown(f"""
        ### 🧾 Invoice #: {invoice_no}  
        **🏪 Store:** Tounsvi Medical Store by Suleman  
        👤 **Customer Name:** {name}  
        📞 **Phone:** {phone}  
        📅 **Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
        ---
        """)

        df_sales = pd.DataFrame(sales)
        df_sales.index += 1
        st.write("### 🧾 Purchased Items:")
        st.dataframe(df_sales[['medicine', 'quantity', 'sale_price', 'total']])

        grand_total = sum(item['total'] for item in sales)
        st.markdown(f"### 💰 **Total Amount:** Rs. {grand_total:.2f}")

        invoice_text = f"""
        Tounsvi Medical Store by Suleman
        ------------------------------------------
        Invoice #: {invoice_no}
        Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Customer Name: {name}
        Phone: {phone}

        Items:
        ------------------------------------------
        {'No.':<4} {'Medicine':<15} {'Qty':<5} {'Price':<10} {'Total':<10}
        ------------------------------------------
        """
        for i, item in enumerate(sales, start=1):
            invoice_text += f"{i:<4} {item['medicine']:<15} {item['quantity']:<5} Rs.{item['sale_price']:<9.2f} Rs.{item['total']:<9.2f}\n"

        invoice_text += f"\nGrand Total: Rs. {grand_total:.2f}\n"
        invoice_text += "------------------------------------------\nThank you for your purchase!"

        st.download_button("⬇️ Download Invoice", invoice_text, file_name=f"{invoice_no}.txt")
    else:
        st.warning("❗ Customer or sale record not found. Please ensure a sale was made.")

# -------------------- 5. View Stock --------------------
elif menu == "📦 View All Stock":
    st.subheader("📦 Current Stock Overview")
    df_display = st.session_state.stock_df.copy()
    df_display['Expiry_Date'] = pd.to_datetime(df_display['Expiry_Date'], errors='coerce')
    df_display['Date'] = pd.to_datetime(df_display['Date'], errors='coerce')

    st.dataframe(df_display[['Medicine_Name', 'Current_Stock', 'Category', 'Supplier', 'Expiry_Date']])

    st.markdown("### 🚨 Medicines With Shortage")
    shortage = df_display[df_display['Current_Stock'] <= 0]
    st.dataframe(shortage[['Medicine_Name', 'Current_Stock', 'Supplier']])
