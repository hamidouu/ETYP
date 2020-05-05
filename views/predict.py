from flask import Flask, render_template, request, jsonify, json, Blueprint, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  
from wtforms import SelectField, Form
from flask_wtf import FlaskForm
from flask_login import current_user
from views.forms import Form
from models import Region, Municipality, Emplacement
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import joblib


model=pickle.load(open('model.pkl','rb'))


sc_X = joblib.load("data_transformer.joblib") 
 
pred = Blueprint('pred', __name__, template_folder='templates')
def transf(l):
    a = [12, 19, 20, 29, 34, 44, 48,  0,  1, 13, 15, 30, 31, 33, 46, 50,  8,
        4,  6, 16, 21, 22, 23, 55,  2, 24,  5, 45, 52,  9, 35, 38, 47,  7,
       54, 36, 37, 39, 40, 42, 51, 26, 27, 28, 43, 56, 18, 25, 32, 17, 49,
        3, 14, 10, 11, 41, 53]
    l0 = [0]*59
    l0[-1], l0[-2] = l[-1], l[-2]
    l0[a[l[0]-1]-1] = 1
    return l0

         
@pred.route('/predict', methods=['GET', 'POST'])
def predict():
    if not current_user.is_authenticated:
        #print(request.path)
        return redirect(url_for('auth.login', messages=request.path))

        #return redirect(url_for('auth.login'))
    form = Form()
    form.region.choices = [(region.id, region.name) for region in Region.query.all()]
    form.region.default = '1'
    if request.method == 'POST':
        emplacement = Emplacement.query.filter_by(id=form.emplacement.data).first()
        region = Region.query.filter_by(id=form.region.data).first()
        municipality = Municipality.query.filter_by(id=form.municipality.data).first()
        area = int(form.area.data)
        roomNumber = int(form.roomNumber.data)
        emp = emplacement.id
        int_features = [emp, roomNumber, area]
        final = np.array(transf(int_features)).reshape(-1, 59)
        print("**" , final)

        final[:,57:] = sc_X.transform(final[:,57:]) 
        print("**" , final)

        prediction = model.predict(final)

        return render_template('price.html',price=round(prediction[0], 2))
    return render_template('predict.html', form=form)
 
@pred.route('/municipality/<get_municipality>')###
def municipalitybyregion(get_municipality):
    municipality = Municipality.query.filter_by(region_id=get_municipality).all()
    municipalityArray = []
    for emplacement in municipality:
        municipalityObj = {}
        municipalityObj['id'] = emplacement.id
        municipalityObj['name'] = emplacement.name
        municipalityArray.append(municipalityObj)
    return jsonify({'municipalityregion' : municipalityArray})
  
@pred.route('/emplacement/<get_emplacement>')
def emplacement(get_emplacement):
    municipality_data = Emplacement.query.filter_by(municipality_id=get_emplacement).all()
    emplacementArray = []
    for emplacement in municipality_data:
        emplacementObj = {}
        emplacementObj['id'] = emplacement.id
        emplacementObj['name'] = emplacement.name
        emplacementArray.append(emplacementObj)
    return jsonify({'emplacementlist' : emplacementArray}) 

