from flask import Flask, render_template_string, request, redirect, url_for
import os
import base64

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
            background-color: #f8f9fa;
            color: #333333;
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .top-bar {
            width: 100%;
            max-width: 800px;
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }
        .settings-btn {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 8px 15px;
            border-radius: 8px;
            text-decoration: none;
            color: #e06d6d;
            font-size: 13px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
            transition: background 0.3s;
        }
        .settings-btn:hover {
            background: #fff0f0;
        }
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        .header h1 {
            color: #e06d6d;
            font-size: 28px;
            margin: 0;
            font-weight: bold;
        }
        .header p {
            color: #888888;
            font-size: 13px;
            margin: 5px 0 0 0;
        }
        .container {
            background: #ffffff;
            border: 1px solid #eaeaea;
            border-radius: 12px;
            padding: 20px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            margin-bottom: 30px;
        }
        h2 {
            color: #e06d6d;
            font-size: 18px;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
            box-sizing: border-box;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-group input:focus {
            border-color: #e06d6d;
        }
        .file-upload {
            border: 2px dashed #e06d6d;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            background: #fff8f8;
            cursor: pointer;
            margin-bottom: 10px;
            color: #e06d6d;
            font-size: 13px;
            transition: background 0.3s;
        }
        .file-upload:hover {
            background: #fff0f0;
        }
        .submit-btn {
            background-color: #e06d6d;
            color: white;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .submit-btn:hover {
            background-color: #cc5c5c;
        }
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 20px;
            width: 100%;
            max-width: 800px;
        }
        .product-card {
            background: #ffffff;
            border: 1px solid #eaeaea;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .product-images {
            display: flex;
            overflow-x: auto;
            gap: 5px;
            background: #111;
            padding: 5px;
            max-height: 160px;
        }
        .product-images img {
            width: 130px;
            height: 150px;
            object-fit: cover;
            border-radius: 4px;
            flex-shrink: 0;
        }
        .product-info {
            padding: 15px;
        }
        .product-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .product-price {
            color: #e06d6d;
            font-weight: bold;
            margin-bottom: 12px;
            font-size: 15px;
        }
        .whatsapp-btn {
            display: block;
            text-align: center;
            background: #25d366;
            color: white;
            padding: 9px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }
        .whatsapp-btn:hover {
            background: #1ebe5d;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="/admin" class="settings-btn">⚙️ الإعدادات (لوحة التحكم)</a>
    </div>

    <div class="header">
        <h1>عتيق | Atiq</h1>
        <p>لكل قطعة حكاية</p>
    </div>

    <div class="container">
        <h2>أضف منتجاً جديداً للبيع</h2>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="input-group">
                <input type="text" name="title" placeholder="اسم المنتج" required>
            </div>
            <div class="input-group">
                <input type="text" name="price" placeholder="السعر" required>
            </div>
            <div class="input-group">
                <input type="text" name="phone" placeholder="رقم التواصل (مثلاً: 9627xxxxxxxx)" required>
            </div>
            
            <div class="file-upload" onclick="document.getElementById('imagesInput').click();">
                اضغط هنا لاختيار صور المنتج (يمكنك اختيار أكثر من صورة) 📸
                <input type="file" id="imagesInput" name="images" multiple accept="image/*" style="display: none;" onchange="showCount(this)">
            </div>
            <div id="file-count" style="font-size: 12px; color: #666; margin-bottom: 15px; text-align: center;"></div>

            <button type="submit" class="submit-btn">نشر المنتج</button>
        </form>
    </div>

    <h2 style="color: #e06d6d; margin-bottom: 15px; width: 100%; max-width: 800px; text-align: right;">المنتجات المعروضة</h2>
    <div class="products-grid">
        {% if products|length == 0 %}
            <p style="color: #888; text-align: center; grid-column: 1 / -1; padding: 20px;">لا توجد منتجات معروضة حالياً.</p>
        {% endif %}
        {% for p in products %}
            <div class="product-card">
                <div class="product-images">
                    {% for img in p.images %}
                        <img src="{{ img }}" alt="صورة">
                    {% endfor %}
                </div>
                <div class="product-info">
                    <div class="product-title">{{ p.title }}</div>
                    <div class="product-price">{{ p.price }}</div>
                    <a class="whatsapp-btn" href="https://wa.me/{{ p.phone }}?text=مرحباً، أنا مهتم بشراء ({{ p.title }})" target="_blank">تواصل عبر واتساب</a>
                </div>
            </div>
        {% endfor %}
    </div>

    <script>
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
        body { background: #f8f9fa; color: #333; font-family: Tahoma, sans-serif; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { background: #fff; padding: 25px; border-radius: 12px; border: 1px solid #eaeaea; width: 100%; max-width: 600px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-top: 20px; }
        h2 { color: #e06d6d; text-align: center; margin-bottom: 20px; }
        input, button { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; font-size: 14px; outline: none; }
        input:focus { border-color: #e06d6d; }
        button { background: #e06d6d; color: white; border: none; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #cc5c5c; }
        .product-row { display: flex; justify-content: space-between; align-items: center; background: #fafafa; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #eee; }
        .delete-btn { background: #dc2626; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; width: auto; margin: 0; font-size: 13px; }
        .delete-btn:hover { background: #b91c1c; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #e06d6d; text-decoration: none; font-size: 14px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>لوحة الإعدادات والتحكم</h2>
        {% if not authorized %}
            <form method="POST">
                <p style="margin-bottom: 12px; font-size: 14px; color: #666; text-align: center;">الرجاء إدخال رمز المرور للوصول:</p>
                <input type="password" name="password" placeholder="رمز المرور" required>
                <button type="submit">دخول</button>
            </form>
            {% if error %}
                <p style="color: #dc2626; text-align: center; font-size: 13px; margin-top: 10px;">❌ رمز المرور غير صحيح!</p>
            {% endif %}
        {% else %}
            <p style="color: #16a34a; text-align: center; margin-bottom: 15px; font-weight: bold;">تم تسجيل الدخول بنجاح</p>
            <h3 style="font-size: 16px; margin-bottom: 15px; color: #444;">قائمة المنتجات (للحذف):</h3>
            <div>
                {% if products|length == 0 %}
                    <p style="color: #888; text-align: center; padding: 15px;">لا توجد منتجات مسجلة حالياً.</p>
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
    return render_template_string(html_template, products=products)

@app.route('/add', methods=['POST'])
def add_product():
    global product_id_counter
    title = request.form.get('title')
    price = request.form.get('price')
    phone = request.form.get('phone')
    image_files = request.files.getlist('images')
    
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
