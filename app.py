from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Predefined Indian meals and their calories
PREDEFINED_MEALS = {
    "Roti": 100,
    "Rice": 200,
    "Dal": 150,
    "Paneer": 250,
    "Chicken Curry": 300,
    "Fish Curry": 280,
    "Chole": 220,
    "Rajma": 240,
    "Dosa": 180,
    "Idli": 70,
    "Upma": 150,
    "Sambar": 120,
    "Poha": 160,
    "Paratha": 250
}

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def index():
    meals = Meal.query.order_by(Meal.date.desc()).all()
    total = sum(meal.calories for meal in meals)

    today = datetime.utcnow().date()
    daily_data = defaultdict(int)

    for meal in meals:
        day = meal.date.date()
        if (today - day).days < 7:
            daily_data[day] += meal.calories

    labels = []
    values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime("%a"))
        values.append(daily_data.get(day, 0))

    return render_template("index.html", meals=meals, total=total, labels=labels, values=values)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form.get('quantity', 1))
        calories = PREDEFINED_MEALS.get(name, 0) * quantity
        new_meal = Meal(name=name, calories=calories)
        db.session.add(new_meal)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', meals=PREDEFINED_MEALS)

@app.route('/edit/<int:meal_id>', methods=['GET', 'POST'])
def edit(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if request.method == 'POST':
        meal.name = request.form['name']
        quantity = int(request.form.get('quantity', 1))
        meal.calories = PREDEFINED_MEALS.get(meal.name, 0) * quantity
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', meal=meal, meals=PREDEFINED_MEALS)

@app.route('/delete/<int:meal_id>')
def delete(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

