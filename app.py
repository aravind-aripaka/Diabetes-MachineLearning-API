from flask import Flask,request
from flask_restful import Resource, Api
import pickle 
import pandas as pd
from flask_cors import CORS
import joblib 

app =  Flask(__name__)
#
CORS(app)
#create an api object 
api = Api(app)

class prediction(Resource):
    def get(self,Pregnancies,Glucose,BloodPressure,BMI,DiabetesPedigreeFunction,Age):
        data_dict = {
            'Pregnancies':[Pregnancies],
            'Glucose':[Glucose],
            'BloodPressure':[BloodPressure],
            'BMI':[BMI],
            'DiabetesPedigreeFunction':[DiabetesPedigreeFunction],
            'Age':[Age]
        }
        df = pd.DataFrame(data=data_dict)
        model = joblib.load(r'diabetes_model.pkl')
        prediction = model.predict(df);
        # prediction = int[prediction[0]]
        return str(prediction[0])

##data.xslx
class getData(Resource):
    def get(self):
        df = pd.read_excel('data.xlsx')
        df = df.rename({'Pregnancies':'Pregnancies',
            'Glucose':'Glucose',
            'BloodPressure':'Blood Pressure',
            'BMI':'BMI',
            'DiabetesPedigreeFunction':'Diabetes Pedigree Function',
            'Age':'Age'})
        res = df.to_json(orient='records')
        return res

api.add_resource(getData,'/api')
api.add_resource(prediction, '/prediction/<int:Pregnancies>/<int:Glucose>/<int:BloodPressure>/<float:BMI>/<float:DiabetesPedigreeFunction>/<int:Age>')

if __name__ == '__main__':
    app.run(debug=True)