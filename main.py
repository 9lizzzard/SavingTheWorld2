from flask import Flask, render_template, request, url_for, redirect
import sqlite3 

app = Flask(__name__)

#create table here#
def create_db():
# create a connection to the SQLite3 database
  conn = sqlite3.connect('CCTV_database.db')

# create a cursor object
  cur = conn.cursor()

# create a table to store the face detection information
  cur.execute('''CREATE TABLE IF NOT EXISTS people
             (person_id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL, address TEXT NOT NULL, status TEXT NOT NULL)''')

  cur.execute('''INSERT INTO people (name, age, address, status) VALUES ("Jeffery", 32, "123 Rainbow Road", "innocent");''')

  cur.execute('''INSERT INTO people (name, age, address, status) VALUES ("Mr Richards", 32, "420 Childrens Street", "suspicious");''')

  cur.execute('''INSERT INTO people (name, age, address, status) VALUES ("Ronald Strudle", 42, "123 Ur Mom Street", "innocent");''')

  cur.execute('''CREATE TABLE IF NOT EXISTS images (img_id INTEGER PRIMARY KEY, img_data BLOB)''')
  
  with open('image.jpg', 'rb') as f:
    binary_data = f.read()

  cur.execute("INSERT INTO images (id, image_data) VALUES (?, ?)", (1, binary_data))

  rows = cur.execute('''SELECT a.person_id, a.name, a.age, a.address, b.img_data, a.status
                        FROM people as a, images as b;''')

# commit the changes to the database
  conn.commit()

  for row in rows:
    print(row)
# close the connection to the database
  conn.close()

#####################
# create_db()

@app.route('/', methods=["GET", "POST"])
def password_page():
  if request.method == "POST":
    password_input = request.form["password_input"]
    if password_input == "SavingTheWorld2":
      return redirect(url_for("homepage"))
  return render_template("password.html")

@app.route("/homepage")
def homepage():
  conn = sqlite3.connect('CCTV_database')
  cur = conn.execute("SELECT * FROM people")
  criminals = cur.fetchall()
  print(criminals)
  conn.close()
  
  return render_template("index.html", criminals=criminals)


@app.route("/upload")
def index():
    tm_url = "https://teachablemachine.withgoogle.com/models/xrnMPy-gX/"
    return render_template('machine.html', tm_url=tm_url)

if __name__ == '__main__':
    app.run()


app.run(host='0.0.0.0', port=81)
