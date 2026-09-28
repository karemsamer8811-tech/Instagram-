تفضل! تم إعادة ترتيب الصفحة بحيث تصبح "المنتجات المعروضة" في البداية، يليها زر "إاضافة منتج" أنيق. عند الضغط على هذا الزر، ستفتح أو تنكشف قائمة أو نافذة إدخال بيانات المنتج الجديد مباشرة.
قم بنسخ هذا الكود بالكامل واستبداله داخل ملف main.py على GitHub:
from flask import Flask, render_template_string, request, redirect, url_for
import os
import base64
import re

app = Flask(__name__)

# قائمة لتخزين المنتجات
products = []
product_id_counter = 1
ADMIN_PASSWORD = "samemomomo**1"

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عتيق | Atiq</title>
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .top-bar {
            width: 100%;
            max-width: 900px;
            display: flex;
            justify-content: flex-end;
            margin-bottom: 15px;
        }
        .settings-btn {
            background: #1e1e1e;
            border: 1px solid #444;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .settings-btn:hover {
            background: #2a2a2a;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        /* خلفية حمراء مع إطار أبيض لامع ونصوص بيضاء */
        .glass-title {
            background: #ff5252;
            border: 2px solid #ffffff;
            display: inline-block;
            padding: 12px 25px;
            border-radius: 14px;
            color: #ffffff;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.4), inset 0 0 10px rgba(255, 255, 255, 0.3);
            margin: 0;
        }
        .header p {
            color: #aaaaaa;
            font-size: 13px;
            margin: 10px 0 0 0;
            letter-spacing: 0.5px;
        }
        
        /* زر إظهار/إخفاء نموذج الإضافة */
        .toggle-form-btn {
            background-color: #ff5252;
            color: white;
            border: 2px solid #ffffff;
            padding: 12px 25px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(255, 82, 82, 0.4);
            transition: all 0.3s ease;
        }
        .toggle-form-btn:hover {
            background-color: #ff1717;
            transform: scale(1.02);
        }

        /* صندوق النموذج المخفي افتراضياً ويظهر عند النقر */
        .container {
            background: #1a1a1a;
            border: 1px solid #2c2c2c;
            border-radius: 12px;
            padding: 20px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            margin-bottom: 30px;
            display: none; /* مخفي في البداية */
        }
        .container.active {
            display: block; /* يظهر عند النقر */
        }

        .form-main-title {
            color: #ffffff;
            font-size: 18px;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 13px;
            color: #ccc;
        }
        .input-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #333;
            border-radius: 8px;
            background: #121212;
            box-sizing: border-box;
            font-size: 14px;
            color: white;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-group input:focus {
            border-color: #ff6b6b;
        }
        .file-upload {
            border: 2px dashed #ff6b6b;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            background: rgba(255, 107, 107, 0.03);
            cursor: pointer;
            margin-bottom: 10px;
            color: #ff6b6b;
            font-size: 13px;
            transition: background 0.3s;
        }
        .file-upload:hover {
            background: rgba(255, 107, 107, 0.08);
        }
        .submit-btn {
            background-color: #ff5252;
            color: white;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        .submit-btn:hover {
            background-color: #ff1717;
        }
        .error-msg {
            background: rgba(220, 38, 38, 0.1);
            border: 1px solid #dc2626;
            color: #ef4444;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            font-size: 13px;
            margin-bottom: 15px;
        }
        
        /* قسم المنتجات في الأعلى */
        .products-section {
            width: 100%;
            max-width: 900px;
            margin-bottom: 20px;
        }
        .products-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            width: 100%;
        }
        @media (min-width: 768px) {
            .products-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        .product-card {
            background: #1a1a1a;
            border: 1px solid #2c2c2c;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .product-images {
            display: flex;
            overflow-x: auto;
            gap: 4px;
            background: #000;
            padding: 4px;
            max-height: 140px;
        }
        .product-images img {
            width: 100%;
            height: 130px;
            object-fit: cover;
            border-radius: 4px;
            flex-shrink: 0;
        }
        .product-info {
            padding: 12px;
        }
        .product-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .product-price {
            color: #ff6b6b;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .whatsapp-btn {
            display: block;
            text-align: center;
            background: #25d366;
            color: white;
            padding: 7px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
        }
        .whatsapp-btn:hover {
            background: #1ebe5d;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="/admin" class="settings-btn">الإعدادات</a>
    </div>

    <div class="header">
        <h1 class="glass-title">عتيق | Atiq</h1>
        <p>لكل قطعة حكاية</p>
    </div>

    <!-- 1. قسم المنتجات المعروضة أولاً -->
    <div class="products-section">
        <h2 style="color: #ff6b6b; margin-bottom: 15px; text-align: right;">المنتجات المعروضة</h2>
        <div class="products-grid">
            {% if products|length == 0 %}
                <p style="color: #777; text-align: center; grid-column: 1 / -1; padding: 20px;">لا توجد منتجات معروضة حالياً.</p>
            {% endif %}
            {% for p in products %}
                <div class="product-card">
                    <div class="product-images">
                        {% for img in p.images %}
                            <img src="{{ img }}" alt="صورة">
                        {% endfor %}
                    </div>
                    <div class="product-info">
                        <div class="product-title" title="{{ p.title }}">{{ p.title }}</div>
                        <div class="product-price">{{ p.price }}</div>
                        <a class="whatsapp-btn" href="https://wa.me/{{ p.phone }}?text=مرحباً، أنا مهتم بشراء ({{ p.title }})" target="_blank">تواصل عبر واتساب</a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    <!-- 2. زر إضافة منتج -->
    <button class="toggle-form-btn" onclick="toggleForm()" id="toggleBtn">➕ إضافة منتج</button>

    <!-- 3. قائمة الإدخال (تفتح عند الضغط على الزر) -->
    <div class="container {% if error %}active{% endif %}" id="formContainer">
        <h2 class="form-main-title">أضف منتجاً جديداً للبيع</h2>
        
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="input-group">
                <label>اسم المنتج</label>
                <input type="text" name="title" placeholder="أدخل اسم المنتج" required>
            </div>
            <div class="input-group">
                <label>السعر</label>
                <input type="text" name="price" placeholder="أدخل السعر" required>
            </div>
            
            <div class="input-group">
                <label>رقم التواصل</label>
                <input type="text" name="phone" placeholder="رقم التواصل" required>
            </div>
            
            <div class="file-upload" onclick="document.getElementById('imagesInput').click();">
                اضغط هنا لاختيار صور المنتج 📸
                <input type="file" id="imagesInput" name="images" multiple accept="image/*" style="display: none;" onchange="showCount(this)">
            </div>
            <div id="file-count" style="font-size: 12px; color: #aaa; margin-bottom: 15px; text-align: center;"></div>

            <button type="submit" class="submit-btn">نشر المنتج</button>
        </form>
    </div>

    <script>
        function toggleForm() {
            const container = document.getElementById('formContainer');
            const btn = document.getElementById('toggleBtn');
            if (container.style.display === 'block') {
                container.style.display = 'none';
                btn.innerText = '➕ إضافة منتج';
            } else {
                container.style.display = 'block';
                btn.innerText = '✖ إغلاق القائمة';
                container.scrollIntoView({ behavior: 'smooth' });
            }
        }

        // إذا حدث خطأ أثناء الإرسال، اجعل القائمة مفتوحة تلقائياً
        window.onload = function() {
            {% if error %}
                document.getElementById('formContainer').style.display = 'block';
                document.getElementById('toggleBtn').innerText = '✖ إغلاق القائمة';
            {% endif %}
        };

        function showCount(input) {
            if(input.files.length > 0) {
                document.getElementById('file-count').innerText = "✅ تم اختيار " + input.files.length + " صورة.";
            }
        }
    </script>
</body>
</html>
"""

admin_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - عتيق</title>
    <style>
        body { background: #121212; color: #e0e0e0; font-family: Tahoma, sans-serif; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { background: #1a1a1a; padding: 25px; border-radius: 12px; border: 1px solid #2c2c2c; width: 100%; max-width: 600px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); margin-top: 20px; }
        h2 { color: #ff6b6b; text-align: center; margin-bottom: 20px; }
        input, button { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #333; background: #121212; color: white; box-sizing: border-box; font-size: 14px; outline: none; }
        input:focus { border-color: #ff6b6b; }
        button { background: #ff5252; color: white; border: none; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #ff1717; }
        .product-row { display: flex; justify-content: space-between; align-items: center; background: #121212; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #2c2c2c; }
        .delete-btn { background: #dc2626; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; width: auto; margin: 0; font-size: 13px; }
        .delete-btn:hover { background: #b91c1c; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #ff6b6b; text-decoration: none; font-size: 14px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>لوحة الإعدادات والتحكم</h2>
        {% if not authorized %}
            <form method="POST">
                <p style="margin-bottom: 12px; font-size: 14px; color: #aaa; text-align: center;">الرجاء إدخال رمز المرور للوصول:</p>
                <input type="password" name="password" placeholder="رمز المرور" required>
                <button type="submit">دخول</button>
            </form>
            {% if error %}
                <p style="color: #dc2626; text-align: center; font-size: 13px; margin-top: 10px;">❌ رمز المرور غير صحيح!</p>
            {% endif %}
        {% else %}
            <p style="color: #16a34a; text-align: center; margin-bottom: 15px; font-weight: bold;">تم تسجيل الدخول بنجاح</p>
            <h3 style="font-size: 16px; margin-bottom: 15px; color: #ccc;">قائمة المنتجات (للحذف):</h3>
            <div>
                {% if products|length == 0 %}
                    <p style="color: #777; text-align: center; padding: 15px;">لا توجد منتجات مسجلة حالياً.</p>
                {% endif %}
                {% for p in products %}
                    <div class="product-row">
                        <span><b>{{ p.title }}</b> ({{ p.price }})</span>
                        <form action="/delete/{{ p.id }}" method="POST" style="margin:0;">
                            <button type="submit" class="delete-btn">حذف</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        <a href="/" class="back-link">← العودة إلى المتجر الرئيسي</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, products=products, error=None)

@app.route('/add', methods=['POST'])
def add_product():
    global product_id_counter
    title = request.form.get('title')
    price = request.form.get('price')
    phone = request.form.get('phone', '').strip()
    image_files = request.files.getlist('images')
    
    # التحقق من أن رقم الهاتف يتكون من أرقام فقط وأطول من 7 خانات
    if not phone.isdigit() or len(phone) <= 7:
        error_message = "❌ خطأ: يجب أن يتكون رقم التواصل من أرقام فقط وأن يكون أطول من 7 خانات."
        return render_template_string(html_template, products=products, error=error_message)

    images_list = []
    for img_file in image_files:
        if img_file and img_file.filename != '':
            image_bytes = img_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            images_list.append(f"data:image/jpeg;base64,{image_base64}")
    
    if title and price and phone and images_list:
        products.insert(0, {
            "id": product_id_counter,
            "title": title, 
            "price": price, 
            "phone": phone, 
            "images": images_list
        })
        product_id_counter += 1
        
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    authorized = False
    error = False
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            authorized = True
        else:
            error = True
    return render_template_string(admin_template, products=products, authorized=authorized, error=error)

@app.route('/delete/<int:p_id>', methods=['POST'])
def delete_product(p_id):
    global products
    products = [p for p in products if p['id'] != p_id]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

