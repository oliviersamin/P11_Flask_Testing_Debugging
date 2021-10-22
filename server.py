import json
from flask import Flask, render_template, request, redirect, flash, url_for
import sys
import time as t


def is_competition_in_the_future(competition):
    date_format = "%Y-%m-%d %H:%M:%S"
    result = t.strptime(competition['date'], date_format)
    result = t.mktime(result)
    difference = result - t.time()
    if difference > 0:
        return True
    return False



def is_a_positive_integer(string_to_check: str) -> bool:
    """ check that the string_to_check is a positive integer and not another alphanumeric value
        param: input type = string
        param: output type = boolean
    """
    filter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    check = ""
    for character in string_to_check:
        if character not in filter:
            check = character
            break
    return check == ""


def check_competitions_number_of_places_is_positive_integer():
    filter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for index, compet in enumerate(competitions):
        for char in compet['numberOfPlaces']:
            if char not in filter:
                competitions[index]['numberOfPlaces'] = "ERROR: The number of places is not a positive integer"
                break


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
        global clubs, competitions
        clubs = loadClubs()
        competitions = loadCompetitions()
        club = [club for club in clubs if club['email'] == request.form['email']]
        if club:
            club = club[0]
            if is_a_positive_integer(club['points']):
                check_competitions_number_of_places_is_positive_integer()
                return render_template('welcome.html', club=club, competitions=competitions)
            else:
                flash('ERROR: The number of points for the club is not a positive integer')
                error = True
                return render_template('welcome.html', club=club, error_club_points=error)
        else:
            return render_template('welcome.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition and is_competition_in_the_future(foundCompetition):
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    elif foundClub and foundCompetition and (not is_competition_in_the_future(foundCompetition)):
        flash("ERROR: This competition is over")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    if is_a_positive_integer(request.form['places']):
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces'])-placesRequired)
        club['points'] = str(int(club['points']) - placesRequired)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('ERROR: The number of places booked is not a positive integer')
        return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
