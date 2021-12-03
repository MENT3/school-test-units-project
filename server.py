from flask import Flask, render_template, request, redirect, flash, url_for
from utils import find_from_slug, loadClubs, loadCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]

        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash('Désolé, cet email n\'a pas été trouvé', 'error')
        return render_template('index.html'), 404

@app.route('/book/<competition_slug>/<club_slug>')
def book(competition_slug, club_slug):
    competition = find_from_slug(competitions, competition_slug)
    club = find_from_slug(clubs, club_slug)

    if club and competition:
        return render_template('booking.html', club=club, competition=competition)
    else:
        flash("Something went wrong-please try again", 'error')
        return render_template('welcome.html',
            club=club, competitions=competitions), 404

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                    == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!', 'success')
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
