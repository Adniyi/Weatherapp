import requests
from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECERT_KEY'] = "ajdkni vkj jjiw vkw"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
with app.app_context():
    db.create_all()
# db.create_all(app)

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        new_city= request.form.get('field')
        if new_city:
            new_city_bj = City(name=new_city)
            db.session.add(new_city_bj)
            db.session.commit()

    cities = City.query.all()

    url =  "http://api.openweathermap.org/data/2.5/weather?q={}&unitsimperial&appid=2bfecacc177710f1552470fe66002fc4"
    
    weather_id = []   


    for city in cities:
        req = requests.get(url.format(city.name)).json()
        # print(req)

        weather={
            'city':city.name,
            'temp' : req['main']['temp'],
            'temp_min':req['main']['temp_min'],
            'temp_max':req['main']['temp_max'],
            'description':req['weather'][0]['description'],
            'icon':req['weather'][0]['icon'],
            'feels_like':req['main']['feels_like'],
            'pressure':req['main']['pressure'],
            'humidity':req['main']['humidity'],
        }

        weather_id.append(weather)
        print(weather_id.append(weather))
    # if request.method == "POST":




    return render_template("index.html",weather_id=weather_id)





if __name__ == "__main__":
    app.run(debug=True)

