from flask import Flask, render_template, request, jsonify
from backend import get_news_recommendations, recommend_news

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    search_query = request.form['search']
    recommendations = get_news_recommendations(search_query)
    
    if recommendations is not None:
        recommended_news = recommend_news(recommendations)
        return jsonify(recommended_news.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Failed to fetch news recommendations.'})

if __name__ == '__main__':
    app.run(debug=True)
