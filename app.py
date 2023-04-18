from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float 
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

app = Flask(__name__)
app.debug = True
# basedir = os.path.abspath.os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planet.db'
app.config['JWT_SECRET_KEY'] = 'somesupersecret'
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '0131a812f47382'
app.config['MAIL_PASSWORD'] = 'a6ec88b97163fe'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

# Flask seed script 
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created')
    
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped')
    
@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=1516,
                     radius=29373.0,
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                     planet_type='Class K',
                     home_star='Sol',
                     mass=4.867e24,
                     radius=3760,
                     distance=67.24e6)
    
    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
                     radius=3959,
                     distance=92.96e6)    
    
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    
    test_user = User(first_name='Williams',
                     last_name='Merschel',
                     email='test@email.com',
                     password='Pass0r4d')
    
    db.session.add(test_user)
    db.session.commit()
    print('Database Seeded!')
    

@app.route('/')
def hello_world():
    return 'hello World'    

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User successfully added'), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='login successful', access_token=access_token)
    else:
        return jsonify(message='Bad Email or Password!'), 401

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message('your planetry api password is ' + user.password,
                      sender='admin@planetary.api.com',
                      recipients=[email])
        mail.send(msg)
        return jsonify(message='Password sent to ' + email)
    else:
        return jsonify(message='That email does not exist')
    
@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message='that planet does not exist'), 404
        

@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify('there is already a planet by this name'), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])
        
        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)
        db.session.add(new_planet)               
        db.session.commit()
        return jsonify(message='You added a new Planet'), 201
        

@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message='You updated a planet'), 202
    else:
        return jsonify(message='That planet does not exist'), 404
  
  
@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message='Planet has been deleted'), 202
    else:
        return jsonify(message='There is no such planet in the database'), 404
  
# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    
class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)