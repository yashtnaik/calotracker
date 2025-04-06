from flask import Flask, request, jsonify
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'date': self.date.isoformat()
        }

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    name = data.get('name')
    calories = data.get('calories')
    if not name or not calories:
        return jsonify({'error': 'Missing name or calories'}), 400
    meal = Meal(name=name, calories=calories)
    db.session.add(meal)
    db.session.commit()
    return jsonify(meal.to_dict()), 201

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.order_by(Meal.date.desc()).all()
    return jsonify([meal.to_dict() for meal in meals])

@app.route('/total_calories', methods=['GET'])
def get_total_calories():
    total = db.session.query(db.func.sum(Meal.calories)).scalar() or 0
    return jsonify({'total_calories': total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
