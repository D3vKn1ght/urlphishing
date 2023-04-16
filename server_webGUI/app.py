#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')
from tienxuly import *

import json
from pandas import json_normalize

import pickle


from sklearn.preprocessing import StandardScaler
from keras.models import load_model


import json
from flask import Flask, render_template, url_for, request, redirect, abort



app = Flask(__name__)
app.secret_key = "doan"

@app.route("/")
def indexnew():
    return render_template("index.html")


from pusher import Pusher
pusher = Pusher(app_id="1496129", key="e0f057db90b68cb7a529", secret="95f3c0e4626c0df3d2e7", cluster="ap1")



import datetime


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3400, debug=True)