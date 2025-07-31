import streamlit as st
import json
import random
import string
from pathlib import Path

# --------- Styling ---------
st.set_page_config(page_title="ONE-TO-ONE Bank", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        /* App background */
        .main {
            background-color: #f2f4f8;
        }

        /* Styled buttons */
        .stButton>button {
            background-color: #0e76a8;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }

        /* Rounded text inputs */
        .stTextInput>div>div>input {
            border-radius: 6px;
        }

        /* Spacing between radio buttons */
        .stRadio > div {
            gap: 1rem;
        }

        /* Big headline font */
        .big-font {
            font-size: 30px !important;
            color: #0e76a8;
            font-weight: bold;
        }

        /* --- New Tab Styling Below --- */

        /* Center the tab bar */
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
            flex-wrap: wrap;
            row-gap: 0.5rem;
        }

        /* Shrink tabs to fit content and center text inside them */
        .stTabs [data-baseweb="tab"] {
            min-width: auto !important;
            max-width: max-content !important;
            font-weight: 600;
            padding: 0.4rem 0.9rem;
            white-space: nowrap;
        }

        /* Center headers inside each tab */
        h1, h2, h3 {
            text-align: center;
        }
            
    </style>
""", unsafe_allow_html=True)


# --------- Database Handling ---------
DATABASE = 'data.json'
if not Path(DATABASE).exists():
    with open(DATABASE, 'w') as f:
        json.dump([], f)

with open(DATABASE) as f:
    bank_data = json.load(f)


def save_data():
    with open(DATABASE, 'w') as f:
        json.dump(bank_data, f, indent=2)

def generate_account_no():
    acc = random.choices(string.ascii_letters, k=3) + random.choices(string.digits, k=10) + random.choices("!@#$%^&*", k=1)
    random.shuffle(acc)
    return ''.join(acc)

# --------- Banking Functions ---------
def create_account(name, age, email, pin):
    if age < 18 or len(str(pin)) != 4:
        return False, "Age must be 18+ and PIN should be 4 digits"
    
    new_user = {
        "Name": name,
        "Age": age,
        "Email": email,
        "AccountNo": generate_account_no(),
        "Pin": pin,
        "balance": 0
    }
    bank_data.append(new_user)
    save_data()
    return True, new_user

def find_user(acc_no, pin):
    return next((u for u in bank_data if u['AccountNo'] == acc_no and u['Pin'] == pin), None)

def deposit(acc_no, pin, amount):
    user = find_user(acc_no, pin)
    if user and 0 < amount <= 10000:
        user['balance'] += amount
        save_data()
        return True, user
    return False, None

def withdraw(acc_no, pin, amount):
    user = find_user(acc_no, pin)
    if user:
        if amount <= user['balance'] and amount <= 10000:
            user['balance'] -= amount
            save_data()
            return True, user
        elif amount > 10000:
            return False, "You can only withdraw up to 10000"
        else:
            return False, "Insufficient balance"
    return False, "Account not found"

def update_user(acc_no, pin, field, new_value):
    user = find_user(acc_no, pin)
    if user:
        user[field] = new_value
        save_data()
        return True, user
    return False, None

def delete_user(acc_no, pin):
    global bank_data
    user = find_user(acc_no, pin)
    if user:
        bank_data = [u for u in bank_data if not (u['AccountNo'] == acc_no and u['Pin'] == pin)]
        save_data()
        return True
    return False

# --------- UI ---------
st.markdown(
    "<h1 style='text-align: center; color: #0e76a8;'> ONE-TO-ONE Bank</h1>",
    unsafe_allow_html=True
)
st.markdown('<p style="text-align: center;">Your Secure Digital Banking Partner</p>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
center_col = st.columns([1.5, 5, 1.5])[1]
with center_col:
    tabs = st.tabs([
        "🏠 Home", 
        "➕ Create Account", 
        "💰 Deposit", 
        "💸 Withdraw", 
        "🔍 Check Account", 
        "✏️ Update Account", 
        "🗑️ Delete Account"
    ])
st.markdown("</div>", unsafe_allow_html=True)

# --------- Home Tab ---------
with tabs[0]:
    st.image("I:\Python Projects-Github\Banking management system\image-Photoroom.png", use_container_width=True)
    st.markdown('<p style="text-align: center;">Welcome to ONE-TO-ONE Bank — a simple, secure, and modern banking experience!</p>', unsafe_allow_html=True)
  

# --------- Create Account Tab ---------
with tabs[1]:

    st.header("➕ Create a New Account")
    name = st.text_input("Enter your Name")
    age = st.number_input("Enter your Age", min_value=1)
    email = st.text_input("Enter your Email")
    pin = st.text_input("Choose a 4-digit PIN", type="password")

    if st.button("Create Account"):
        if name and email and pin:
            success, result = create_account(name, age, email, int(pin))
            if success:
                st.success("✅ Account Created Successfully!")
                st.json(result)
            else:
                st.error(f"❌ {result}")
        else:
            st.warning("Please fill all fields.")

# --------- Deposit Tab ---------
with tabs[2]:
    st.header("💰 Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount (max 10000)", min_value=1)

    if st.button("Deposit"):
        success, user = deposit(acc, int(pin), amount)
        if success:
            st.success("✅ Deposit Successful")
            st.json(user)
        else:
            st.error("❌ Deposit Failed. Check Account Info or Limit")

# --------- Withdraw Tab ---------
with tabs[3]:
    st.header("💸 Withdraw Money")
    acc = st.text_input("Account Number ", key="withdraw_acc")
    pin = st.text_input("PIN", type="password", key="withdraw_pin")
    amount = st.number_input("Amount (max 10000)", min_value=1, key="withdraw_amount")

    if st.button("Withdraw"):
        success, result = withdraw(acc, int(pin), amount)
        if success:
            st.success("✅ Withdrawal Successful")
            st.json(result)
        else:
            st.error(f"❌ Withdrawal Failed: {result}")

# --------- Check Account Tab ---------
with tabs[4]:
    st.header("🔍 Check Account Details")
    acc = st.text_input("Account Number", key="check_acc")
    pin = st.text_input("PIN", type="password", key="check_pin")

    if st.button("Check"):
        user = find_user(acc, int(pin))
        if user:
            st.success("✅ Account Found")
            st.json(user)
        else:
            st.error("❌ Account Not Found")

# --------- Update Tab ---------
with tabs[5]:
    st.header("✏️ Update Account Info")
    acc = st.text_input("Account Number", key="update_acc")
    pin = st.text_input("PIN", type="password", key="update_pin")

    options = {"Name": "Name", "Age": "Age", "Email": "Email", "Pin": "Pin"}
    field = st.selectbox("Choose Field to Update", list(options.values()))
    new_value = st.text_input(f"Enter new {field}")

    if st.button("Update"):
        success, user = update_user(acc, int(pin), field, new_value if field != "Pin" else int(new_value))
        if success:
            st.success("✅ Account Updated")
            st.json(user)
        else:
            st.error("❌ Update Failed. Check credentials.")

# --------- Delete Tab ---------
with tabs[6]:
    st.header("🗑️ Delete Account")
    acc = st.text_input("Account Number", key="delete_acc")
    pin = st.text_input("PIN", type="password", key="delete_pin")

    if st.button("Delete"):
        confirm = st.radio("Are you sure?", ("No", "Yes"))
        if confirm == "Yes":
            success = delete_user(acc, int(pin))
            if success:
                st.success("✅ Account Deleted Successfully")
            else:
                st.error("❌ Deletion Failed. Check credentials.")
