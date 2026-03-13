function toggleDetails(id) {
    const extra = document.getElementById(`extra-${id}`);
    const btn = document.querySelector(`#car-${id} .btn-expand`);
    if (extra.style.display === "none") {
        extra.style.display = "block";
        btn.textContent = "Hide Details";
    } else {
        extra.style.display = "none";
        btn.textContent = "View Details";
    }
}
async function searchCars() {
    const params = new URLSearchParams();

    const fields = ["manufacturer", "min_price", "max_price", "min_year", "max_year", "fuel", "transmission", "state"];
    fields.forEach(field => {
        const value = document.getElementById(field).value;
        if (value) params.append(field, value);
    });

    params.append("limit", 50);

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
                    <div class='car-card' id='car-${car.listing_id}'>
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
                        <div class='car-extra' id='extra-${car.listing_id}' style='display:none'>
                            <div class='extra-grid'>
                                <div><span class='extra-label'>Listing ID</span><span class='extra-value'>${car.listing_id}</span></div>
                                <div><span class='extra-label'>Body Type</span><span class='extra-value'>${car.body_type || "N/A"}</span></div>
                                <div><span class='extra-label'>Condition</span><span class='extra-value'>${car.condition || "N/A"}</span></div>
                                <div><span class='extra-label'>State</span><span class='extra-value'>${car.state ? car.state.toUpperCase() : "N/A"}</span></div>
                            </div>
                        </div>
                        <button class='btn-expand' onclick='toggleDetails(${car.listing_id})'>View Details</button>
                        <div class='listing-id'>ID: ${car.listing_id}</div>
                    </div>
                `).join("")}
            </div>`;
    } catch (error) {
        resultsDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}