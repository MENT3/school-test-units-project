from flask import Flask, render_template, request, redirect, flash, url_for, g
from utils import find_from_slug, load_clubs, load_competitions, reset_jsons, update_club_from_slug, update_competition_from_slug

app = Flask(__name__)
app.secret_key = 'something_special'

@app.before_request
def before_all():
    g.competitions = load_competitions()
    g.clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in g.clubs if club['email'] == request.form['email']][0]

        return render_template('welcome.html', club=club, competitions=g.competitions)
    except IndexError:
        flash('Désolé, cet email n\'a pas été trouvé', 'error')
        return render_template('index.html'), 404

@app.route('/book/<competition_slug>/<club_slug>')
def book(competition_slug, club_slug):
    competition = find_from_slug(g.competitions, competition_slug)
    club = find_from_slug(g.clubs, club_slug)

    if club and competition:
        return render_template('booking.html', club=club, competition=competition)
    else:
        flash("Something went wrong-please try again", 'error')
        return render_template('welcome.html',
            club=club, competitions=g.competitions), 404

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club_slug, competition_slug, requested_places = request.form.values()

    try:
        competition = find_from_slug(g.competitions, competition_slug)
        club = find_from_slug(g.clubs, club_slug)

        if int(requested_places) > 12: raise
        elif int(requested_places) > int(competition['numberOfPlaces']): raise
        elif (int(requested_places) * 5) > int(club['points']): raise

        update_club_from_slug(club_slug, {
            **club,
            'points': str(int(club['points']) - int(requested_places) * 5)
        })

        update_competition_from_slug(competition_slug, {
            **competition,
            'numberOfPlaces': str(int(competition['numberOfPlaces']) - int(requested_places))
        })

        # reload json data
        club = find_from_slug(g.clubs, club_slug)
        competitions = load_competitions()

        flash('Great-booking complete!', 'success')
        return render_template('welcome.html', club=club, competitions=competitions)
    except:
        flash('Impossible de réserver', 'error')
        return render_template('booking.html', club=club, competition=competition), 500

@app.route('/reset-data')
def reset_data():
    reset_jsons()
    flash('Data correctement reset', 'success')
    return redirect(url_for('index'))

# TODO: Reset JSON values
# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
