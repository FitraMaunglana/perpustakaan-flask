import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

# === Konfigurasi dasar ===
app = Flask(__name__)
app.secret_key = 'fitra-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perpustakaan.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
ALLOWED_EXTENSIONS = {'pdf'}

db = SQLAlchemy(app)

# === Flask-Login setup ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# === Model database ===
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    penulis = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    filename = db.Column(db.String(300))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    isi = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Util ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === Routing utama ===
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books, user=current_user)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    comments = Comment.query.filter_by(book_id=book.id).all()
    if request.method == 'POST':
        nama = request.form['nama']
        isi = request.form['isi']
        if nama and isi:
            c = Comment(nama=nama, isi=isi, book_id=book.id)
            db.session.add(c)
            db.session.commit()
            flash('Komentar berhasil dikirim!')
        return redirect(url_for('detail', book_id=book.id))
    return render_template('detail.html', book=book, comments=comments, user=current_user)

@app.route('/uploads/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# === Login & Logout ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login berhasil!')
            return redirect(url_for('admin'))
        else:
            flash('Username atau password salah!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.')
    return redirect(url_for('index'))

# === Admin upload ===
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        deskripsi = request.form['deskripsi']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            new_book = Book(judul=judul, penulis=penulis, deskripsi=deskripsi, filename=filename)
            db.session.add(new_book)
            db.session.commit()
            flash('Buku berhasil diunggah!')
            return redirect(url_for('admin'))
        else:
            flash('Format file harus PDF!')
    books = Book.query.all()
    return render_template('admin.html', books=books, user=current_user)

# === Inisialisasi DB & buat akun admin ===
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='minku').first():
        admin_user = User(username='minku', password='minku32')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
