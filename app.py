import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for
from models import db, Store

app = Flask(__name__)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store")
def store():
    return render_template('store.html')

@app.route("/store/new", methods=['POST'])
def store_create():    
    name = request.form.get('store_name')
    store = Store(name=name)
    if store.save():
        print("Successfully saved")
        return redirect(url_for('store'))
    else:
        print("Something went wrong... Try again!")
        return render_template('store.html')



if __name__ == '__main__':
   app.run()