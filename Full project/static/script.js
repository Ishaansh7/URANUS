document.addEventListener('DOMContentLoaded', function () {
    // Function to handle form submission
    document.getElementById('search-button').addEventListener('click', function () {
        // Get the search query entered by the user
        var searchQuery = document.getElementById('search-text').value;

        // Send a POST request to the root URL with the search query
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'search=' + encodeURIComponent(searchQuery) // Encode search query
        })
            .then(response => response.json()) // Parse response as JSON
            .then(data => {
                // Update the cards container with the recommendations
                updateCards(data);
            })
            .catch(error => console.error('Error fetching recommendations:', error));
    });

    // Function to update cards container with recommendations
    function updateCards(recommendations) {
        var cardsContainer = document.getElementById('cards-container');
        cardsContainer.innerHTML = ''; // Clear existing cards

        recommendations.forEach(function (newsItem) {
            var template = document.getElementById('template-news-card');
            var clone = template.content.cloneNode(true);
            clone.querySelector('#news-title').textContent = newsItem.headline;
            clone.querySelector('#news-source').textContent = newsItem.source;
            clone.querySelector('#news-desc').textContent = newsItem.abstract;
            clone.querySelector('#news-img').src = newsItem.urlToImage || 'https://via.placeholder.com/400x200';
            cardsContainer.appendChild(clone);
        });
    }
});
