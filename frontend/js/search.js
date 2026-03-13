async function searchCars() {
    const params = new URLSearchParams();

    const fields = ["manufacturer", "min_price", "max_price", "min_year", "max_year", "fuel", "transmission", "state"];
    fields.forEach(field => {
        const value = document.getElementById(field).value;
        if (value) params.append(field, value);
    });

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p class='loading'>Searching...</p>";

    try {
        const response = await fetch(`${API_URL}/cars/search?${params.toString()}`);
        const data = await response.json();

        if (response.status === 404) {
            resultsDiv.innerHTML = "<p class='no-results'>No cars found matching your filters.</p>";
            return;
        }

        resultsDiv.innerHTML = `<p class='results-count'>${data.count} cars found</p>
            <div class='cars-grid'>
                ${data.cars.map(car => `
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
                    </div>
                `).join("")}
            </div>`;
    } catch (error) {
        resultsDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}