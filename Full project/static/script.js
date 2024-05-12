// No changes needed for the API key and URL, as they will be handled by the backend
const API_KEY = ""; // Leave empty, as the backend will handle the API key
const url = "/recommend"; // URL to fetch recommendations from the backend

window.addEventListener("load", () => fetchNews("India"));

function reload() {
    window.location.reload();
}

async function fetchNews(query) {
    const res = await fetch(`${url}?search=${query}`);
    const data = await res.json();
    bindData(data);
}

function bindData(recommendationsles) {
    const cardsContainer = document.getElementById("cards-container");
    const newsCardTemplate = document.getElementById("template-news-card");

    cardsContainer.innerHTML = "";

    recommendationsles.forEach((recommendationsle) => {
        if (!recommendationsle.urlToImage) return;
        const cardClone = newsCardTemplate.content.cloneNode(true);
        fillDataInCard(cardClone, recommendationsle);
        cardsContainer.appendChild(cardClone);
    });
}

function fillDataInCard(cardClone, recommendationsle) {
    const newsImg = cardClone.querySelector("#news-img");
    const newsTitle = cardClone.querySelector("#news-title");
    const newsSource = cardClone.querySelector("#news-source");
    const newsDesc = cardClone.querySelector("#news-desc");

    newsImg.src = recommendationsle.urlToImage;
    newsTitle.innerHTML = recommendationsle.headline;
    newsDesc.innerHTML = recommendationsle.abstract;

    // No need to adjust date since it's already formatted on the backend
    newsSource.innerHTML = `${recommendationsle.source} · ${recommendationsle.publishedAt}`;

    cardClone.firstElementChild.addEventListener("click", () => {
        window.open(recommendationsle.url, "_blank");
    });
}

let curSelectedNav = null;
function onNavItemClick(id) {
    fetchNews(id);
    const navItem = document.getElementById(id);
    curSelectedNav?.classList.remove("active");
    curSelectedNav = navItem;
    curSelectedNav.classList.add("active");
}

const searchButton = document.getElementById("search-button");
const searchText = document.getElementById("search-text");

searchButton.addEventListener("click", () => {
    const query = searchText.value;
    if (!query) return;
    fetchNews(query);
    curSelectedNav?.classList.remove("active");
    curSelectedNav = null;
});
