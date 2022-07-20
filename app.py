from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import WilliamHill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prices(db.Model):
    runner_number = db.Column(db.Integer, nullable=False)
    horse_name = db.Column(db.String(100), nullable=False, primary_key=True)
    best_odds = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return '<Horse%r>' % self.horse_name

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', horses=horses)

if __name__ == '__main__':
    wh_data = WilliamHill.get_price_data()[0]
    horses = []
    for index, row in wh_data.iterrows():
        new_horse = Prices(horse_name=row['Name'], runner_number=row['Number'], best_odds=row['William Hill'])
        horses.append(new_horse)
        db.session.add(new_horse)
    app.run(debug=True)
