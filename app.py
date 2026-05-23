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
        
        # Категории (виды цветов/букетов)
        category_bouquets = db.Column(db.Boolean, default=True)  # Букеты цветов
        category_baskets = db.Column(db.Boolean, default=True)   # Цветы в корзинках
        category_live = db.Column(db.Boolean, default=True)      # Живые цветы
        category_roses = db.Column(db.Boolean, default=True)     # Розы
        category_tulips = db.Column(db.Boolean, default=True)    # Тюльпаны
        category_violets = db.Column(db.Boolean, default=True)   # Фиалки
        
        # Кому дарить
        gift_grandma = db.Column(db.Boolean, default=True)    # Бабушке
        gift_girlfriend = db.Column(db.Boolean, default=True) # Девушке
        gift_wife = db.Column(db.Boolean, default=True)       # Жене
        gift_mom = db.Column(db.Boolean, default=True)        # Маме
        
        # Праздники
        holiday_march8 = db.Column(db.Boolean, default=True)      # 8 марта
        holiday_feb14 = db.Column(db.Boolean, default=True)       # 14 февраля
        holiday_cheer = db.Column(db.Boolean, default=True)       # Порадовать
        holiday_just = db.Column(db.Boolean, default=True)        # Просто так

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
        # Получаем параметры фильтрации из URL
        category_filter = request.args.get('category')  # фильтр по категории
        price_min = request.args.get('price_min', type=float)  # минимальная цена
        price_max = request.args.get('price_max', type=float)  # максимальная цена
        gift_filter = request.args.get('gift')  # кому дарить
        holiday_filter = request.args.get('holiday')  # праздник
        
        # Базовый запрос
        query = Bouquet.query
        
        # Применяем фильтры
        if category_filter:
            category_column = f'category_{category_filter}'
            if hasattr(Bouquet, category_column):
                query = query.filter(getattr(Bouquet, category_column) == True)
        
        if price_min is not None:
            query = query.filter(Bouquet.price >= price_min)
        
        if price_max is not None:
            query = query.filter(Bouquet.price <= price_max)
        
        if gift_filter:
            gift_column = f'gift_{gift_filter}'
            if hasattr(Bouquet, gift_column):
                query = query.filter(getattr(Bouquet, gift_column) == True)
        
        if holiday_filter:
            holiday_column = f'holiday_{holiday_filter}'
            if hasattr(Bouquet, holiday_column):
                query = query.filter(getattr(Bouquet, holiday_column) == True)
        
        bouquets = query.all()
        return render_template('index.html', bouquets=bouquets, 
                             active_category=category_filter,
                             active_gift=gift_filter,
                             active_holiday=holiday_filter,
                             price_min=price_min,
                             price_max=price_max)

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
                # Получаем значения чекбоксов категорий
                category_bouquets = request.form.get('category_bouquets') == 'on'
                category_baskets = request.form.get('category_baskets') == 'on'
                category_live = request.form.get('category_live') == 'on'
                category_roses = request.form.get('category_roses') == 'on'
                category_tulips = request.form.get('category_tulips') == 'on'
                category_violets = request.form.get('category_violets') == 'on'
                
                # Получаем значения чекбоксов "кому дарить"
                gift_grandma = request.form.get('gift_grandma') == 'on'
                gift_girlfriend = request.form.get('gift_girlfriend') == 'on'
                gift_wife = request.form.get('gift_wife') == 'on'
                gift_mom = request.form.get('gift_mom') == 'on'
                
                # Получаем значения чекбоксов праздников
                holiday_march8 = request.form.get('holiday_march8') == 'on'
                holiday_feb14 = request.form.get('holiday_feb14') == 'on'
                holiday_cheer = request.form.get('holiday_cheer') == 'on'
                holiday_just = request.form.get('holiday_just') == 'on'
                
                bouquet = Bouquet(
                    name=name, 
                    price=price, 
                    description=description, 
                    image_file=image_file,
                    category_bouquets=category_bouquets,
                    category_baskets=category_baskets,
                    category_live=category_live,
                    category_roses=category_roses,
                    category_tulips=category_tulips,
                    category_violets=category_violets,
                    gift_grandma=gift_grandma,
                    gift_girlfriend=gift_girlfriend,
                    gift_wife=gift_wife,
                    gift_mom=gift_mom,
                    holiday_march8=holiday_march8,
                    holiday_feb14=holiday_feb14,
                    holiday_cheer=holiday_cheer,
                    holiday_just=holiday_just
                )
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
