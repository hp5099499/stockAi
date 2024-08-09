# import streamlit as st
# from streamlit_navigation_bar import st_navbar
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# import uuid
# import csv, json
# from datetime import datetime, timedelta

# # Load environment variables
# EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# # File for storing user data
# USER_DATA_FILE = 'users.csv'
# RESET_TOKENS_FILE = 'reset_tokens.json'

# # Utility Functions
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def load_user_data():
#     if os.path.exists(USER_DATA_FILE):
#         with open(USER_DATA_FILE, mode='r', newline='') as f:
#             reader = csv.DictReader(f)
#             return {row['email']: row for row in reader}
#     return {}

# def save_user_data(data):
#     with open(USER_DATA_FILE, mode='w', newline='') as f:
#         fieldnames = ['username', 'email', 'password']
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         for email, user_info in data.items():
#             writer.writerow(user_info)

# def load_reset_tokens():
#     if os.path.exists(RESET_TOKENS_FILE):
#         with open(RESET_TOKENS_FILE, 'r') as f:
#             return json.load(f)
#     return {}

# def save_reset_tokens(data):
#     with open(RESET_TOKENS_FILE, 'w') as f:
#         json.dump(data, f)

# def send_reset_email(user_email, token):
#     if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
#         st.error("Email settings are not configured correctly.")
#         return False

#     sender_email = EMAIL_ADDRESS
#     receiver_email = user_email

#     # Create the email
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = 'Password Reset Request'

#     reset_link = f"http://localhost:8501/?token={token}&email={user_email}"
#     body = f"Hi,\n\nClick the link below to reset your password:\n{reset_link}"
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(sender_email, EMAIL_PASSWORD)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         return True
#     except Exception as e:
#         st.error(f"Failed to send email: {e}")
#         return False

# # Signup Page
# def signup():
#     st.title("Sign Up")
#     username = st.text_input("Username", key="signup_username")
#     email = st.text_input("Email", key="signup_email")
#     password = st.text_input("Password", type="password", key="signup_password")
#     confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
#     if username and email and password:
#         if st.button("Sign Up", key="signup_button"):
#             user_data = load_user_data()
#             if password != confirm_password:
#                 st.error("Passwords do not match.")
#             elif email in user_data:
#                 st.error("Email already registered.")
#             else:
#                 hashed_password = hash_password(password)
#                 user_data[email] = {"username": username, "email": email, "password": hashed_password}
#                 save_user_data(user_data)
#                 st.success("Sign up successful! You can now log in.")

# # Sign In Page
# def signin():
#     st.title("Sign In")
#     email = st.text_input("Email", key="signin_email")
#     password = st.text_input("Password", type="password", key="signin_password")

#     if st.button("Sign In", key="signin_button"):
#         user_data = load_user_data()
#         hashed_password = hash_password(password)
#         if email in user_data and user_data[email]["password"] == hashed_password:
#             st.success(f"Welcome back, {user_data[email]['username']}!")
#         else:
#             st.error("Invalid email or password.")
    
#     # Forgot Password Section
#     st.subheader("Forgot Password?")
#     reset_email = st.text_input("Enter your email to reset your password", key="reset_email")
#     if st.button("Send Reset Link", key="send_reset_link"):
#         if reset_email:
#             user_data = load_user_data()
#             if reset_email in user_data:
#                 token = str(uuid.uuid4())
#                 reset_tokens = load_reset_tokens()
#                 reset_tokens[token] = {"email": reset_email, "expiry": (datetime.utcnow() + timedelta(hours=1)).isoformat()}
#                 save_reset_tokens(reset_tokens)
#                 if send_reset_email(reset_email, token):
#                     st.success("A password reset link has been sent to your email.")
#             else:
#                 st.error("Email not registered.")
#         else:
#             st.error("Please enter an email address.")

# # Reset Password Page
# def reset_password():
#     st.info("After redirection through the email you are able to reset the password")
#     token = st.query_params.get('token', [None])[0]
#     email = st.query_params.get('email', [None])[0]
    
#     reset_tokens = load_reset_tokens()

#     if token and email:
#         if token not in reset_tokens or reset_tokens[token]["email"] != email:
#             st.error("Invalid or expired reset link.")
#             return
        
#         expiry_time = datetime.fromisoformat(reset_tokens[token]["expiry"])
#         if datetime.utcnow() > expiry_time:
#             st.error("Reset link has expired.")
#             del reset_tokens[token]
#             save_reset_tokens(reset_tokens)
#             return
        
#         st.title("Reset Password")
#         new_password = st.text_input("New Password", type="password", key="new_password")
#         confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")
#         if new_password:
#             if st.button("Reset Password", key="reset_password_button"):
#                 if new_password != confirm_new_password:
#                     st.error("Passwords do not match.")
#                 else:
#                     user_data = load_user_data()
#                     hashed_password = hash_password(new_password)
                    
#                     if email in user_data:
#                         user_data[email]["password"] = hashed_password
#                         save_user_data(user_data)
#                         st.success("Password has been reset. You can now log in.")
#                         del reset_tokens[token]
#                         save_reset_tokens(reset_tokens)

# # Main Function with Navigation
# def main():
#     choice = st_navbar(["Home", "Documentation", "Examples", "Community", "About","Sign In", "Sign Up", "Reset Password"])
    
#     if choice == "Sign In":
#         signin()
#     elif choice == "Sign Up":
#         signup()
#     elif choice == "Reset Password":
#         reset_password()

# if __name__ == "__main__":
#     main()
