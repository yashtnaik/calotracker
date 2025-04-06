from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

DAILY_GOAL = 2000

PREDEFINED_MEALS = {
    'Roti (1)': 100,
    'Rice (1 cup)': 200,
    'Dal (1 cup)': 150,
    'Paneer Curry (1 cup)': 300,
    'Chicken Curry (1 cup)': 350,
    'Samosa': 250,
    'Dosa': 200,
    'Idli (2)': 120,
    'Poha': 180,
    'Upma': 170,
    'Banana': 105,
    'Apple': 95
}

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form.get('quantity', 1))
        calories = PREDEFINED_MEALS.get(name, 0) * quantity
        meal = Meal(name=name, calories=calories)
        db.session.add(meal)
        db.session.commit()
        return redirect(url_for('index'))

    all_meals = Meal.query.order_by(Meal.date.desc()).all()
    meals_today = [meal for meal in all_meals if meal.date.date() == date.today()]
    total_today = sum(m.calories for m in meals_today)

    return render_template('index.html',
        meals=PREDEFINED_MEALS,
        all_meals=all_meals,
        total_today=total_today,
        daily_goal=DAILY_GOAL,
        chart_labels=[m.name for m in all_meals],
        chart_data=[m.calories for m in all_meals]
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

