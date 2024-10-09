from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

app = Flask(__name__)

MODEL_PATH = 'model.joblib'

def load_model():
    return joblib.load(MODEL_PATH)

pipeline = load_model()

@app.route('/')
def home():
    return "Welcome to the Text Classification API!"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global pipeline
    if request.method == 'POST':
        try:
            sentences = request.form.get('sentences').split('\n')
            if not sentences:
                return render_template('predict.html', error='Please provide at least one sentence.')
            
            single_entry = pd.DataFrame({'Textos_espanol': sentences})
            predictions = pipeline.predict(single_entry)

            return render_template('predict.html', predictions=zip(sentences, predictions))

        except Exception as e:
            return render_template('predict.html', error=str(e))

    return render_template('predict.html')

@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    global pipeline
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return render_template('retrain.html', error='Please provide an Excel file.')

        file = request.files['file']
        # try:
        df = pd.read_excel(file)

        if 'Textos_espanol' not in df or 'sdg' not in df:
            return render_template('retrain.html', error='The Excel file must contain Textos_espanol and sdg columns.')
        
        X = df[['Textos_espanol']]
        y = df['sdg']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        pipeline.fit(X_train, y_train)

        joblib.dump(pipeline, MODEL_PATH)

        pipeline = load_model()

        y_pred = pipeline.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)

        return render_template('retrain.html', message='Model retrained successfully.', report=report)

        # except Exception as e:
        #     return render_template('retrain.html', error=str(e))

    return render_template('retrain.html')

if __name__ == '__main__':
    app.run(debug=True)
