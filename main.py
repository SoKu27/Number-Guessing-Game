from flask import Flask, render_template, session, request
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def main():
  return render_template("index.html")



@app.route('/play', methods=['GET', 'POST'])
def index():

  if 'numtoguess' not in session:
    session['numtoguess'] = random.randint(1,100)
    session['attempts'] = 0
    session['feedback'] = None
    session['lowchange'] = 0
    session['highchange'] = 0


  if request.method == 'POST':
    try:
      guess = int(request.form['guess'])
    except ValueError:
      error = "Please enter a number"
      return render_template('index.html', error=error)
    if guess < 1 or guess > 100:
      notinrange = "Your number was not between 1 and 100"
      return render_template('index.html', notinrange=notinrange)
    session['attempts'] += 1
    numtoguess = session['numtoguess']
    if guess < numtoguess:
      session['feedback'] = "your guess is too LOW."
      session['lowchange'] += 1
      if session['lowchange'] % 2 == 0:
        session['feedback'] = "your guess is still too LOW."
      return render_template('game.html', feedback=session['feedback'])
    elif guess > numtoguess:
      session['feedback'] = "your guess is too HIGH"
      session['highchange'] += 1
      if session['highchange'] % 2 == 0:
        session['feedback'] = "your guess is still too HIGH."
      return render_template('game.html', feedback=session['feedback'])
    else:
      session['feedback'] = f'you guessed the number! It took you {session["attempts"]} attempts. Enter a number to play again' 
      session.pop('numtoguess', None)
      session.pop('attempts', None) 
      feedback = session['feedback']
      session.pop('feedback', None) 
      return render_template('game.html', feedback=feedback)
  return render_template('index.html')
@app.route("/return", methods = ["GET", "POST"])    
def goBack():
    return render_template("index.html")

if __name__== "__main__":
  app.run(debug=True)