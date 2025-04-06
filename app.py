from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

DAILY_GOAL = 2000

PREDEFINED_MEALS = {
    "Dal & Rice": 300,
    "Chapati & Sabzi": 250,
    "Idli & Sambar": 200,
    "Paneer Curry": 350,
    "Chicken Biryani": 600,
    "Paratha": 300,
    "Masala Dosa": 400,
    "Upma": 180,
    "Poha": 220,
    "Aloo Puri": 500
    "Apple": 56,
    "Avocado Pear": 190,
    "Banana": 95,
    "Chickoo": 94,
    "Cherries": 70,
    "Dates": 281,
    "Grapes Black": 45,
    "Guava": 66,
    "Kiwi Fruit": 45,
    "Lychies": 61,
    "Mangoes": 70,
    "Orange": 53,
    "Papaya": 32,
    "Peach": 50,
    "Pears": 51,
    "Pineapple": 46,
    "Plums": 56,
    "Strawberries": 77,
    "Watermelon": 26,
    "Pomegranate": 77,
    "Broccoli": 25,
    "Brinjal": 24,
    "Cabbage": 45,
    "Carrot": 48,
    "Cauliflower": 30,
    "Fenugreek (Methi)": 49,
    "French beans": 26,
    "Lettuce": 21,
    "Mushroom": 18,
    "Onion": 50,
    "Peas": 93,
    "Potato": 97,
    "Tomato": 21,
    "Bajra": 360,
    "Maize flour": 355,
    "Rice": 325,
    "Wheat flour": 341,
    "Chapatti (1 medium)": 119,
    "White Bread (1 slice)": 60,
    "Paratha (no filling)": 280,
    "Butter": 750,
    "Buttermilk": 19,
    "Cheese": 315,
    "Cream": 210,
    "Ghee": 910,
    "Milk (Buffalo)": 115,
    "Milk (Cow)": 100,
    "Milk (Skimmed)": 45,
    "Sugar (1 tbsp)": 48,
    "Honey (1 tbsp)": 90,
    "Coconut Water (100 ml)": 25,
    "Coffee": 40,
    "Tea": 30
}

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form.get('quantity', 1))
        calories = PREDEFINED_MEALS.get(name, 0) * quantity
        new_meal = Meal(name=name, calories=calories)
        db.session.add(new_meal)
        db.session.commit()
        return redirect(url_for('index'))

    query = Meal.query.order_by(Meal.date.desc())
    if start_date:
        query = query.filter(Meal.date >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Meal.date <= datetime.strptime(end_date, "%Y-%m-%d"))

    all_meals = query.all()
    today = datetime.utcnow().date()
    total_today = sum(m.calories for m in all_meals if m.date.date() == today)

    # For bar chart
    meal_summary = defaultdict(int)
    for meal in all_meals:
        meal_summary[meal.name] += meal.calories

    chart_labels = list(meal_summary.keys())
    chart_data = list(meal_summary.values())

    return render_template('index.html',
                           meals=PREDEFINED_MEALS,
                           all_meals=all_meals,
                           total_today=total_today,
                           daily_goal=DAILY_GOAL,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           start_date=start_date,
                           end_date=end_date)

@app.route('/edit/<int:id>', methods=['POST'])
def edit_meal(id):
    meal = Meal.query.get_or_404(id)
    meal.name = request.form['name']
    meal.calories = PREDEFINED_MEALS.get(meal.name, 0) * int(request.form.get('quantity', 1))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

