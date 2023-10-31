from flask import Flask, request, jsonify
from content import ContentBasedRecommender
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
cb = ContentBasedRecommender()

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    title = data.get('title')
    k = data.get('k')

    if not title or k is None:
        return jsonify({"error": "Invalid request. Make sure 'title' and 'k' are provided."}), 400

    recommendations = cb.recommend(title, k)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)