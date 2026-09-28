from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# قائمة مؤقتة لتخزين المنتجات (يمكنك استبدالها بقاعدة بيانات لاحقاً)
products = [
    {"title": "باقة ورد جوري", "price": "10 دينار", "phone": "962700000000", "image": "https://images.unsplash.com/photo-1561181286-d3fee7d55364?w=400"},
    {"title": "تحفة خشبية يدوية", "price": "25 دينار", "phone": "962700000000", "image": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=400"}
]

# قالب الصفحة الواحدة (HTML + CSS + JavaScript)
html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة البيع السريع</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { background-color: #0f172a; color: #e2e8f0; padding: 20px; }
        header { text-align: center; margin-bottom: 30px; }
        header h1 { color: #f8fafc; font-size: 28px; }
        .container { max-width: 800px; margin: auto; background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        h2 { margin-bottom: 15px; font-size: 20px; color: #38bdf8; }
        form input { display: block; width: 100%; margin-bottom: 12px; padding: 10px; font-size: 15px; background: #0f172a; border: 1px solid #475569; color: white; border-radius: 6px; }
        form button { background: #25d366; color: white; border: none; width: 100%; padding: 10px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        form button:hover { background: #1ebe5d; }
        .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
        .product-card { background: #0f172a; border: 1px solid #334155; border-radius: 8px; overflow: hidden; }
        .product-card img { width: 100%; height: 160px; object-fit: cover; }
        .product-info { padding: 12px; }
        .product-title { font-size: 16px; font-weight: bold; margin-bottom: 5px; color: #f8fafc; }
        .product-price { color: #f43f5e; font-weight: bold; margin-bottom: 10px; }
        .whatsapp-btn { display: block; text-align: center; background: #25d366; color: white; padding: 8px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>

    <header>
        <h1>🛍️ منصة عرض وبيع المنتجات</h1>
    </header>

    <div class="container">
        <h2>أضف منتجاً جديداً</h2>
        <form action="/add" method="POST">
            <input type="text" name="title" placeholder="اسم المنتج (مثلاً: باقة ورد، تحفة)" required>
            <input type="text" name="price" placeholder="السعر (مثلاً: 15 دينار)" required>
            <input type="text" name="phone" placeholder="رقم الواتساب (مثلاً: 9627xxxxxxxx)" required>
            <input type="text" name="image" placeholder="رابط صورة المنتج (صورة من الإنترنت)" required>
            <button type="submit">نشر المنتج</button>
        </form>
    </div>

    <div class="container">
        <h2>المنتجات المعروضة</h2>
        <div class="products-grid">
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
    image = request.form.get('image')
    
    if title and price and phone and image:
        products.insert(0, {"title": title, "price": price, "phone": phone, "image": image})
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
