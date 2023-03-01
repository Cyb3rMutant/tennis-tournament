from flask import Flask
import random
import string
print("hello")

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(32)) 
print("hello2")

from routes import *

if(__name__ == "__main__"):
    print("hello3")
    app.run(debug=True)
