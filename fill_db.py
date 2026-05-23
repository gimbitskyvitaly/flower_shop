#!/usr/bin/env python3
"""
Скрипт для автоматического заполнения базы данных тестовыми данными.
Заполняет таблицу Bouquet тестовыми букетами с различными категориями,
получателями и праздниками.
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def fill_database():
    """Заполняет базу данных тестовыми данными."""
    
    # Создаём минимальное приложение для работы с БД
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flowers.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    # Определяем модель заново для доступа к БД
    class Bouquet(db.Model):
        __tablename__ = 'bouquet'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        price = db.Column(db.Float, nullable=False)
        description = db.Column(db.Text, nullable=True)
        image_file = db.Column(db.String(200), nullable=True)
        
        # Категории (виды цветов/букетов)
        category_bouquets = db.Column(db.Boolean, default=True)
        category_baskets = db.Column(db.Boolean, default=True)
        category_live = db.Column(db.Boolean, default=True)
        category_roses = db.Column(db.Boolean, default=True)
        category_tulips = db.Column(db.Boolean, default=True)
        category_violets = db.Column(db.Boolean, default=True)
        category_peonies = db.Column(db.Boolean, default=True)
        category_carnations = db.Column(db.Boolean, default=True)
        category_chrysanthemums = db.Column(db.Boolean, default=True)
        category_lilies = db.Column(db.Boolean, default=True)
        category_orchids = db.Column(db.Boolean, default=True)
        category_daisies = db.Column(db.Boolean, default=True)
        category_eustoma = db.Column(db.Boolean, default=True)
        category_alstroemeria = db.Column(db.Boolean, default=True)
        category_gerberas = db.Column(db.Boolean, default=True)
        category_irises = db.Column(db.Boolean, default=True)
        category_narcissus = db.Column(db.Boolean, default=True)
        category_mixed = db.Column(db.Boolean, default=True)
        
        # Кому дарить
        gift_grandma = db.Column(db.Boolean, default=True)
        gift_girlfriend = db.Column(db.Boolean, default=True)
        gift_wife = db.Column(db.Boolean, default=True)
        gift_mom = db.Column(db.Boolean, default=True)
        
        # Праздники
        holiday_march8 = db.Column(db.Boolean, default=True)
        holiday_feb14 = db.Column(db.Boolean, default=True)
        holiday_cheer = db.Column(db.Boolean, default=True)
        holiday_just = db.Column(db.Boolean, default=True)

        def __repr__(self):
            return f'<Bouquet {self.name}>'
    
    with app.app_context():
        # Очищаем существующие данные
        print("Очистка существующих данных...")
        Bouquet.query.delete()
        db.session.commit()
        
        # Тестовые данные
        test_bouquets = [
            {
                'name': 'Красные розы',
                'price': 2500.0,
                'description': 'Классический букет из 15 красных роз. Идеальный подарок для романтического свидания.',
                'image_file': None,
                'categories': ['roses', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'wife'],
                'holidays': ['feb14', 'march8', 'cheer']
            },
            {
                'name': 'Весенние тюльпаны',
                'price': 1800.0,
                'description': 'Нежные тюльпаны разных оттенков. Символ весны и обновления.',
                'image_file': None,
                'categories': ['tulips', 'bouquets', 'live'],
                'gifts': ['mom', 'grandma', 'girlfriend'],
                'holidays': ['march8', 'cheer', 'just']
            },
            {
                'name': 'Белые пионы',
                'price': 3200.0,
                'description': 'Роскошные белые пионы в полной красе. Премиум букет для особых случаев.',
                'image_file': None,
                'categories': ['peonies', 'bouquets', 'live'],
                'gifts': ['wife', 'girlfriend', 'mom'],
                'holidays': ['march8', 'feb14', 'cheer']
            },
            {
                'name': 'Полевые ромашки',
                'price': 1200.0,
                'description': 'Простой и очаровательный букет из ромашек. Напоминание о лете.',
                'image_file': None,
                'categories': ['daisies', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'mom', 'grandma'],
                'holidays': ['just', 'cheer']
            },
            {
                'name': 'Цветочная корзинка',
                'price': 2800.0,
                'description': 'Композиция из различных цветов в плетёной корзинке. Удобно и красиво.',
                'image_file': None,
                'categories': ['baskets', 'mixed', 'live'],
                'gifts': ['grandma', 'mom', 'wife'],
                'holidays': ['march8', 'cheer', 'just']
            },
            {
                'name': 'Лилии нежности',
                'price': 2100.0,
                'description': 'Ароматные лилии белого и розового цвета. Элегантность и грация.',
                'image_file': None,
                'categories': ['lilies', 'bouquets', 'live'],
                'gifts': ['wife', 'mom', 'girlfriend'],
                'holidays': ['march8', 'feb14', 'cheer']
            },
            {
                'name': 'Орхидея в горшке',
                'price': 1900.0,
                'description': 'Живая орхидея фаленопсис в декоративном горшке. Долговечный подарок.',
                'image_file': None,
                'categories': ['orchids', 'live'],
                'gifts': ['grandma', 'mom', 'wife'],
                'holidays': ['march8', 'cheer', 'just']
            },
            {
                'name': 'Яркие герберы',
                'price': 1600.0,
                'description': 'Разноцветные герберы поднимут настроение в любой день.',
                'image_file': None,
                'categories': ['gerberas', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'mom', 'grandma'],
                'holidays': ['cheer', 'just']
            },
            {
                'name': 'Ирисы мечты',
                'price': 1750.0,
                'description': 'Фиолетовые ирисы с неповторимым ароматом.',
                'image_file': None,
                'categories': ['irises', 'bouquets', 'live'],
                'gifts': ['wife', 'girlfriend'],
                'holidays': ['march8', 'feb14', 'cheer']
            },
            {
                'name': 'Микс цветов',
                'price': 2300.0,
                'description': 'Авторская композиция из сезонных цветов. Каждый букет уникален.',
                'image_file': None,
                'categories': ['mixed', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'wife', 'mom', 'grandma'],
                'holidays': ['march8', 'feb14', 'cheer', 'just']
            },
            {
                'name': 'Гвоздики классика',
                'price': 1400.0,
                'description': 'Традиционные гвоздики красного и белого цвета.',
                'image_file': None,
                'categories': ['carnations', 'bouquets', 'live'],
                'gifts': ['grandma', 'mom'],
                'holidays': ['march8', 'cheer']
            },
            {
                'name': 'Хризантемы осенние',
                'price': 1550.0,
                'description': 'Пушистые хризантемы тёплых осенних оттенков.',
                'image_file': None,
                'categories': ['chrysanthemums', 'bouquets', 'live'],
                'gifts': ['grandma', 'mom', 'wife'],
                'holidays': ['cheer', 'just']
            },
            {
                'name': 'Эустома нежность',
                'price': 1950.0,
                'description': 'Изящная эустома (лизиантус) пастельных тонов.',
                'image_file': None,
                'categories': ['eustoma', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'wife'],
                'holidays': ['march8', 'feb14', 'cheer']
            },
            {
                'name': 'Альстромерия радость',
                'price': 1650.0,
                'description': 'Яркая альстромерия с экзотическим узором на лепестках.',
                'image_file': None,
                'categories': ['alstroemeria', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'mom', 'grandma'],
                'holidays': ['cheer', 'just']
            },
            {
                'name': 'Нарциссы весна',
                'price': 1350.0,
                'description': 'Первые весенние нарциссы. Символ пробуждения природы.',
                'image_file': None,
                'categories': ['narcissus', 'bouquets', 'live'],
                'gifts': ['mom', 'grandma', 'girlfriend'],
                'holidays': ['march8', 'cheer']
            },
            {
                'name': 'Фиалки уют',
                'price': 900.0,
                'description': 'Комнатные фиалки в маленьких горшочках. Уют и тепло дома.',
                'image_file': None,
                'categories': ['violets', 'live'],
                'gifts': ['grandma', 'mom'],
                'holidays': ['just', 'cheer']
            },
            {
                'name': 'Розовый закат',
                'price': 2900.0,
                'description': 'Романтичный букет из розовых роз и эвкалипта.',
                'image_file': None,
                'categories': ['roses', 'bouquets', 'live'],
                'gifts': ['girlfriend', 'wife'],
                'holidays': ['feb14', 'march8', 'cheer']
            },
            {
                'name': 'Белое облако',
                'price': 3100.0,
                'description': 'Воздушный букет из белых роз, лилий и гипсофилы.',
                'image_file': None,
                'categories': ['roses', 'lilies', 'bouquets', 'live'],
                'gifts': ['wife', 'girlfriend'],
                'holidays': ['wedding', 'feb14', 'cheer']
            },
            {
                'name': 'Подарок бабушке',
                'price': 1700.0,
                'description': 'Тёплый и уютный букет для любимой бабушки.',
                'image_file': None,
                'categories': ['mixed', 'bouquets', 'live'],
                'gifts': ['grandma'],
                'holidays': ['march8', 'cheer', 'just']
            },
            {
                'name': 'Для мамы',
                'price': 2200.0,
                'description': 'Нежный букет из любимых маминых цветов.',
                'image_file': None,
                'categories': ['tulips', 'roses', 'bouquets', 'live'],
                'gifts': ['mom'],
                'holidays': ['march8', 'cheer']
            }
        ]
        
        # Создаём букеты
        print(f"Добавление {len(test_bouquets)} тестовых букетов...")
        
        for bouquet_data in test_bouquets:
            # Создаём объект букета
            bouquet = Bouquet(
                name=bouquet_data['name'],
                price=bouquet_data['price'],
                description=bouquet_data['description'],
                image_file=bouquet_data['image_file']
            )
            
            # Устанавливаем категории
            for cat in bouquet_data['categories']:
                category_attr = f'category_{cat}'
                if hasattr(bouquet, category_attr):
                    setattr(bouquet, category_attr, True)
            
            # Устанавливаем получателей
            for gift in bouquet_data['gifts']:
                gift_attr = f'gift_{gift}'
                if hasattr(bouquet, gift_attr):
                    setattr(bouquet, gift_attr, True)
            
            # Устанавливаем праздники
            for holiday in bouquet_data['holidays']:
                holiday_attr = f'holiday_{holiday}'
                if hasattr(bouquet, holiday_attr):
                    setattr(bouquet, holiday_attr, True)
            
            db.session.add(bouquet)
            print(f"  Добавлен: {bouquet.name} - {bouquet.price} руб.")
        
        # Сохраняем все изменения
        db.session.commit()
        print(f"\n✓ База данных успешно заполнена {len(test_bouquets)} тестовыми букетами!")


if __name__ == '__main__':
    fill_database()
