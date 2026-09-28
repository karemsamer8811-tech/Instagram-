from flask import Flask, render_template_string, request, redirect, url_for
import os
import base64

app = Flask(__name__)

# قائمة لتخزين المنتجات مع صورها المحفوظة كـ Base64
products = []

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة أنتيكا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body {
            background-color: #050505;
            color: #f3f4f6;
            padding: 20px;
            background-image: radial-gradient(circle at 50% 10%, rgba(220, 38, 38, 0.15) 0%, transparent 60%);
            min-height: 100vh;
        }
        header { text-align: center; margin-bottom: 30px; }
        header h1 {
            color: #ef4444;
            font-size: 30px;
            text-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
            letter-spacing: 1px;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: rgba(18, 18, 18, 0.85);
            padding: 25px;
            border-radius: 14px;
            border: 1px solid rgba(239, 68, 68, 0.3);
            margin-bottom: 30px;
            box-shadow: 0 0 25px rgba(239, 68, 68, 0.1);
            backdrop-filter: blur(10px);
        }
        h2 { margin-bottom: 15px; font-size: 20px; color: #ef4444; text-shadow: 0 0 8px rgba(239, 68, 68, 0.3); }
        
        label.file-upload-label {
            display: block;
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            background: #111;
            border: 2px dashed rgba(239, 68, 68, 0.5);
            color: #9ca3af;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        label.file-upload-label:hover {
            border-color: #ef4444;
            color: #f3f4f6;
            background: rgba(239, 68, 68, 0.05);
        }
        input[type="file"] { display: none; }

        form input {
            display: block;
            width: 100%;
            margin-bottom: 15px;
            padding: 12px;
            font-size: 15px;
            background: #111;
            border: 1px solid #333;
            color: white;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.3s;
        }
        form input:focus {
            border-color: #ef4444;
            box-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
        }
        form button {
            background: linear-gradient(135deg, #dc2626, #991b1b);
            color: white;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        form button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(220, 38, 38, 0.6);
        }
        .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
        .product-card {
            background: #111;
            border: 1px solid #222;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            transition: transform 0.3s, border-color 0.3s;
        }
        .product-card:hover {
            transform: translateY(-3px);
            border-color: rgba(239, 68, 68, 0.5);
        }
        .product-card img { width: 100%; height: 160px; object-fit: cover; }
        .product-info { padding: 15px; }
        .product-title { font-size: 17px; font-weight: bold; margin-bottom: 5px; color: #f3f4f6; }
        .product-price { color: #ef4444; font-weight: bold; margin-bottom: 12px; font-size: 16px; }
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
            box-shadow: 0 3px 10px rgba(37, 211, 102, 0.3);
            transition: background 0.2s;
        }
        .whatsapp-btn:hover { background: #1ebe5d; }
    </style>
</head>
<body>

    <header>
        <h1>🔥 منصة أنتيكا لبيع الأغراض المستعملة 🔥</h1>
    </header>

    <div class="container">
        <h2>أضف منتجاً جديداً للبيع</h2>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <input type="text" name="title" placeholder="اسم المنتج" required>
            <input type="text" name="price" placeholder="السعر" required>
            <input type="text" name="phone" placeholder="رقم التواصل (مثلاً: 9627xxxxxxxx)" required>
            
            <label class="file-upload-label" id="file-label">
                📷 اضغط هنا لاختيار صورة المنتج من المعرض
                <input type="file" name="image" accept="image/*" required onchange="updateFileName(this)">
            </label>

            <button type="submit">نشر المنتج</button>
        </form>
    </div>

    <div class="container">
        <h2>المنتجات المعروضة</h2>
        <div class="products-grid">
            {% if products|length == 0 %}
                <p style="color: #666; text-align: center; grid-column: 1 / -1; padding: 20px;">لا توجد منتجات معروضة حالياً. كن أول من يضيف منتجاً!</p>
            {% endif %}
            {% for p in products %}
                <div class="product-card">
                    <img src="{{ p.image }}" alt="{{ p.title }}">
                    <div class="product-info">
                        <div class="product-title">{{ p.title }}</div>
                        <div class="product-price">{{ p.price }}</div>
                        <a class="whatsapp-btn" href="https://wa.me/{{ p.phone }}?text=مرحباً، أنا مهتم بشراء ({{ p.title }})" target="_blank">تواصل عبر واتساب</a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    <script>
        function updateFileName(input) {
            const label = document.getElementById('file-label');
            if (input.files && input.files[0]) {
                label.style.borderColor = '#ef4444';
                label.style.color = '#ef4444';
                label.innerHTML = '✅ تم اختيار الصورة: ' + input.files[0].name;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, products=products)

@app.route('/add', methods=['POST'])
def add_product():
    title = request.form.get('title')
    price = request.form.get('price')
    phone = request.form.get('phone')
    image_file = request.files.get('image')
    
    if title and price and phone and image_file:
        # قراءة الصورة وتحويلها لـ Base64 لضمان عملها بشكل ممتاز وثابت على السيرفر
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_data = f"data:image/jpeg;base64,{image_base64}"
        
        products.insert(0, {
            "title": title, 
            "price": price, 
            "phone": phone, 
            "image": image_data
        })
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
