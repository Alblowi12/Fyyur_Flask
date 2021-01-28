#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from models import app, db, venue, artist, showss 
from flask import jsonify
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import babel
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
import sys  
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
#-----------
app.config.from_object('config')
#----------------------------------------------------------------------------------------
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('/pages/home.html')


#  Define Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = venue.query.all()
  return render_template('/pages/venues.html', venue=data)


#  Search Venues
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    venues = venue.query.filter(venue.name.ilike('%{}%'.format(search_term))).all()
      
    data = []
    for vn in venues:
          arr= {}
          arr['id'] = vn.id
          arr['name'] = vn.name
          data.append(arr)

    response = {}
    response['data'] = data

    return render_template('pages/search_venues.html',
                             results=response,
                             search_term=request.form.get('search_term', ''))

#  Shows Venues
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue1 = venue.query.get(venue_id)

  if not venue1: 
    return render_template('errors/404.html')

  upcoming_shows_query = db.session.query(showss).join(artist).filter(showss.venue_id==venue_id).filter(showss.starttime>datetime.now()).all()
  upcoming_shows = []

  past_shows_query = db.session.query(showss).join(artist).filter(showss.venue_id==venue_id).filter(showss.starttime<datetime.now()).all()
  past_shows = []

  for show in past_shows_query:
    past_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.starttime.strftime('%Y-%m-%d %H:%M:%S')
    })

  for show in upcoming_shows_query:
    upcoming_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.starttime.strftime("%Y-%m-%d %H:%M:%S")    
    })

  data = {
    "id": venue1.id,
    "name": venue1.name,
    "genres": venue1.genres,
    "address": venue1.address,
    "city": venue1.city,
    "state": venue1.state,
    "phone": venue1.phone,
    "website": venue1.website,
    "facebook_link": venue1.facebook_link,
    "seeking_talent": venue1.seeking_talent,
    "seeking_description": venue1.seeking_description,
    "image_link": venue1.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    name = request.form['name']
    gen = ','.join(request.form.getlist('genres'))   
    add = request.form['address']    
    cit = request.form['city']
    st = request.form['state']
    ph = request.form['phone'] 
    sk = request.form['seeking_description']
    fcb = request.form['facebook_link']
    web = request.form['website']
    img = request.form['image_link']
    try:
        newven = venue(name=name, genres=gen, address=add, city=cit, state=st, phone=ph, website=web, facebook_link=fcb, seeking_talent=True, seeking_description=sk, image_link=img)
        db.session.add(newven)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
             flash('Venue ' + request.form['name'] + ' Is Not Added')
        else:
              flash('Venue ' + request.form['name'] + ' is successfully Added!')
    return render_template('pages/home.html')

#  Delete Venue
#  -------------------------------------------------------------------------
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
       venue.query.filter_by(id=venue_id).delete()
       db.session.commit()
    except:
       error = True
       db.session.rollback()
       print(sys.exc_info())
    finally:
        db.session.close()
        if error:
             flash('Error: Operation Failure')
        else:
              flash('Venue ' + venue.name + ' is successfully Deleted!')
    return jsonify({ 'success': True })
    

    
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=artist.query.all()
  return render_template('pages/artists.html', artists = data ) 

#  DELETE Artists
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    error = False
    try:
       artist.query.filter_by(id=artist_id).delete()
       db.session.commit()
    except:
       error = True
       db.session.rollback()
       print(sys.exc_info())
    finally:
        db.session.close()
        if error:
             flash('Error: Operation Failure')
        else:
              flash('artist ' + artist.name + ' is successfully Deleted!')
    return jsonify({ 'success': True })
    

    
#  Search Artists
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    artists = artist.query.filter(artist.name.ilike('%{}%'.format(search_term))).all()
      
    data = []
    for ar in artists:
          arr= {}
          arr['id'] = ar.id
          arr['name'] = ar.name
          data.append(arr)

    response = {}
    response['data'] = data

    return render_template('pages/search_artists.html',
                             results=response,
                             search_term=request.form.get('search_term', ''))

    
#  Show Artists
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)

    

#  Edit Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    edtart = artist.query.get(artist_id)

    return render_template('forms/edit_artist.html', form=form, artist=edtart)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
     error = False
     edtart = artist.query.filter_by(id=artist_id).first()
     name = request.form['name']
     gen = ','.join(request.form.getlist('genres'))
     cit = request.form['city']
     st = request.form['state']
     ph = request.form['phone'] 
     fcb = request.form['facebook_link']
     img = request.form['image_link']
     sk =  request.form['seeking_description']
     sn =  request.form['seeking_talent']
     web = request.form['website']
     try:
        edtart.name = name
        edtart.genres = gen
        edtart.city = cit
        edtart.state = st
        edtart.phone = ph 
        edtart.facebook_link = fcb
        edtart.image_link = img
        edtart.seeking_description = sk
        edtart.seeking_talent = sn
        edtart.website = web
        db.session.commit()
     except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
     finally:
        db.session.close()
        if error:
            flash('Failure Updated')
            return redirect(url_for('server_error'))
        else:
            flash(' successfully Updated!')
            return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  edtven = venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=edtven)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
     error = False
     edtven = venue.query.filter_by(id=venue_id).first()
     name = request.form['name']
     gen = ','.join(request.form.getlist('genres'))
     cit = request.form['city']
     st = request.form['state']
     add = request.form['address']
     ph = request.form['phone'] 
     fcb = request.form['facebook_link']
     web = request.form['website']
     img =  request.form['image_link']
     sk = request.form['seeking_description']
     try:
        edtven.name = name
        edtven.genres = gen
        edtven.city = cit
        edtven.state = st
        edtven.address = add
        edtven.phone = ph 
        edtven.facebook_link = fcb
        edtven.website = web
        edtven.image_link = img
        edtven.seeking_description = sk
        db.session.commit()
     except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
     finally:
        db.session.close()
        if error:
            flash('Failure Updated')
            return redirect(url_for('server_error'))
        else:
            flash(' successfully Updated!')
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    name = request.form['name']
    gen = ','.join(request.form.getlist('genres'))
    cit = request.form['city']
    st = request.form['state']
    ph = request.form['phone'] 
    fcb = request.form['facebook_link']
    web = request.form['website']
    img = request.form['image_link']
    sk = request.form['seeking_description']
    sn = request.form['seeking_talent']
    if  sn =='y':
        sn = 1
    else:
      
        sk = 0
      
    try:
        newart = artist(name=name, genres=gen, city=cit, state=st, phone=ph, website=web, facebook_link=fcb, seeking_venue=sn, seeking_description=sk, image_link=img)
        db.session.add(newart)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
             flash('Artist ' + request.form['name'] + ' Is Not Added')
        else:
              flash('Artist ' + request.form['name'] + ' is successfully Added!')
        return render_template('pages/home.html')
        
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
 
  shows = db.session.query(showss).join(artist).join(venue).all()

  data = []
  for sh in shows: 
    data.append({
      "venue_id": sh.venue_id,
      "venue_name": sh.venue.name,
      "artist_id": sh.artist_id,
      "artist_name": sh.artist.name, 
      "artist_image_link": sh.artist.image_link,
      "starttime": sh.starttime.strftime('%Y-%m-%d %H:%M:%S')
    })


  return render_template('pages/shows.html', shows = data )

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    aid = request.form['artist_id']
    vid = request.form['venue_id']
    st = request.form['starttime']
    error = False
    try: 
        
        sh = showss(artist_id=aid, venue_id=vid, starttime=st)
        db.session.add(sh)
        db.session.commit()
    except: 
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: 
        db.session.close()
        if error: 
            flash(aid + ' Venue ID : ' + vid + ' Time ' + st)
        if not error: 
            flash('Show was successfully listed')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
