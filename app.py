from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    meals = Meal.query.order_by(Meal.date.desc()).all()
    total = db.session.query(db.func.sum(Meal.calories)).scalar() or 0
    return render_template('index.html', meals=meals, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_meal():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        if name and calories:
            meal = Meal(name=name, calories=int(calories))
            db.session.add(meal)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add.html')

# JSON API
@app.route('/meals', methods=['GET', 'POST'])
def meals_api():
    if request.method == 'POST':
        data = request.get_json()
        meal = Meal(name=data['name'], calories=data['calories'])
        db.session.add(meal)
        db.session.commit()
        return jsonify({'message': 'Meal added'}), 201
    meals = Meal.query.order_by(Meal.date.desc()).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'calories': m.calories,
        'date': m.date.isoformat()
    } for m in meals])

@app.route('/total_calories')
def total_calories():
    total = db.session.query(db.func.sum(Meal.calories)).scalar() or 0
    return jsonify({'total_calories': total})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
