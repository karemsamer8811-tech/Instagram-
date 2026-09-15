import os
import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "hohosbid_super_secret_key")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MEDIAFIRE_URL = "https://www.mediafire.com/file/61ugass1zqpavlm/Hide_Online_v4.9.50_Mod__40_Updated__41_.apk/file"

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
            background: #0b0b0b; 
            color: #f5f5f5;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }
        .box { 
            background: #141414; 
            width: 100%; 
            max-width: 400px; 
            padding: 35px 25px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(220, 20, 60, 0.15); 
            text-align: center; 
            border: 1px solid #260a0a; 
        }
        h1 { color: #ff2a2a; font-size: 20px; font-weight: 800; margin-bottom: 25px; text-shadow: 0 0 10px rgba(255, 0, 0, 0.4); }
        .next-btn { 
            display: block; 
            width: 100%; 
            background: #ff2a2a; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            padding: 12px; 
            font-size: 15px; 
            font-weight: 600; 
            text-decoration: none; 
            cursor: pointer; 
            transition: background 0.2s; 
        }
        .next-btn:hover { background: #e02424; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Welcome to PATRICK MOD</h1>
        <a href="/step2" class="next-btn">التالي</a>
    </div>
</body>
</html>
""")

# الصفحة الثانية: إدخال النص والتحقق من أنه مطابق تماماً لـ 12345P3
@app.route("/step2", methods=["GET", "POST"])
def step2():
  error = ""
  if request.method == "POST":
    user_text = request.form.get("secret_text", "").strip()
    if user_text == "12345P3":
      return redirect("/step3")
    else:
      error = "الرجاء إدخال النص الصحيح للمتابعة!"

  return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التحقق من النص • PATRICK MOD</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { 
            background: #0b0b0b; 
            color: #f5f5f5;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }
        .box { 
            background: #141414; 
            width: 100%; 
            max-width: 400px; 
            padding: 35px 25px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(220, 20, 60, 0.15); 
            text-align: center; 
            border: 1px solid #260a0a; 
        }
        p.instruction { color: #cccccc; font-size: 15px; margin-bottom: 20px; font-weight: 500; }
        .error-msg { color: #ed4956; font-size: 12px; margin-bottom: 12px; background: #1c1c1c; padding: 8px; border-radius: 6px; border: 1px solid #331a1a; }
        input[type="text"] { 
            width: 100%; 
            background: #000; 
            border: 1px solid #333; 
            border-radius: 6px; 
            padding: 12px; 
            font-size: 15px; 
            color: #fff; 
            outline: none; 
            margin-bottom: 15px; 
            text-align: center;
        }
        input[type="text"]:focus { border-color: #ff2a2a; }
        .submit-btn { 
            width: 100%; 
            background: #ff2a2a; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            padding: 12px; 
            font-size: 15px; 
            font-weight: 600; 
            cursor: pointer; 
        }
        .submit-btn:hover { background: #e02424; }
    </style>
</head>
<body>
    <div class="box">
        <p class="instruction">الرجاء وضع نص</p>
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

# الصفحة الثالثة: عرض معلومات التسجيل ورابط التحميل
@app.route("/step3")
def step3():
  # إرسال إشعار لتليجرام عند وصول المستخدم للصفحة الثالثة بنجاح
  if BOT_TOKEN and CHAT_ID:
    try:
      msg = "🎯 وصل المستخدم إلى الصفحة الأخيرة بنجاح في PATRICK MOD!"
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
    <title>تنزيل الملف • PATRICK MOD</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ 
            background: #0b0b0b; 
            color: #f5f5f5;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            width: 100vw; 
            padding: 20px; 
        }}
        .box {{ 
            background: #141414; 
            width: 100%; 
            max-width: 420px; 
            padding: 35px 25px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(220, 20, 60, 0.15); 
            text-align: center; 
            border: 1px solid #260a0a; 
        }}
        p {{ color: #d0d0d0; font-size: 14px; line-height: 1.6; margin-bottom: 20px; }}
        .cred-box {{ 
            background: #000; 
            border: 1px solid #333; 
            border-radius: 8px; 
            padding: 15px; 
            margin-bottom: 25px; 
            text-align: left; 
            direction: ltr;
        }}
        .cred-item {{ color: #ff5252; font-size: 14px; margin-bottom: 5px; font-family: monospace; }}
        .download-btn {{ 
            display: block; 
            width: 100%; 
            background: #28a745; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            padding: 12px; 
            font-size: 15px; 
            font-weight: 600; 
            text-decoration: none; 
            cursor: pointer; 
            transition: background 0.2s; 
        }}
        .download-btn:hover {{ background: #218838; }}
    </style>
</head>
<body>
    <div class="box">
        <p>الرجاء التسجيل بالبريد الإلكتروني لتنزيل الملف من هناك :</p>
        <div class="cred-box">
            <div class="cred-item"><b>Email:</b> patrickmod156@gmail.com</div>
            <div class="cred-item"><b>Password:</b> PM.smash,mod</div>
        </div>
        <a href="{MEDIAFIRE_URL}" class="download-btn" target="_blank">تنزيل الملف</a>
    </div>
</body>
</html>
""")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
