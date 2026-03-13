async function findSimilar() {
    const listingId = document.getElementById("listing_id").value;

    if (!listingId) {
        document.getElementById("results").innerHTML = "<p class='no-results'>Please enter a listing ID.</p>";
        return;
    }

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p class='loading'>Searching for similar cars...</p>";

    try {
        const response = await fetch(`${API_URL}/cars/similar/${listingId}`);
        const data = await response.json();

        if (response.status === 404) {
            resultsDiv.innerHTML = "<p class='no-results'>No car found with that listing ID.</p>";
            return;
        }

        if (data.similar_cars.length === 0) {
            resultsDiv.innerHTML = "<p class='no-results'>No similar cars found for this listing.</p>";
            return;
        }

        resultsDiv.innerHTML = `<p class='results-count'>${data.similar_cars.length} similar cars found</p>
            <div class='cars-grid'>
                ${data.similar_cars.map(car => `
                    <div class='car-card'>
                        <div class='car-header'>
                            <span class='car-title'>${car.manufacturer.toUpperCase()} ${car.model}</span>
                            <span class='car-price'>$${car.price.toLocaleString()}</span>
                        </div>
                        <div class='car-details'>
                            <span>${car.year}</span>
                            <span>${car.fuel}</span>
                            <span>${car.transmission}</span>
                            <span>${car.odometer.toLocaleString()} mi</span>
                            <span>${car.state.toUpperCase()}</span>
                        </div>
                        <div class='listing-id'>ID: ${car.listing_id}</div>
                    </div>
                `).join("")}
            </div>`;
    } catch (error) {
        resultsDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}