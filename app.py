import os
from flask import Flask, render_template
from models import db, User, Supply

app = Flask(__name__)

# Generowanie bezwzględnej ścieżki do pliku bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    supplies = Supply.query.all()
    return render_template('index.html', supplies=supplies)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Dodanie przykładowych danych użytkowników i zaopatrzenia
        if User.query.count() == 0:  # Sprawdzenie czy baza jest pusta
            user1 = User(username='user1', email='user1@example.com')
            user2 = User(username='user2', email='user2@example.com')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
        
        if Supply.query.count() == 0:  # Sprawdzenie czy tabela zaopatrzenia jest pusta
            supply1 = Supply(product_name='Ołówki', category='Artykuły papiernicze', location='101', quantity=100, status='Na stanie')
            supply2 = Supply(product_name='Kreda', category='Artykuły papiernicze', location='102', quantity=200, status='Na stanie')
            db.session.add(supply1)
            db.session.add(supply2)
            db.session.commit()

    app.run(debug=True)
