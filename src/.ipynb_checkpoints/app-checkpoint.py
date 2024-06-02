from flask import Flask, render_template, url_for, request, redirect, flash
from ml import inference
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
import datetime
import psycopg2

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:danil@localhost:7777/request_data'
db = SQLAlchemy(app)

class Recoms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    #data = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Recom %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    test_sample = [
        [54.0, 0.382, 0.814, 3.0, -7.230, 1, 0.0406, 0.001100, 0.004010, 0.1010, 0.5690, 116.454, 251733.0, 4],
        [43.0, 0.92, 2, 0.0, 3, 1, 9.0506, 0.001100, 0.004010, 43, 9, 116.454, 251733.0, 2]]
    a = inference(test_sample)

    return render_template("about.html")


@app.route('/sing_in')
def sing():
    return render_template("sing_in.html")

@app.route('/input', methods=['GET', 'POST'])
def Input():
    form = LoginForm()
    return render_template('TEST.html', title='Input', form=form)


@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        recom=Recoms(title=title, text= text, intro=intro)
        try:
            db.session.add(recom)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавление произошла ошибка'
    else:
        return render_template("create_articl.html")


if __name__=="__main__":
    app.run(debug = True)
