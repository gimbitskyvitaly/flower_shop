from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

def create_app():
    app = Flask(__name__)
    
    # Конфигурация базы данных
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flowers.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'flower-shop-secret-key-change-in-production'
    
    # Конфигурация загрузки файлов
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    # Создаем папку для загрузок если не существует
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    db = SQLAlchemy(app)
    
    # Модель букета
    class Bouquet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        price = db.Column(db.Float, nullable=False)
        description = db.Column(db.Text, nullable=True)
        image_file = db.Column(db.String(200), nullable=True)  # Имя файла изображения

        def __repr__(self):
            return f'<Bouquet {self.name}>'
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    # Создание таблиц БД
    with app.app_context():
        db.create_all()

    # Главная страница - каталог
    @app.route('/')
    def index():
        bouquets = Bouquet.query.all()
        return render_template('index.html', bouquets=bouquets)

    # Страница входа для администратора
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            password = request.form.get('password')
            # Пароль администратора: admin123 (в production заменить на env variable)
            if password == 'admin123':
                session['admin_logged_in'] = True
                flash('Вы успешно вошли как администратор!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Неверный пароль!', 'error')
        return render_template('login.html')

    # Выход из админ-панели
    @app.route('/logout')
    def logout():
        session.pop('admin_logged_in', None)
        flash('Вы вышли из админ-панели.', 'info')
        return redirect(url_for('index'))

    # Страница администратора - управление каталогом
    @app.route('/admin')
    def admin():
        if not session.get('admin_logged_in'):
            flash('Пожалуйста, войдите как администратор.', 'warning')
            return redirect(url_for('login'))
        bouquets = Bouquet.query.all()
        return render_template('admin.html', bouquets=bouquets)

    # Добавление букета
    @app.route('/add', methods=['POST'])
    def add_bouquet():
        if not session.get('admin_logged_in'):
            flash('Требуется авторизация администратора.', 'error')
            return redirect(url_for('login'))
        
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        
        # Обработка загруженного файла
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Добавляем timestamp чтобы избежать коллизий
                import time
                timestamp = int(time.time())
                ext = filename.rsplit('.', 1)[1].lower()
                image_file = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))

        if name and price:
            try:
                price = float(price)
                bouquet = Bouquet(name=name, price=price, description=description, image_file=image_file)
                db.session.add(bouquet)
                db.session.commit()
                flash('Букет успешно добавлен!', 'success')
            except ValueError:
                flash('Ошибка: неверный формат цены.', 'error')

        return redirect(url_for('admin'))

    # Удаление букета
    @app.route('/delete/<int:id>')
    def delete_bouquet(id):
        if not session.get('admin_logged_in'):
            flash('Требуется авторизация администратора.', 'error')
            return redirect(url_for('login'))
        
        bouquet = Bouquet.query.get_or_404(id)
        
        # Удаляем файл изображения если он существует
        if bouquet.image_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], bouquet.image_file)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(bouquet)
        db.session.commit()
        flash('Букет успешно удалён!', 'success')
        return redirect(url_for('admin'))

    return app

app = create_app()

def main():
    """Точка входа для запуска через uv run start"""
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()
