document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('search-button').addEventListener('click', function () {
        var searchQuery = document.getElementById('search-text').value;

        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'search=' + encodeURIComponent(searchQuery)
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    updateCards(data);
                }
            })
            .catch(error => console.error('Error fetching recommendations:', error));
    });

    function updateCards(recommendations) {
        var cardsContainer = document.getElementById('cards-container');
        cardsContainer.innerHTML = '';

        recommendations.forEach(function (newsItem) {
            var template = document.getElementById('template-news-card');
            var clone = template.content.cloneNode(true);
            clone.querySelector('.news-title').textContent = newsItem.headline;
            clone.querySelector('.news-source').textContent = newsItem.source;
            clone.querySelector('.news-desc').textContent = newsItem.abstract;
            clone.querySelector('.news-img').src = newsItem.urlToImage || 'https://via.placeholder.com/400x200';
            clone.querySelector('.news-link').href = newsItem.url;
            cardsContainer.appendChild(clone);
        });
    }
});
