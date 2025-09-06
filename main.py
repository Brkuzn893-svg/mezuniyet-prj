from flask import Flask, render_template, request, redirect
import os
from model import get_class
app = Flask(__name__)

# Yüklenen dosyaların kaydedileceği dizin
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','jfif'}

# Dosyanın izin verilen bir uzantıya sahip olup olmadığını kontrol eden fonksiyon
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Görseli model ile analiz et
        class_name, confidence = get_class(file_path)
        
        # Sonuçları kullanıcıya göster
        return render_template('result.html', class_name=class_name, confidence=confidence, filename=filename)

    return 'Geçersiz dosya tipi'

def model_tahmin(resim_dosyasi):

    return 'plastik sise'
@app.route('/nesne', methods=['GET','POST'])
def nesne_sayfa():
    if request.method == 'POST':
        # Burada modeli kullanarak nesneyi tahmin ediyorsun
        nesne = model_tahmin(request.files['resim'])
        
        # Nesneye göre bilgi metni
        if nesne == 'plastik sise':
            metin = "Bu bir plastik şişedir.Plastik  geri dönüşüm kutusuna atınız."
        elif nesne == 'cam sise':
            metin = "Bu bir cam şişedir. Kırılgandır, dikkatli olun ve cam geri dönüşüm kutusuna atınız."
        else:
            metin = "Bu nesne tanınamadı."
        
        return render_template('sonuc.html', metin=metin)
    
    return render_template('form.html')
if __name__ == '__main__':
    # images klasörünün var olduğundan emin olalım
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=8080)
