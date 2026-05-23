from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Конфигурация базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flowers.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'flower-shop-secret-key'

db = SQLAlchemy(app)

# Модель букета
class Bouquet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Bouquet {self.name}>'

# Создание таблиц БД
with app.app_context():
    db.create_all()

# Главная страница - каталог
@app.route('/')
def index():
    bouquets = Bouquet.query.all()
    return render_template('index.html', bouquets=bouquets)

# Страница администратора - управление каталогом
@app.route('/admin')
def admin():
    bouquets = Bouquet.query.all()
    return render_template('admin.html', bouquets=bouquets)

# Добавление букета
@app.route('/add', methods=['POST'])
def add_bouquet():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image_url = request.form.get('image_url')

    if name and price:
        try:
            price = float(price)
            bouquet = Bouquet(name=name, price=price, description=description, image_url=image_url)
            db.session.add(bouquet)
            db.session.commit()
        except ValueError:
            pass

    return redirect(url_for('admin'))

# Удаление букета
@app.route('/delete/<int:id>')
def delete_bouquet(id):
    bouquet = Bouquet.query.get_or_404(id)
    db.session.delete(bouquet)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
