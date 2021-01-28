
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='../Frontend/templates', static_folder='../Frontend/static')
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False , default=False)
    seeking_description = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    showsV = db.relationship('showss', backref='venue', lazy=True)
    upcoming_shows_count = db.Column(db.Integer, nullable=True)
    past_shows_count = db.Column(db.Integer, nullable=True)
    def __repr__(self):
      return f'<Venue ID:{self.id}, name:{self.name}, Genres:{self.genres}, address:{self.address}, city:{self.city}, state:{self.state},  phone:{self.phone}, website:{self.website}, facebook:{self.facebook}, seeking_talent:{self.seeking_talent}, seeking_description:{self.seeking_description}, image:{self.image_link}, ShowsV:{self.showsV}, upcoming_shows_count{self.upcoming_shows_count}>, past_shows_count{self.past_shows_count}>'

    def __init__(self, name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link): 
        self.name = name
        self.genres = genres
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.image_link = image_link
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    showsA = db.relationship('showss', backref='artist', lazy=True)
    upcoming_shows_count = db.Column(db.Integer, nullable=True)
    past_shows_count = db.Column(db.Integer, nullable=True)

    def __repr__(self):
      return f'<Artist ID:{self.id}, name:{self.name}, Genres:{self.genres}, city:{self.city}, state:{self.state},  phone:{self.phone}, website:{self.website}, facebook:{self.facebook_link}, seeking_talent:{self.seeking_venue}, seeking_description:{self.seeking_description}, image:{self.image_link}, ShowsV:{self.showsA}, upcoming_shows_count{self.upcoming_shows_count}>, past_shows_count{self.past_shows_count}>'

    def __init__(self, name, genres, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link

      # TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class showss(db.Model):
    __tablename__ = "showss"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable = False)
    starttime = db.Column(db.DateTime, nullable=True, default=True)

    def __repr__(self):
      return f'<Shows ID:{self.id}, Arist ID:{self.artist_id}, Venue ID:{self.venue_id}>'

       
db.create_all()

