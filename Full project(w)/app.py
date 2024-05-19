from flask import Flask, render_template, request, jsonify
from backend import get_news_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    search_query = request.form.get('search')
    if search_query:
        recommendations = get_news_recommendations(search_query)
        if recommendations is not None:
            return jsonify(recommendations)
        else:
            return jsonify({'error': 'Failed to fetch news recommendations.'}), 500
    else:
        return jsonify({'error': 'Please enter a search query.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
