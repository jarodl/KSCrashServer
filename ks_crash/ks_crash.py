import os

from flask import Flask
from flask import render_template, redirect, url_for, request

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
