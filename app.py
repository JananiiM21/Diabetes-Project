from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import pickle

scaler = pickle.load(open('scaler.pkl', 'rb'))
model = pickle.load(open('svm_model.pkl', 'rb'))

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True, methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

app.config['SECRET_KEY'] = 'supersecret'
app.config['PROPAGATE_EXCEPTIONS'] = True



@app.route('/submit', methods=['POST'])
def submit():
    prediction = -1
    if request.method == 'POST':
        data = request.json
       
        patient_id = int(data.get('patient_id'))
        pregs = int(data.get('pregs'))
        gluc = int(data.get('gluc'))
        bp = int(data.get('bp'))
        skin = int(data.get('skin'))
        insuli = float(data.get('insuli'))
        bmi = float(data.get('bmi'))
        fun = float(data.get('fun'))
        age = int(data.get('age'))

        input_features = [[pregs, gluc, bp, skin, insuli, bmi, fun, age]]
        prediction = model.predict(scaler.transform(input_features))
        prediction_value = prediction[0].item()

       

        if prediction_value == 0:
            return jsonify(message='It is unlikely for the patient to have diabetes!', prediction_value=prediction_value)
        else:
            return jsonify(message='It is highly likely that the patient already has or will have diabetes!', prediction_value=prediction_value)

@app.route('/', methods=['GET'])
def status():
    # Handling preflight requests
    if request.method == 'OPTIONS':
        return '', 200

    return "Diabetes Disease Detection"

if __name__ == '__main__':
    app.run(debug=True)
