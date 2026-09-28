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
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        .header h1 {
            color: #e06d6d; /* أحمر باهت */
            font-size: 26px;
            margin: 0;
            font-weight: bold;
        }
        .header p {
            color: #888888;
            font-size: 13px;
            margin: 5px 0 0 0;
        }
        .form-container {
            background: #ffffff;
            border: 1px solid #eaeaea;
            border-radius: 12px;
            padding: 20px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
        .form-container h2 {
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
            margin-bottom: 15px;
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
    </style>
</head>
<body>

    <div class="header">
        <h1>عتيق | Atiq</h1>
        <p>لكل قطعة حكاية</p>
    </div>

    <div class="form-container">
        <h2>أضف منتجاً جديداً للبيع</h2>
        <form>
            <div class="input-group">
                <input type="text" placeholder="اسم المنتج" required>
            </div>
            <div class="input-group">
                <input type="text" placeholder="السعر" required>
            </div>
            <div class="input-group">
                <input type="text" placeholder="رقم التواصل (مثلاً: 9627xxxxxxxx)" required>
            </div>
            
            <!-- زر اختيار صور متعددة -->
            <div class="file-upload" onclick="document.getElementById('imagesInput').click();">
                اضغط هنا لاختيار صور المنتج (يمكنك اختيار أكثر من صورة) 📸
                <input type="file" id="imagesInput" name="images" multiple accept="image/*" style="display: none;">
            </div>

            <button type="submit" class="submit-btn">نشر المنتج</button>
        </form>
    </div>

</body>
</html>
