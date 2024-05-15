from flask import Flask, render_template, request, jsonify
from backend import get_news_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')  # Get search query from form data
        if search_query:
            recommendations = get_news_recommendations(search_query)
            if recommendations is not None:
                return render_template('index.html', recommendations=recommendations)
            else:
                return render_template('index.html', error='Failed to fetch news recommendations.')
        else:
            return render_template('index.html', error='Please enter a search query.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
