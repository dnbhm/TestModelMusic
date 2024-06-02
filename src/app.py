import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from ml import inference

app = Flask(__name__)
conn = psycopg2.connect(database="postgres", user="postgres", password="danil", host="localhost", port="7777")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS TEST 
(id serial PRIMARY KEY, Popularity float NULL, danceability float NULL, energy float NULL, key float NULL, loudness float NULL,
 mode float NULL, speechiness float NULL, acousticness float NULL, instrumentalness float NULL, liveness float NULL, valence float NULL,
tempo float NULL, duration_in float NULL, time_signature float NULL);''')

conn.commit()

cur.close()
conn.close()

dict = {0: "диско",
        1: "металл",
        2: "регги",
        3: "блюз",
        4: "рок",
        5: "классика",
        6: "джаз",
        7: "хип-хоп",
        8: "кантри",
        9: "поп"}

class musclass():
    def __init__(self, num, d=0):
        self.number=num
        self.data=d
    def tr(data):
        for i in range(14):
            if i in (0,12,13):
                data[i]*=10


    def str(num):
        return 'Жанр музыки ' + dict[num]

@app.route('/')
def index():

    conn = psycopg2.connect(database="postgres", user="postgres",password="danil", host="localhost", port="7777")

    cur = conn.cursor()

    cur.execute('''SELECT * FROM TEST''')

    data = cur.fetchall()
    data = musclass.tr(data)
    cur.close()
    conn.close()
    return render_template('about.html', data=data)

@app.route('/begin')
def begin():
    return render_template('create_articl.html')

@app.route('/chose')
def chose():
    conn = psycopg2.connect(database="postgres", user="postgres",password="danil", host="localhost", port="7777")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM TEST ORDER BY id desc LIMIT 1''')
    data = cur.fetchall()
    n = [0]*14
    for row in data:
        for i in range(1,15):
            n[i-1] = row[i]
    a = inference([n])
    return render_template('chose.html', data=data, context = musclass.str(a[0][0]))


@app.route('/create', methods=['POST'])
def create():
    conn = psycopg2.connect(database="postgres", user="postgres",password="danil", host="localhost", port="7777")
    cur = conn.cursor()


    Popularity = request.form['Popularity']
    danceability = request.form['danceability']
    energy = request.form['energy']
    key = request.form['key']
    loudness = request.form['loudness']
    mode = request.form['mode']
    speechiness = request.form['speechiness']
    acousticness = request.form['acousticness']
    instrumentalness = request.form['instrumentalness']
    liveness = request.form['liveness']
    valence = request.form['valence']
    tempo = request.form['tempo']
    duration_in = request.form['duration_in']
    time_signature = request.form['time_signature']


    cur.execute(
        '''INSERT INTO TEST  
        (Popularity , danceability , energy , key , loudness ,
 mode , speechiness , acousticness , instrumentalness , liveness , valence ,
tempo , duration_in , time_signature ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)''',
        (Popularity, danceability, energy, key, loudness,
         mode, speechiness, acousticness, instrumentalness, liveness, valence,
         tempo, duration_in, time_signature))

    conn.commit()

    cur.close()
    conn.close()
    return redirect(url_for('chose'))


if __name__ == '__main__':
    app.run(debug=True)