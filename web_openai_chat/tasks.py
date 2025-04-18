# from flask_mail import Message
# from extensions import mail
# from models import User
# from datetime import datetime
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# def send_welcome_email_task(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return
    
#     openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
#     if not openrouter_api_key:
#         return

#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json"
#     }
    
#     prompt = f"""
#     Generate a professional and welcoming email for a new user who has just registered on a flight booking platform (SkyWings). The user's details are:

#     - First Name: {user.first_name}
#     - Last Name: {user.last_name}
#     - Email: {user.email}
#     - Username: {user.username}

#     The email should have:
#     - A subject line like "Welcome to SkyWings - Your Journey Begins!"
#     - A greeting addressing the user by first name (e.g., "Dear [First Name]")
#     - A warm welcome message, mentioning their registration and the benefits of using SkyWings
#     - Instructions on how to log in and set up their profile
#     - Contact information for support
#     - A closing remark with best wishes
#     """

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json={
#                 "model": "deepseek/deepseek-chat-v3-0324:free",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "max_tokens": 1000,
#                 "temperature": 0.7
#             }
#         )

#         response.raise_for_status()
#         ai_response = response.json()
#         email_content = ai_response['choices'][0]['message']['content'].strip()

#         lines = email_content.split('\n')
#         subject = lines[0].replace("Subject: ", "").strip()
#         body = '\n'.join(lines[1:]).strip()

#         msg = Message(subject, recipients=[user.email])
#         msg.html = f"""
#         <html>
#             <body>
#                 <p>{body.replace('\n', '<br>')}</p>
#                 <p>Best regards,<br>The SkyWings Team</p>
#             </body>
#         </html>
#         """

#         mail.send(msg)
#     except Exception as e:
#         # Log the error but don't crash the application
#         print(f"Error sending welcome email: {str(e)}")

# def send_login_email_task(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return
    
#     openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
#     if not openrouter_api_key:
#         return

#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json"
#     }
    
#     login_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     prompt = f"""
#     Generate a professional and informative email to notify a user that they have successfully logged into the SkyWings flight booking platform. The user's details are:

#     - First Name: {user.first_name}
#     - Last Name: {user.last_name}
#     - Email: {user.email}
#     - Username: {user.username}

#     The email should have:
#     - A subject line like "Successful Login to SkyWings"
#     - A greeting addressing the user by first name
#     - A brief message confirming the successful login, including the date and time of login ({login_datetime})
#     - A reminder to contact support if the login was not initiated by them
#     - A closing remark with best wishes
#     """

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json={
#                 "model": "deepseek/deepseek-chat-v3-0324:free",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "max_tokens": 1000,
#                 "temperature": 0.7
#             }
#         )

#         response.raise_for_status()
#         ai_response = response.json()
#         email_content = ai_response['choices'][0]['message']['content'].strip()

#         lines = email_content.split('\n')
#         subject = lines[0].replace("Subject: ", "").strip()
#         body = '\n'.join(lines[1:]).strip()

#         msg = Message(subject, recipients=[user.email])
#         msg.html = f"""
#         <html>
#             <body>
#                 <p>{body.replace('\n', '<br>')}</p>
#                 <p>Best regards,<br>The SkyWings Team</p>
#             </body>
#         </html>
#         """

#         mail.send(msg)
#     except Exception as e:
#         print(f"Error sending login email: {str(e)}")

# def send_logout_email_task(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return
    
#     openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
#     if not openrouter_api_key:
#         return

#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json"
#     }

#     logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     prompt = f"""
#     Generate a professional and informative email to notify a user that they have successfully logged out of the SkyWings flight booking platform. The user's details are:

#     - First Name: {user.first_name}
#     - Last Name: {user.last_name}
#     - Email: {user.email}
#     - Username: {user.username}

#     The email should have:
#     - A subject line like "Successful Logout from SkyWings"
#     - A greeting addressing the user by first name
#     - A brief message confirming the successful logout, including the date and time of logout ({logout_time})
#     - A reminder to contact support if they did not initiate the logout
#     - A closing remark with best wishes
#     """

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json={
#                 "model": "deepseek/deepseek-chat-v3-0324:free",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "max_tokens": 1000,
#                 "temperature": 0.7
#             }
#         )

#         response.raise_for_status()
#         ai_response = response.json()
#         email_content = ai_response['choices'][0]['message']['content'].strip()

#         lines = email_content.split('\n')
#         subject = lines[0].replace("Subject: ", "").strip()
#         body = '\n'.join(lines[1:]).strip()

#         msg = Message(subject, recipients=[user.email])
#         msg.html = f"""
#         <html>
#             <body>
#                 <p>{body.replace('\n', '<br>')}</p>
#                 <p>Best regards,<br>The SkyWings Team</p>
#             </body>
#         </html>
#         """

#         mail.send(msg)
#     except Exception as e:
#         print(f"Error sending logout email: {str(e)}")