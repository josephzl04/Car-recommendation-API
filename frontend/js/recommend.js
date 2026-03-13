async function recommendCars() {
    const budget = document.getElementById("budget").value;

    if (!budget) {
        document.getElementById("results").innerHTML = "<p class='no-results'>Please enter a budget.</p>";
        return;
    }

    const params = new URLSearchParams();
    params.append("budget", budget);

    const optionalFields = ["max_odometer", "min_year", "fuel", "transmission"];
    optionalFields.forEach(field => {
        const value = document.getElementById(field).value;
        if (value) params.append(field, value);
    });

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p class='loading'>Finding best matches...</p>";

    try {
        const response = await fetch(`${API_URL}/cars/recommend?${params.toString()}`);
        const data = await response.json();

        if (response.status === 404) {
            resultsDiv.innerHTML = "<p class='no-results'>No cars found within your budget.</p>";
            return;
        }

        resultsDiv.innerHTML = `<p class='results-count'>${data.count} recommendations found</p>
            <div class='cars-grid'>
                ${data.recommendations.map((car, index) => `
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
                        <div class='score-badge'>Similiarity Score: ${car.value_score}</div>
                    </div>
                `).join("")}
            </div>`;
    } catch (error) {
        resultsDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}