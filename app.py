from flask import Flask, render_template



app = Flask(__name__)


@app.route("/")
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/inventory')
def inventory_list():
    return render_template('inventory_page.html')
