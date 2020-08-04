import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for
from models import db, Store, Warehouse

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

# show all stores 
@app.route("/store/show", methods=['GET'])
def store_show():
    store_list = Store.select()
    return render_template('store_show.html', store_list = store_list)

@app.route("/warehouse")
def warehouse():
    all_stores = Store.select()
    return render_template('warehouse.html', all_stores=all_stores)

@app.route("/warehouse/new", methods=['POST'])
def warehouse_create():    
    store = request.form.get('store')
    w = Warehouse(location = request.form['location'], store=store)
    if w.save():
        print("Successfully saved")
        return redirect(url_for('warehouse'))
    else:
        print("Something went wrong... Try again!")
        return render_template('warehouse.html')

if __name__ == '__main__':
   app.run()