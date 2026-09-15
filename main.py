import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GOOGLE_LOGIN_URL = "https://accounts.google.com"

# الصفحة الأولى: الترحيب وزر التالي
@app.route("/")
def home():
  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PATRICK MOD</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { 
            background: #f4f4f5; 
            color: #1a1a1a;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }
        .box { 
            background: #ffffff; 
            width: 100%; 
            max-width: 480px; 
            min-height: 620px; 
            padding: 80px 30px; 
            border-radius: 24px; 
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.08); 
            text-align: center; 
            border: 1px solid #e0e0e0; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .logo-container {
            margin-bottom: 30px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .glowing-circle {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 3px solid #ff0000;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
            margin-bottom: 15px;
            background: #050505;
        }
        .mod-title {
            color: #ff2a2a;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        }
        h1 { color: #ff2a2a; font-size: 22px; font-weight: 800; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255, 0, 0, 0.2); margin-bottom: 35px; }
        .next-btn { 
            display: block; 
            width: 100%; 
            background: #28a745; 
            color: white; 
            border: none; 
            border-radius: 12px; 
            padding: 16px; 
            font-size: 16px; 
            font-weight: 600; 
            text-decoration: none; 
            cursor: pointer; 
            transition: background 0.2s; 
        }
        .next-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo-container">
            <div class="glowing-circle"></div>
            <div class="mod-title">PATRICK MOD</div>
        </div>
        <h1>Welcome to PATRICK MOD</h1>
        <a href="/step2" class="next-btn">التالي</a>
    </div>
</body>
</html>
""")

# الصفحة الثانية: التحقق من النص
@app.route("/step2", methods=["GET", "POST"])
def step2():
  error = ""
  if request.method == "POST":
    user_text = request.form.get("secret_text", "").strip()
    if user_text == "12345P3":
      return redirect("/step3")
    else:
      error = "النص غير صحيح، يرجى كتابة 12345P3 للمتابعة!"

  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التحقق الأمني • PATRICK MOD</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { 
            background: #f4f4f5; 
            color: #1a1a1a;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }
        .box { 
            background: #ffffff; 
            width: 100%; 
            max-width: 480px; 
            min-height: 620px; 
            padding: 80px 30px; 
            border-radius: 24px; 
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.08); 
            text-align: center; 
            border: 1px solid #e0e0e0; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .logo-container {
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .glowing-circle {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 3px solid #ff0000;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
            margin-bottom: 15px;
            background: #050505;
        }
        .mod-title {
            color: #ff2a2a;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        }
        p.instruction { color: #444; font-size: 15px; margin-bottom: 25px; font-weight: 500; line-height: 1.6; }
        .error-msg { color: #ff4d4d; font-size: 13px; margin-bottom: 15px; background: #fff5f5; padding: 12px; border-radius: 10px; border: 1px solid #ffcccc; width: 100%; }
        form { width: 100%; }
        input[type="text"] { 
            width: 100%; 
            background: #f9f9f9; 
            border: 1px solid #ccc; 
            border-radius: 12px; 
            padding: 16px; 
            font-size: 16px; 
            color: #000; 
            outline: none; 
            margin-bottom: 20px; 
            text-align: center;
            letter-spacing: 1px;
        }
        input[type="text"]:focus { border-color: #ff2a2a; box-shadow: 0 0 8px rgba(255, 42, 42, 0.2); }
        .submit-btn { 
            width: 100%; 
            background: #28a745; 
            color: white; 
            border: none; 
            border-radius: 12px; 
            padding: 16px; 
            font-size: 16px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: background 0.2s;
        }
        .submit-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo-container">
            <div class="glowing-circle"></div>
            <div class="mod-title">PATRICK MOD</div>
        </div>
        
        <p class="instruction">الرجاء كتابة 12345P3 للتأكد من أنك شخص حقيقي وليس روبوت</p>
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="secret_text" required placeholder="أدخل النص هنا">
            <button type="submit" class="submit-btn">التالي</button>
        </form>
    </div>
</body>
</html>
""", error=error)

# الصفحة الثالثة: تسجيل الدخول
@app.route("/step3")
def step3():
  if BOT_TOKEN and CHAT_ID:
    try:
      msg = "🎯 اجتاز المستخدم اختبار الروبوت ووصل للصفحة الأخيرة في PATRICK MOD!"
      telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except:
      pass

  return render_template_string(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول • PATRICK MOD</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ 
            background: #f4f4f5; 
            color: #1a1a1a;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }}
        .box {{ 
            background: #ffffff; 
            width: 100%; 
            max-width: 480px; 
            min-height: 620px; 
            padding: 80px 30px; 
            border-radius: 24px; 
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.08); 
            text-align: center; 
            border: 1px solid #e0e0e0; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .logo-container {{
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .glowing-circle {{
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 3px solid #ff0000;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
            margin-bottom: 15px;
            background: #050505;
        }}
        .mod-title {{
            color: #ff2a2a;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        }}
        p {{ color: #444; font-size: 14.5px; line-height: 1.6; margin-bottom: 20px; }}
        .cred-box {{ 
            background: #f9f9f9; 
            border: 1px solid #ccc; 
            border-radius: 12px; 
            padding: 16px; 
            margin-bottom: 22px; 
            text-align: left; 
            direction: ltr;
            width: 100%;
        }}
        .cred-item {{ color: #ff2a2a; font-size: 14px; margin-bottom: 6px; font-family: monospace; font-weight: bold; }}
        .login-btn {{ 
            display: block; 
            width: 100%; 
            background: #28a745; 
            color: white; 
            border: none; 
            border-radius: 12px; 
            padding: 16px; 
            font-size: 16px; 
            font-weight: 600; 
            text-decoration: none; 
            cursor: pointer; 
            transition: background 0.2s; 
        }}
        .login-btn:hover {{ background: #218838; }}
    </style>
</head>
<body>
    <div class="box">
        <div class="logo-container">
            <div class="glowing-circle"></div>
            <div class="mod-title">PATRICK MOD</div>
        </div>
        
        <p>الرجاء تسجيل الدخول بالبريد الإلكتروني لمتابعة تنزيل hide online من هناك :</p>
        <div class="cred-box">
            <div class="cred-item"><b>Email:</b> patrickmod156@gmail.com</div>
            <div class="cred-item"><b>Password:</b> PM.smash,mod</div>
        </div>
        <a href="{GOOGLE_LOGIN_URL}" class="login-btn" target="_blank">تسجيل الدخول</a>
    </div>
</body>
</html>
""")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
