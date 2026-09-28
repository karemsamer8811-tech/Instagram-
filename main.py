from flask import Flask, render_template_string, request, redirect, url_for
import os
import base64

app = Flask(__name__)

# قائمة لتخزين المنتجات
products = []
product_id_counter = 1
ADMIN_PASSWORD = "samemomomo**1"

# إعدادات التحكم والخواص العامة
site_controls = {
    "block_posting": False,  
    "enable_search": True,
    "enable_socials": True,       
    "enable_copyright": True,
    "enable_contact_btn": True,   
    "social_links": [
        {"name": "إنستغرام", "url": "#"},
        {"name": "تيليجرام", "url": "#"}
    ],
    "copyright_text": "جميع الحقوق محفوظة © عتيق 2026. تم تصميم وتطوير المنصة بعناية فائقة."
}

# التحكم بإظهار أو إخفاء كل نص أو عنصر في الواجهة (True = ظاهر، False = مخفي)
text_visibility = {
    "heading_products": True,
    "no_products": True,
    "toggle_btn_open": True,
    "toggle_btn_close": True,
    "form_main_title": True,
    "label_title": True,
    "input_title_placeholder": True,
    "label_price": True,
    "input_price_placeholder": True,
    "label_contact_method": True,
    "contact_type_instagram": True,
    "contact_type_phone": True,
    "input_contact_placeholder": True,
    "upload_text": True,
    "submit_btn": True,
    "back_home": True,
    "view_details": True,
    "search_placeholder": True,
    "contact_word": True
}

# إعدادات واجهة الموقع ونصوصها الأساسية
site_config = {
    "title": "عتيق | Atiq",
    "subtitle": "لكل قطعة حكاية",
    "bg_image": "",
    "texts": {
        "heading_products": "المنتجات المعروضة",
        "no_products": "لا توجد منتجات معروضة حالياً.",
        "toggle_btn_open": "➕ إضافة منتج",
        "toggle_btn_close": "✖ إغلاق القائمة",
        "form_main_title": "أضف منتجاً جديداً للبيع",
        "label_title": "اسم المنتج",
        "input_title_placeholder": "أدخل اسم المنتج",
        "label_price": "السعر",
        "input_price_placeholder": "أدخل السعر",
        "label_contact_method": "طريقة التواصل",
        "contact_type_instagram": "حساب Instagram",
        "contact_type_phone": "الرقم الخاص بي",
        "input_contact_placeholder": "أدخل حساب الانستغرام أو الرقم",
        "upload_text": "اضغط هنا لاختيار صور المنتج 📸",
        "submit_btn": "نشر المنتج",
        "back_home": "← العودة إلى المتجر الرئيسي",
        "view_details": "عرض التفاصيل",
        "search_placeholder": "🔍 ابحث عن عنصر أو منتج...",
        "contact_word": "تواصل"
    },
    "colors": {
        "bg_color": "#000000",             
        "title": "#ff5252",                
        "subtitle": "#aaaaaa",             
        "logo_bg": "#000000",              
        "logo_border": "#ffffff",          
        "products_heading": "#ffffff",     
        "no_products": "#777777",          
        "product_title": "#ffffff",        
        "product_price": "#25d366",        
        "whatsapp_btn": "#25d366",         
        "toggle_btn": "#25d366",           
        "form_main_title": "#ffffff",      
        "label_title": "#cccccc",          
        "upload_text": "#ffffff",          
        "submit_btn": "#25d366"            
    }
}

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ config.title }}</title>
    <style>
        body {
            background-color: {{ config.colors.bg_color }};
            {% if config.bg_image %}
            background-image: url('{{ config.bg_image }}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            {% endif %}
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }
        {% if config.bg_image %}
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.75);
            z-index: -1;
        }
        {% endif %}
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
            margin-bottom: 25px;
        }
        .glass-title {
            background: {{ config.colors.logo_bg }};
            border: 2px solid {{ config.colors.logo_border }};
            display: inline-block;
            padding: 12px 25px;
            border-radius: 14px;
            color: {{ config.colors.title }};
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 0 20px {{ config.colors.logo_border }}66, inset 0 0 10px {{ config.colors.logo_border }}33;
            margin: 0;
        }
        .header p {
            color: {{ config.colors.subtitle }};
            font-size: 13px;
            margin: 10px 0 0 0;
            letter-spacing: 0.5px;
        }
        .search-box {
            width: 100%;
            max-width: 900px;
            margin-bottom: 20px;
        }
        .search-input {
            width: 100%;
            padding: 12px 18px;
            background: #111;
            border: 1px solid #333;
            border-radius: 10px;
            color: white;
            font-size: 14px;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.3s;
        }
        .search-input:focus {
            border-color: #25d366;
        }
        .products-section {
            width: 100%;
            max-width: 900px;
            margin-bottom: 20px;
            flex: 1;
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
            background: #111111;
            border: 1px solid #222222;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-decoration: none;
            transition: transform 0.2s;
        }
        .product-card:hover {
            transform: scale(1.02);
            border-color: #444;
        }
        .product-images {
            display: flex;
            flex-direction: row;
            overflow-x: auto;
            gap: 8px;
            background: #000;
            padding: 8px;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
            width: 100%;
            box-sizing: border-box;
        }
        .product-images::-webkit-scrollbar {
            height: 6px;
        }
        .product-images::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 4px;
        }
        .product-images img {
            width: 100%;
            height: 140px;
            object-fit: cover;
            border-radius: 6px;
            flex: 0 0 100%;
            scroll-snap-align: start;
        }
        .product-info {
            padding: 12px;
        }
        .product-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
            color: {{ config.colors.product_title }};
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .product-price {
            color: {{ config.colors.product_price }};
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .contact-btn {
            display: block;
            text-align: center;
            background: {{ config.colors.whatsapp_btn }};
            color: white;
            padding: 7px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 11px;
            word-break: break-all;
        }
        .toggle-form-btn {
            background-color: {{ config.colors.toggle_btn }};
            color: white;
            border: 2px solid #ffffff;
            padding: 12px 25px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
            transition: all 0.3s ease;
        }
        .container {
            background: #111111;
            border: 1px solid #222;
            border-radius: 12px;
            padding: 20px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.8);
            margin-bottom: 30px;
            display: none;
        }
        .container.active {
            display: block;
        }
        .form-main-title {
            color: {{ config.colors.form_main_title }};
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
            color: {{ config.colors.label_title }};
        }
        .input-group input[type="text"], .input-group input[type="password"], .input-group select {
            width: 100%;
            padding: 12px;
            border: 1px solid #333;
            border-radius: 8px;
            background: #000000;
            box-sizing: border-box;
            font-size: 14px;
            color: white;
            outline: none;
            margin-bottom: 8px;
        }
        .file-upload {
            border: 2px dashed #25d366;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            background: rgba(37, 211, 102, 0.03);
            cursor: pointer;
            margin-bottom: 10px;
            color: {{ config.colors.upload_text }};
            font-size: 13px;
            transition: background 0.3s;
        }
        .file-upload:hover {
            background: rgba(37, 211, 102, 0.08);
        }
        .submit-btn {
            background-color: {{ config.colors.submit_btn }};
            color: white;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
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
        .site-footer {
            width: 100%;
            max-width: 900px;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #222;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            text-align: center;
        }
        .footer-socials {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .footer-social-link {
            color: #aaa;
            text-decoration: none;
            font-size: 13px;
            background: #111;
            padding: 6px 14px;
            border-radius: 6px;
            border: 1px solid #222;
            transition: color 0.3s, border-color 0.3s;
        }
        .footer-social-link:hover {
            color: #25d366;
            border-color: #25d366;
        }
        .footer-copyright {
            color: #666;
            font-size: 12px;
            text-decoration: none;
            transition: color 0.3s;
        }
        .footer-copyright:hover {
            color: #aaa;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="/admin" class="settings-btn">الإعدادات</a>
    </div>

    <div class="header">
        <h1 class="glass-title">{{ config.title }}</h1>
        <p>{{ config.subtitle }}</p>
    </div>

    {% if controls.enable_search and vis.search_placeholder %}
    <div class="search-box">
        <input type="text" id="searchInput" class="search-input" placeholder="{{ config.texts.search_placeholder }}" onkeyup="filterProducts()">
    </div>
    {% endif %}

    <div class="products-section">
        {% if vis.heading_products %}
        <h2 style="color: {{ config.colors.products_heading }}; margin-bottom: 15px; text-align: right;">{{ config.texts.heading_products }}</h2>
        {% endif %}
        <div class="products-grid" id="productsGrid">
            {% if products|length == 0 and vis.no_products %}
                <p style="color: {{ config.colors.no_products }}; text-align: center; grid-column: 1 / -1; padding: 20px;" id="noProductsMsg">{{ config.texts.no_products }}</p>
            {% endif %}
            {% for p in products %}
                <div class="product-card" data-title="{{ p.title }}">
                    <div class="product-images">
                        {% for img in p.images %}
                            <img src="{{ img }}" alt="صورة">
                        {% endfor %}
                    </div>
                    <div class="product-info">
                        <div class="product-title" title="{{ p.title }}">{{ p.title }}</div>
                        <div class="product-price">{{ p.price }}</div>
                        {% if vis.view_details %}
                        <a href="/product/{{ p.id }}" class="contact-btn">{{ config.texts.view_details }}</a>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    {% if not controls.block_posting and (vis.toggle_btn_open or vis.toggle_btn_close) %}
    <button class="toggle-form-btn" onclick="toggleForm()" id="toggleBtn">{{ config.texts.toggle_btn_open }}</button>

    <div class="container {% if error %}active{% endif %}" id="formContainer">
        {% if vis.form_main_title %}
        <h2 class="form-main-title">{{ config.texts.form_main_title }}</h2>
        {% endif %}
        
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}

        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="input-group">
                {% if vis.label_title %}
                <label style="color: {{ config.colors.label_title }};">{{ config.texts.label_title }}</label>
                {% endif %}
                <input type="text" name="title" {% if vis.input_title_placeholder %}placeholder="{{ config.texts.input_title_placeholder }}"{% endif %} required>
            </div>
            <div class="input-group">
                {% if vis.label_price %}
                <label style="color: {{ config.colors.label_title }};">{{ config.texts.label_price }}</label>
                {% endif %}
                <input type="text" name="price" {% if vis.input_price_placeholder %}placeholder="{{ config.texts.input_price_placeholder }}"{% endif %} required>
            </div>
            <div class="input-group">
                {% if vis.label_contact_method %}
                <label style="color: {{ config.colors.label_title }};">{{ config.texts.label_contact_method }}</label>
                {% endif %}
                <select name="contact_type" required>
                    {% if vis.contact_type_instagram %}
                    <option value="instagram">{{ config.texts.contact_type_instagram }}</option>
                    {% endif %}
                    {% if vis.contact_type_phone %}
                    <option value="phone">{{ config.texts.contact_type_phone }}</option>
                    {% endif %}
                </select>
                <input type="text" name="contact_value" {% if vis.input_contact_placeholder %}placeholder="{{ config.texts.input_contact_placeholder }}"{% endif %} required>
            </div>
            {% if vis.upload_text %}
            <div class="file-upload" onclick="document.getElementById('imagesInput').click();">
                {{ config.texts.upload_text }}
                <input type="file" id="imagesInput" name="images" multiple accept="image/*" style="display: none;" onchange="showCount(this)">
            </div>
            <div id="file-count" style="font-size: 12px; color: #aaa; margin-bottom: 15px; text-align: center;"></div>
            {% endif %}

            {% if vis.submit_btn %}
            <button type="submit" class="submit-btn">{{ config.texts.submit_btn }}</button>
            {% endif %}
        </form>
    </div>
    {% endif %}

    {% if controls.enable_socials or controls.enable_copyright %}
    <footer class="site-footer">
        {% if controls.enable_socials and controls.social_links|length > 0 %}
        <div class="footer-socials">
            {% for s in controls.social_links %}
                <a href="{{ s.url }}" target="_blank" class="footer-social-link">{{ s.name }}</a>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if controls.enable_copyright %}
        <a href="/copyright" class="footer-copyright">حقوق النشر والشروط</a>
        {% endif %}
    </footer>
    {% endif %}

    <script>
        function toggleForm() {
            const container = document.getElementById('formContainer');
            const btn = document.getElementById('toggleBtn');
            if (container.style.display === 'block') {
                container.style.display = 'none';
                btn.innerText = '{{ config.texts.toggle_btn_open }}';
            } else {
                container.style.display = 'block';
                btn.innerText = '{{ config.texts.toggle_btn_close }}';
                container.scrollIntoView({ behavior: 'smooth' });
            }
        }

        window.onload = function() {
            {% if error %}
                const container = document.getElementById('formContainer');
                if(container) {
                    container.style.display = 'block';
                    document.getElementById('toggleBtn').innerText = '{{ config.texts.toggle_btn_close }}';
                }
            {% endif %}
        };

        function showCount(input) {
            if(input.files.length > 0) {
                document.getElementById('file-count').innerText = "✅ تم اختيار " + input.files.length + " صورة.";
            }
        }

        function filterProducts() {
            const input = document.getElementById('searchInput');
            if(!input) return;
            const filter = input.value.toLowerCase();
            const grid = document.getElementById('productsGrid');
            const cards = grid.getElementsByClassName('product-card');

            for (let i = 0; i < cards.length; i++) {
                let title = cards[i].getAttribute('data-title').toLowerCase();
                if (title.includes(filter)) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""

product_detail_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ product.title }} - {{ config.title }}</title>
    <style>
        body {
            background-color: {{ config.colors.bg_color }};
            color: #ffffff;
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .detail-container {
            background: #111111;
            border: 1px solid #222;
            border-radius: 14px;
            padding: 25px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.9);
            margin-top: 20px;
            text-align: center;
        }
        .gallery {
            display: flex;
            flex-direction: row;
            overflow-x: auto;
            gap: 10px;
            margin-bottom: 20px;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
        }
        .gallery::-webkit-scrollbar {
            height: 6px;
        }
        .gallery::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 4px;
        }
        .gallery img {
            width: 100%;
            max-height: 450px;
            object-fit: contain;
            border-radius: 8px;
            background: #000;
            border: 1px solid #333;
            flex: 0 0 100%;
            scroll-snap-align: start;
        }
        .product-title {
            font-size: 22px;
            font-weight: bold;
            color: {{ config.colors.product_title }};
            margin-bottom: 10px;
        }
        .product-price {
            font-size: 18px;
            color: {{ config.colors.product_price }};
            font-weight: bold;
            margin-bottom: 20px;
        }
        .contact-btn {
            display: block;
            text-align: center;
            background: {{ config.colors.whatsapp_btn }};
            color: white;
            padding: 12px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 15px;
        }
        .back-link {
            display: inline-block;
            color: #25d366;
            text-decoration: none;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="detail-container">
        <h1 class="product-title">{{ product.title }}</h1>
        <div class="product-price">{{ product.price }}</div>
        
        <div class="gallery">
            {% for img in product.images %}
                <img src="{{ img }}" alt="صورة المنتج">
            {% endfor %}
        </div>

        {% if controls.enable_contact_btn %}
            {% if product.contact_type == 'instagram' %}
                <a class="contact-btn" href="https://instagram.com/{{ product.contact_value.replace('@', '') }}" target="_blank">
                    {% if vis.contact_word %}{{ config.texts.contact_word }}: {% endif %}{{ product.contact_value }}
                </a>
            {% else %}
                <a class="contact-btn" href="https://wa.me/{{ product.contact_value }}" target="_blank">
                    {% if vis.contact_word %}{{ config.texts.contact_word }}: {% endif %}{{ product.contact_value }}
                </a>
            {% endif %}
        {% endif %}

        {% if vis.back_home %}
        <a href="/" class="back-link">{{ config.texts.back_home }}</a>
        {% endif %}
    </div>
</body>
</html>
"""

copyright_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حقوق النشر والشروط</title>
    <style>
        body { background: #000; color: #fff; font-family: Tahoma, sans-serif; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .box { background: #111; border: 1px solid #222; padding: 30px; border-radius: 12px; max-width: 600px; width: 100%; margin-top: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.8); line-height: 1.8; }
        h1 { color: #25d366; text-align: center; font-size: 20px; margin-bottom: 20px; }
        p { color: #ddd; font-size: 14px; white-space: pre-wrap; word-break: break-word; }
        .back { display: block; text-align: center; margin-top: 25px; color: #25d366; text-decoration: none; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>حقوق النشر والشروط</h1>
        <p>{{ text }}</p>
        <a href="/" class="back">← العودة إلى المتجر الرئيسي</a>
    </div>
</body>
</html>
"""

admin_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الإعدادات والتحكم</title>
    <style>
        body { background: #000000; color: #ffffff; font-family: Tahoma, sans-serif; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { background: #111111; padding: 25px; border-radius: 12px; border: 1px solid #222222; width: 100%; max-width: 650px; box-shadow: 0 10px 25px rgba(0,0,0,0.8); margin-top: 20px; }
        h2, h3 { color: #ffffff; text-align: center; margin-bottom: 20px; }
        input[type="text"], input[type="password"], textarea { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #333333; background: #000000; color: #ffffff; box-sizing: border-box; font-size: 13px; outline: none; }
        input[type="color"] { width: 50px; height: 32px; border: 1px solid #333333; border-radius: 6px; background: #000000; cursor: pointer; padding: 0; vertical-align: middle; }
        button { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 8px; background: #25d366; color: white; border: none; font-weight: bold; cursor: pointer; transition: background 0.3s; font-size: 15px; }
        button:hover { background: #1ebd56; }
        .product-row { display: flex; justify-content: space-between; align-items: center; background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #222222; }
        .delete-btn { background: #dc2626; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; width: auto; margin: 0; font-size: 13px; }
        .delete-btn:hover { background: #b91c1c; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #25d366; text-decoration: none; font-size: 14px; font-weight: bold; }
        .section-box { border-top: 1px solid #222222; margin-top: 25px; padding-top: 20px; }
        .row-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; background: #000000; padding: 6px 10px; border-radius: 6px; border: 1px solid #222222; }
        .row-item span { font-size: 12px; color: #cccccc; width: 40%; }
        .row-item input[type="text"] { width: 45%; margin: 0; }
        label { display: block; margin-bottom: 5px; font-size: 13px; color: #ffffff; font-weight: bold; }
        .checkbox-label { display: flex; align-items: center; gap: 10px; background: #000000; padding: 10px; border-radius: 8px; border: 1px solid #222222; cursor: pointer; margin-bottom: 10px; font-size: 14px; color: #ffffff; font-weight: normal; }
        .checkbox-label input { width: 18px; height: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>لوحة الإعدادات والتحكم</h2>
        {% if not authorized %}
            <form method="POST">
                <p style="margin-bottom: 12px; font-size: 14px; color: #cccccc; text-align: center;">الرجاء إدخال رمز المرور للوصول:</p>
                <input type="password" name="password" placeholder="رمز المرور" required>
                <button type="submit">دخول</button>
            </form>
            {% if error %}
                <p style="color: #ef4444; text-align: center; font-size: 13px; margin-top: 10px;">❌ رمز المرور غير صحيح!</p>
            {% endif %}
        {% else %}
            <p style="color: #25d366; text-align: center; margin-bottom: 15px; font-weight: bold;">تم تسجيل الدخول بنجاح</p>
            
            <div class="section-box">
                <h3>إدارة الخصائص والميزات العامة</h3>
                <form action="/update-controls" method="POST">
                    <label class="checkbox-label">
                        <input type="checkbox" name="block_posting" {% if controls.block_posting %}checked{% endif %}>
                        منع المستخدمين من إضافة ونشر منتجات جديدة
                    </label>
                    
                    <label class="checkbox-label">
                        <input type="checkbox" name="enable_search" {% if controls.enable_search %}checked{% endif %}>
                        تفعيل شريط البحث عن العناصر في الواجهة
                    </label>

                    <label class="checkbox-label">
                        <input type="checkbox" name="enable_contact_btn" {% if controls.enable_contact_btn %}checked{% endif %}>
                        تفعيل وعرض زر ورقم/طريقة التواصل في صفحة تفاصيل المنتج
                    </label>

                    <label class="checkbox-label">
                        <input type="checkbox" name="enable_socials" {% if controls.enable_socials %}checked{% endif %}>
                        تفعيل وعرض حسابات التواصل الاجتماعي في أسفل المتجر
                    </label>

                    <label class="checkbox-label">
                        <input type="checkbox" name="enable_copyright" {% if controls.enable_copyright %}checked{% endif %}>
                        تفعيل وعرض صفحة وحقوق النشر في أسفل المتجر
                    </label>

                    <button type="submit" style="margin-top: 10px;">حفظ الخصائص العامة</button>
                </form>
            </div>

            <div class="section-box">
                <h3>إدارة إظهار، إطفاء وتعديل نصوص وكلمات الموقع</h3>
                <form action="/update-texts" method="POST">
                    <p style="font-size: 12px; color: #888; margin-bottom: 12px; text-align: center;">ضع علامة صح لإظهار الكلمة أو قم بإزالتها لإطفائها، ويمكنك تعديل النص.</p>
                    
                    {% for key, val in config.texts.items() %}
                        <div class="row-item">
                            <label style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #fff; cursor: pointer; width: 45%; margin: 0;">
                                <input type="checkbox" name="vis_{{ key }}" {% if vis[key] %}checked{% endif %} style="width: 16px; height: 16px; cursor: pointer;">
                                {{ key }}
                            </label>
                            <input type="text" name="txt_{{ key }}" value="{{ val }}" required>
                        </div>
                    {% endfor %}

                    <button type="submit" style="margin-top: 15px;">حفظ النصوص وإعدادات الظهور</button>
                </form>
            </div>

            <div class="section-box">
                <h3>إدارة حسابات التواصل (تظهر أسفل المتجر)</h3>
                <form action="/update-socials" method="POST">
                    <label>اسم الحساب الأول:</label>
                    <input type="text" name="s1_name" value="{{ controls.social_links[0].name if controls.social_links|length > 0 else '' }}" placeholder="مثال: إنستغرام">
                    <label>رابط الحساب الأول:</label>
                    <input type="text" name="s1_url" value="{{ controls.social_links[0].url if controls.social_links|length > 0 else '' }}" placeholder="https://instagram.com/...">

                    <label style="margin-top: 15px;">اسم الحساب الثاني:</label>
                    <input type="text" name="s2_name" value="{{ controls.social_links[1].name if controls.social_links|length > 1 else '' }}" placeholder="مثال: تيليجرام">
                    <label>رابط الحساب الثاني:</label>
                    <input type="text" name="s2_url" value="{{ controls.social_links[1].url if controls.social_links|length > 1 else '' }}" placeholder="https://t.me/...">

                    <button type="submit" style="margin-top: 10px;">حفظ الحسابات</button>
                </form>
            </div>

            <div class="section-box">
                <h3>تعديل صفحة حقوق النشر</h3>
                <form action="/update-copyright" method="POST">
                    <label>النص الذي سيظهر في صفحة حقوق النشر:</label>
                    <textarea name="copyright_text" rows="5" required>{{ controls.copyright_text }}</textarea>
                    <button type="submit">حفظ نص حقوق النشر</button>
                </form>
            </div>

            <div class="section-box">
                <h3>تغيير كلمة المرور</h3>
                <form action="/update-password" method="POST">
                    <label>كلمة المرور الجديدة:</label>
                    <input type="password" name="new_password" placeholder="أدخل كلمة المرور الجديدة" required>
                    <button type="submit">تحديث كلمة المرور</button>
                </form>
            </div>

            <div class="section-box">
                <h3>تعديل واجهة وألوان الموقع</h3>
                <form action="/update-config" method="POST" enctype="multipart/form-data">
                    <label>اسم الموقع:</label>
                    <input type="text" name="title" value="{{ config.title }}" required>
                    
                    <label>شعار / وصف الموقع:</label>
                    <input type="text" name="subtitle" value="{{ config.subtitle }}" required>

                    <label>صورة خلفية الواجهة (من المعرض):</label>
                    <input type="file" name="bg_image_file" accept="image/*" style="margin-bottom: 10px; color: #ffffff;">
                    
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #000; padding: 8px 12px; border-radius: 6px; border: 1px solid #222; margin-bottom: 15px;">
                        <span style="font-size: 13px; color: #ccc;">إلغاء وإزالة صورة الخلفية الحالية؟</span>
                        <input type="checkbox" name="remove_bg_image" style="width: 18px; height: 18px; cursor: pointer;">
                    </div>

                    <h3 style="margin-top: 25px; font-size: 15px; border-bottom: 1px solid #222222; padding-bottom: 8px;">تعديل ألوان أجزاء الموقع</h3>
                    
                    <div class="row-item">
                        <span>لون خلفية الموقع:</span>
                        <input type="color" name="c_bg_color" value="{{ config.colors.bg_color }}">
                    </div>
                    <div class="row-item">
                        <span>عنوان الموقع الرئيسي:</span>
                        <input type="color" name="c_title" value="{{ config.colors.title }}">
                    </div>
                    <div class="row-item">
                        <span>لون خلفية مربع الشعار:</span>
                        <input type="color" name="c_logo_bg" value="{{ config.colors.logo_bg }}">
                    </div>
                    <div class="row-item">
                        <span>إطار وتوهج مربع الشعار (Atiq):</span>
                        <input type="color" name="c_logo_border" value="{{ config.colors.logo_border }}">
                    </div>
                    <div class="row-item">
                        <span>وصف الموقع:</span>
                        <input type="color" name="c_subtitle" value="{{ config.colors.subtitle }}">
                    </div>
                    <div class="row-item">
                        <span>عنوان المنتجات المعروضة:</span>
                        <input type="color" name="c_products_heading" value="{{ config.colors.products_heading }}">
                    </div>
                    <div class="row-item">
                        <span>جملة لا توجد منتجات:</span>
                        <input type="color" name="c_no_products" value="{{ config.colors.no_products }}">
                    </div>
                    <div class="row-item">
                        <span>عنوان المنتج:</span>
                        <input type="color" name="c_product_title" value="{{ config.colors.product_title }}">
                    </div>
                    <div class="row-item">
                        <span>سعر المنتج:</span>
                        <input type="color" name="c_product_price" value="{{ config.colors.product_price }}">
                    </div>
                    <div class="row-item">
                        <span>زر التواصل:</span>
                        <input type="color" name="c_whatsapp_btn" value="{{ config.colors.whatsapp_btn }}">
                    </div>
                    <div class="row-item">
                        <span>زر فتح/إغلاق القائمة:</span>
                        <input type="color" name="c_toggle_btn" value="{{ config.colors.toggle_btn }}">
                    </div>
                    <div class="row-item">
                        <span>عنوان نموذج الإضافة:</span>
                        <input type="color" name="c_form_main_title" value="{{ config.colors.form_main_title }}">
                    </div>
                    <div class="row-item">
                        <span>عناوين الحقول ( Labels ):</span>
                        <input type="color" name="c_label_title" value="{{ config.colors.label_title }}">
                    </div>
                    <div class="row-item">
                        <span>جملة اختيار الصور:</span>
                        <input type="color" name="c_upload_text" value="{{ config.colors.upload_text }}">
                    </div>
                    <div class="row-item">
                        <span>زر نشر المنتج:</span>
                        <input type="color" name="c_submit_btn" value="{{ config.colors.submit_btn }}">
                    </div>
                    
                    <button type="submit" style="margin-top: 15px;">حفظ الألوان والتصميم</button>
                </form>
            </div>

            <div class="section-box">
                <h3>قائمة المنتجات (للحذف)</h3>
                <div>
                    {% if products|length == 0 %}
                        <p style="color: #888888; text-align: center; padding: 15px;">لا توجد منتجات مسجلة حالياً.</p>
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
            </div>
        {% endif %}
        <a href="/" class="back-link">← العودة إلى المتجر الرئيسي</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, products=products, config=site_config, controls=site_controls, vis=text_visibility, error=None)

@app.route('/product/<int:p_id>')
def product_detail(p_id):
    product = next((p for p in products if p['id'] == p_id), None)
    if not product:
        return redirect(url_for('index'))
    return render_template_string(product_detail_template, product=product, config=site_config, controls=site_controls, vis=text_visibility)

@app.route('/copyright')
def copyright_page():
    if not site_controls['enable_copyright']:
        return redirect(url_for('index'))
    return render_template_string(copyright_template, text=site_controls['copyright_text'])

@app.route('/add', methods=['POST'])
def add_product():
    global product_id_counter
    if site_controls['block_posting']:
        return redirect(url_for('index'))
        
    title = request.form.get('title')
    price = request.form.get('price')
    contact_type = request.form.get('contact_type')
    contact_value = request.form.get('contact_value', '').strip()
    image_files = request.files.getlist('images')
    
    if len(contact_value) <= 5:
        error_message = "❌ خطأ: رقم التواصل غير صحيح (يجب أن يكون أطول من 5 أحرف)."
        return render_template_string(html_template, products=products, config=site_config, controls=site_controls, vis=text_visibility, error=error_message)

    images_list = []
    for img_file in image_files:
        if img_file and img_file.filename != '':
            image_bytes = img_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            images_list.append(f"data:image/jpeg;base64,{image_base64}")
    
    if title and price and contact_value and images_list:
        products.insert(0, {
            "id": product_id_counter,
            "title": title, 
            "price": price, 
            "contact_type": contact_type,
            "contact_value": contact_value,
            "images": images_list
        })
        product_id_counter += 1
        
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global ADMIN_PASSWORD
    authorized = False
    error = False
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            authorized = True
        else:
            error = True
    return render_template_string(admin_template, products=products, config=site_config, controls=site_controls, vis=text_visibility, authorized=authorized, error=error)

@app.route('/update-controls', methods=['POST'])
def update_controls():
    global site_controls
    site_controls['block_posting'] = True if request.form.get('block_posting') == 'on' else False
    site_controls['enable_search'] = True if request.form.get('enable_search') == 'on' else False
    site_controls['enable_contact_btn'] = True if request.form.get('enable_contact_btn') == 'on' else False
    site_controls['enable_socials'] = True if request.form.get('enable_socials') == 'on' else False
    site_controls['enable_copyright'] = True if request.form.get('enable_copyright') == 'on' else False
    return redirect(url_for('admin'))

@app.route('/update-texts', methods=['POST'])
def update_texts():
    global site_config, text_visibility
    for key in site_config['texts']:
        form_txt = request.form.get(f'txt_{key}')
        if form_txt:
            site_config['texts'][key] = form_txt
        text_visibility[key] = True if request.form.get(f'vis_{key}') == 'on' else False
    return redirect(url_for('admin'))

@app.route('/update-socials', methods=['POST'])
def update_socials():
    global site_controls
    s1_name = request.form.get('s1_name', '').strip()
    s1_url = request.form.get('s1_url', '').strip()
    s2_name = request.form.get('s2_name', '').strip()
    s2_url = request.form.get('s2_url', '').strip()
    
    new_links = []
    if s1_name and s1_url:
        new_links.append({"name": s1_name, "url": s1_url})
    if s2_name and s2_url:
        new_links.append({"name": s2_name, "url": s2_url})
        
    site_controls['social_links'] = new_links
    return redirect(url_for('admin'))

@app.route('/update-copyright', methods=['POST'])
def update_copyright():
    global site_controls
    text = request.form.get('copyright_text', '').strip()
    if text:
        site_controls['copyright_text'] = text
    return redirect(url_for('admin'))

@app.route('/update-password', methods=['POST'])
def update_password():
    global ADMIN_PASSWORD
    new_pwd = request.form.get('new_password', '').strip()
    if new_pwd:
        ADMIN_PASSWORD = new_pwd
    return redirect(url_for('admin'))

@app.route('/update-config', methods=['POST'])
def update_config():
    global site_config
    site_config['title'] = request.form.get('title', site_config['title'])
    site_config['subtitle'] = request.form.get('subtitle', site_config['subtitle'])
    
    for key in site_config['colors']:
        form_val = request.form.get(f'c_{key}')
        if form_val:
            site_config['colors'][key] = form_val
    
    if request.form.get('remove_bg_image') == 'on':
        site_config['bg_image'] = ""

    bg_file = request.files.get('bg_image_file')
    if bg_file and bg_file.filename != '':
        bg_bytes = bg_file.read()
        bg_base64 = base64.b64encode(bg_bytes).decode('utf-8')
        site_config['bg_image'] = f"data:image/jpeg;base64,{bg_base64}"
        
    return redirect(url_for('admin'))

@app.route('/delete/<int:p_id>', methods=['POST'])
def delete_product(p_id):
    global products
    products = [p for p in products if p['id'] != p_id]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
