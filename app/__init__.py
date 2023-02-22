from flask import Flask
import random
import string

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(32)) 

from app import models, routes

if(__name__ == "__main__"):
    app.run(debug=True)
