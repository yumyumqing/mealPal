#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, send_from_directory
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://yd2369:Keineanung20@104.196.18.7/w4111"

engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  
  cursor.close()
  context = dict(data = names)
  return render_template("index.html", **context)

@app.route('/profile')
def profile():
  return render_template("another.html", **context)


@app.route('/another')
def another():
  cursor = g.conn.execute("SELECT * FROM users U WHERE U.uid='10001' ")
  information = []
  for result in cursor:
    information.append(result)  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = information)
  return render_template("another.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = []
  name.append(request.form['name'])
  g.conn.execute('INSERT INTO test(name) VALUES %s', name)
  return redirect('/')

@app.route('/add_eaten', methods=['POST'])
def add_eaten():
  rid = []
  score = []
  review = []
  rid.append(request.form['rid'])
  score.append(request.form['score'])
  review.append(request.form['review'])
  g.conn.execute('INSERT INTO test(name) VALUES %s', rid)
  return redirect('/')

@app.route('/add_marked', methods=['POST'])
def add_marked():
  rid = []
  rid.append(request.form['rid'])
  g.conn.execute('INSERT INTO test(name) VALUES %s', rid)
  return redirect('/')


@app.route('/food_profile', methods=['POST'])
def food_profile():
  error = None
  context = dict(error = error)
  rid = []
  rname = []
  cursor1 = g.conn.execute("SELECT R.rname FROM Restaurants R")
  for result in cursor1:
    rname.append(result)
  cursor1.close()
  cursor2 = g.conn.execute("SELECT R.rid FROM Restaurants R")
  for result in cursor2:
    rid.append(result)
  cursor2.close()
  context = dict(id = rid, name = rname)
  print(context)
  return render_template("food_profile.html", result=context)

@app.route('/login',methods=['POST'])
def login():
    error = None
    context = dict(error = error)
    name =  request.form['name']
    global myUid
    myUid = name
    cursor = g.conn.execute("SELECT * FROM users U WHERE U.uid = %s", name)
    information = []
    for result in cursor:
        for column in result:
            information.append(column)
    cursor.close()
    context["data"] = information
    
    cursor = g.conn.execute("SELECT R.rid, R.rname, R.cuisine, R.link, R.lid FROM restaurants R, ate A, users U WHERE R.rid = A.rid AND A.uid = U.uid AND U.name = %s", name)
    information = []
    for result in cursor:
        for column in result:
            information.append(column)
    cursor.close()
    context["eaten"] = information

    cursor = g.conn.execute("SELECT R.rid, R.rname, R.cuisine, R.link, R.lid FROM restaurants R, marked M, users U WHERE R.rid = M.rid AND M.uid = U.uid AND U.name = %s", name)
    information = []
    for result in cursor:
        for column in result:
            information.append(column)
    cursor.close()
    context["marked"] = information
    return render_template("profile.html", **context)

# Random suggestion swiping page
@app.route('/swipe', methods=['POST'])
def swipe():
    isLike = request.form['submit']
    if (isLike == 'Yes'):
        print('like')
        liker_uid = g.conn.execute("SELECT COUNT(*) FROM interest I WHERE I.liker_uid=%s AND I.likee_uid=%s", myUid, otherUsers[0][0])
        likeNotExists = (liker_uid.fetchone()[0] == 0)
        if likeNotExists:
            g.conn.execute("INSERT INTO interest(liker_uid,likee_uid) VALUES (%s,%s)", myUid, otherUsers[0][0])

#    isback = request.form['submit']
#    if (isback == 'Back to swipe'):
#        return redirect(url_for('swipe'))
    randomNum = random.randint(1,9) + 10000
    cursor = g.conn.execute("SELECT * FROM Users U WHERE U.uid=%s", str(randomNum))
    global otherUsers
    otherUsers = []
    otherUsersLocation = []
    otherUsersDisplay = []
    global rests1
    rests1 = []
    rid1 = []
    rests2 = []
    rid2 = []
    
    for result in cursor:
      otherUsers.append(result)  
    cursor.close()
    
    cursorLoc = g.conn.execute("SELECT L.street_num, L.street, L.city, L.zip FROM locations L WHERE L.lid=%s", otherUsers[0][4])
    for result in cursorLoc:
        otherUsersLocation.append(result)
    cursorLoc.close()
    otherUsersDisplay = [otherUsers[0][1], otherUsers[0][2], otherUsers[0][3], otherUsersLocation[0][0], otherUsersLocation[0][1], otherUsersLocation[0][2], otherUsersLocation[0][3]]
    
    cursor2 = g.conn.execute("SELECT R.rname, A.score, A.review \
                             FROM restaurants R, ate A \
                             WHERE R.rid=A.rid AND A.uid=%s",\
                             str(randomNum))
    for result in cursor2:
        rests1.append(result)
    cursor2.close()
    
    cursor2id = g.conn.execute("SELECT R.rid \
                                FROM restaurants R, ate A \
                                WHERE R.rid=A.rid AND A.uid=%s",\
                                str(randomNum))
    for result in cursor2id:
        rid1.append(result)
    cursor2id.close()

    cursor3 = g.conn.execute("SELECT R.rname \
                             FROM restaurants R, marked M \
                             WHERE R.rid=M.rid AND M.uid=%s",\
                             str(randomNum))
    for result in cursor3:
        rests2.append(result)
    cursor3.close()
    global context
    context = dict(data = otherUsersDisplay, rests1=rests1, rid1=rid1, rests2=rests2)
    return render_template("swipe.html", **context)

# get restaurant profile page
@app.route('/restaurant', methods=['POST'])
def restaurant():
    isEatenOrMarked = request.form['submit']
    if (isEatenOrMarked == "Check Eaten Restaurant"):
        cursor = g.conn.execute("SELECT * FROM restaurants R WHERE R.rname = %s", rests1[0])
    print(rests1[0])
    if (isEatenOrMarked == "Check Marked Restaurant"):
        cursor = g.conn.execute("SELECT * FROM restaurants R WHERE R.rname = %s", rests2[0])
    information = []
    for result in cursor:
        for column in result:
            information.append(column)
    cursor.close()
    context = dict(data = information)
    return render_template("restaurant.html", **context)

def redirect_url(default='index'):
    return request.referrer 
  

@app.route('/back', methods=['POST'])
def back():
    
    return render_template("swipe.html", **context)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
