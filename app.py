import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Supply

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Generowanie bezwzględnej ścieżki do pliku bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    supplies = Supply.query.all()
    users = User.query.all()

    return render_template('index.html', supplies=supplies, users=users)

@app.route('/edit/<int:supply_id>', methods=['GET', 'POST'])
def edit_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        if not quantity:
            return render_template('edit_supply.html', supply=supply)
        
        try:
            supply.quantity = int(quantity)
            db.session.commit()
            return redirect(url_for('home'))
        except ValueError:
            return render_template('edit_supply.html', supply=supply)
    return render_template('edit_supply.html', supply=supply)


@app.route('/add', methods=['POST'])
def add_supply():
    product_name = request.form.get('product_name')
    category = request.form.get('category')
    location = request.form.get('location')
    quantity = request.form.get('quantity')
    status = request.form.get('status')

    if not all([product_name, category, location, quantity, status]):
        return redirect(url_for('home'))

    try:
        new_supply = Supply(
            product_name=product_name,
            category=category,
            location=location,
            quantity=int(quantity),
            status=status
        )
        db.session.add(new_supply)
        db.session.commit()
    except ValueError:
        flash('Będne wartości!', 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Dodanie przykładowych danych użytkowników i zaopatrzenia
        if User.query.count() == 0:  # Sprawdzenie czy baza jest pusta
            user1 = User(username='user1', email='user1@gmail.com', first_name='Jan', last_name='Nowak', position='Dyrektor', employment_date=datetime(2020, 1, 15))
            user2 = User(username='user2', email='user2@gmail.com', first_name='Joanna', last_name='Kowal', position='Sekretarka', employment_date=datetime(2021, 5, 20))
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
