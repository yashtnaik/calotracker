from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'date': self.date.isoformat()
        }

# Predefined Indian meals
INDIAN_MEALS = {
    'Roti': 100,
    'Rice (1 cup)': 200,
    'Dal (1 cup)': 180,
    'Paneer Curry': 250,
    'Chicken Curry': 300,
    'Samosa': 130,
    'Chole Bhature': 400,
    'Idli (2 pcs)': 150,
    'Dosa': 180,
    'Biryani (1 plate)': 450
}

# Routes

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def index():
    meals = Meal.query.order_by(Meal.date.desc()).all()
    total_calories = sum(meal.calories for meal in meals)
    return render_template('index.html', meals=meals, total=total_calories)

@app.route('/add', methods=['GET', 'POST'])
def add_meal():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        calories = INDIAN_MEALS.get(name, 0) * quantity
        if name and calories:
            meal = Meal(name=name, calories=calories)
            db.session.add(meal)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add.html', meals=INDIAN_MEALS)

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.serialize() for meal in meals])

@app.route('/meals', methods=['POST'])
def add_meal_api():
    data = request.json
    name = data.get('name')
    calories = data.get('calories')
    if not name or not calories:
        return jsonify({'error': 'Missing data'}), 400
    meal = Meal(name=name, calories=calories)
    db.session.add(meal)
    db.session.commit()
    return jsonify(meal.serialize()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
