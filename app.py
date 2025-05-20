from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from model.predict_model import predict_fill_levels
from optimization.route_optimizer import optimize_route

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filepath = os.path.join('uploads', secure_filename(file.filename))
    file.save(filepath)

    # Predict fill levels using ML model
    predictions = predict_fill_levels(filepath)

    # Optimize route using heuristics / DP
    route = optimize_route(predictions)

    return jsonify({
        "predictions": predictions,
        "route": route
    })

if __name__ == '__main__':
    app.run(debug=True)
