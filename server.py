from flask import Flask, abort, render_template, request, redirect, flash, url_for, g, session
from utils import find_by, load_clubs, load_competitions, reset_jsons, update_club_from_slug, update_competition_from_slug

app = Flask(__name__)
app.secret_key = 'something_special'

@app.before_request
def before_all():
    public_endpoints = ['index', 'public_dashboard', 'reset_data']
    g.competitions = load_competitions()
    g.clubs = load_clubs()

    if 'club_slug' in session:
        if request.endpoint == 'book':
            club_slug = request.view_args.get('club_slug')
            if session['club_slug'] != club_slug:
                abort(403)
    else:
        if request.endpoint == 'show_summary' and 'email' in request.form:
            return
        elif request.endpoint not in public_endpoints:
            abort(403)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = find_by('email', request.form['email'], g.clubs)

    if club:
        session['club_slug'] = club['slug']
        return render_template('welcome.html', club=club, competitions=g.competitions)
    else:
        flash('Désolé, cet email n\'a pas été trouvé', 'error')
        return render_template('index.html'), 404

@app.route('/book/<competition_slug>/<club_slug>')
def book(competition_slug, club_slug):
    competition = find_by('slug', competition_slug, g.competitions)
    club = find_by('slug', club_slug, g.clubs)

    if club and competition:
        return render_template('booking.html', club=club, competition=competition)
    else:
        flash("Something went wrong-please try again", 'error')
        return render_template('welcome.html',
            club=club, competitions=g.competitions), 404

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    club_slug, competition_slug, requested_places = request.form.values()

    try:
        competition = find_by('slug', competition_slug, g.competitions)
        club = find_by('slug', club_slug, g.clubs)

        if int(requested_places) > 12: raise ValueError
        elif int(requested_places) > int(competition['numberOfPlaces']): raise ValueError
        elif (int(requested_places) * 3) > int(club['points']): raise ValueError

        update_club_from_slug(club_slug, {
            **club,
            'points': str(int(club['points']) - int(requested_places) * 3)
        })

        update_competition_from_slug(competition_slug, {
            **competition,
            'numberOfPlaces': str(int(competition['numberOfPlaces']) - int(requested_places))
        })

        # reload json data
        clubs = load_clubs()
        club = find_by('slug', club_slug, clubs)
        competitions = load_competitions()

        flash('Great-booking complete!', 'success')
        return render_template('welcome.html', club=club, competitions=competitions)
    except:
        flash('Impossible de réserver', 'error')
        return render_template('booking.html', club=club, competition=competition), 500

@app.route('/dashboard')
def public_dashboard():
    return render_template('dashboard.html', clubs=g.clubs, competitions=g.competitions)

@app.route('/reset-data')
def reset_data():
    reset_jsons()
    flash('Data correctement reset', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
