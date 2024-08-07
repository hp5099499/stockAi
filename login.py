import streamlit as st
import pandas as pd
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

# File to store user credentials
user_data_FILE = 'user_data.csv'
EMAIL_VERIFICATION_FILE = 'email_verification.csv'

# Create files if they do not exist
if not os.path.exists(user_data_FILE):
    pd.DataFrame(columns=['username', 'email', 'password', 'verified']).to_csv(user_data_FILE, index=False)

if not os.path.exists(EMAIL_VERIFICATION_FILE):
    pd.DataFrame(columns=['email', 'token']).to_csv(EMAIL_VERIFICATION_FILE, index=False)

def hash_password(password):
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def send_verification_email(email, token):
    """Send an email with a verification link."""
    sender_email = "mohitkmourya@gmail.com" 
    sender_password = "gavo mgvo eqyf joke"
    subject = "Email Verification"
    body = f"Please verify your email by clicking the following link:\nhttp://localhost:8501/verify?token={token}"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the correct SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        st.success("Verification email sent! Please check your inbox.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def load_user_data():
    if os.path.exists(user_data_FILE):
        return pd.read_csv(user_data_FILE)
    else:
        return pd.DataFrame(columns=['username', 'email', 'password', 'verified'])

def save_user_data(user_data):
    user_data.to_csv(user_data_FILE, index=False)

def load_verification_data():
    if os.path.exists(EMAIL_VERIFICATION_FILE):
        return pd.read_csv(EMAIL_VERIFICATION_FILE)
    else:
        return pd.DataFrame(columns=['email', 'token'])

def save_verification_data(verification_data):
    verification_data.to_csv(EMAIL_VERIFICATION_FILE, index=False)

def signup():
    st.subheader("Sign Up")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
        user_data = load_user_data()
        if username in user_data['username'].values:
            st.error("Username already exists!")
        elif email in user_data['email'].values:
            st.error("Email already registered!")
        else:
            token = str(uuid.uuid4())
            new_user = pd.DataFrame([{'username': username, 'email': email, 'password': hash_password(password), 'verified': False}])
            user_data = pd.concat([user_data, new_user], ignore_index=True)
            save_user_data(user_data)
            verification_data = load_verification_data()
            new_verification = pd.DataFrame([{'email': email, 'token': token}])
            verification_data = pd.concat([verification_data, new_verification], ignore_index=True)
            save_verification_data(verification_data)
            send_verification_email(email, token)

def verify_email(token):
    verification_data = load_verification_data()
    if token in verification_data['token'].values:
        email = verification_data[verification_data['token'] == token]['email'].values[0]
        user_data = load_user_data()
        if email in user_data['email'].values:
            user_data.loc[user_data['email'] == email, 'verified'] = True
            save_user_data(user_data)
            verification_data = verification_data[verification_data['token'] != token]
            save_verification_data(verification_data)
            st.success("Email verified successfully! You can now log in.")
    else:
        st.error("Invalid or expired verification token.")

def login():
    st.subheader("Log In")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Log In"):
        user_data = load_user_data()
        
        if email not in user_data['email'].values:
            st.error("Email does not exist!")
        else:
            user_row = user_data[user_data['email'] == email]
            if user_row.empty:
                st.error("Email does not exist!")
            else:
                if user_row['password'].values[0] != hash_password(password):
                    st.error("Incorrect password!")
                elif not user_row['verified'].values[0]:
                    st.error("Email not verified. Please check your email for the verification link.")
                else:
                    st.success("Logged in successfully!")

def main():
    st.title("Login and Signup System")

    choice = st.sidebar.selectbox("Select a page", ["Login", "Sign Up"])

    if choice == "Sign Up":
        signup()
    else:
        login()

if __name__ == "__main__":
    # Uncomment for testing email functionality
    # token = str(uuid.uuid4())
    # send_verification_email("your_test_email@gmail.com", token)
    main()
