async function lookupCar() {
    const id = document.getElementById("listing_id").value;
    if (!id) return;

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<p class='loading'>Looking up car...</p>";

    try {
        const res = await fetch(`${API_URL}/cars/${id}`);
        const car = await res.json();

        if (res.status === 404) {
            resultDiv.innerHTML = "<p class='no-results'>No car found with that ID.</p>";
            return;
        }

        resultDiv.innerHTML = `
            <div class='car-card'>
                <div class='car-header'>
                    <span class='car-title'>${car.manufacturer.toUpperCase()} ${car.model}</span>
                    <span class='car-price'>$${car.price.toLocaleString()}</span>
                </div>
                <div class='extra-grid' style='margin-top:16px'>
                    <div><span class='extra-label'>Listing ID</span><span class='extra-value'>${car.listing_id}</span></div>
                    <div><span class='extra-label'>Year</span><span class='extra-value'>${car.year}</span></div>
                    <div><span class='extra-label'>Fuel</span><span class='extra-value'>${car.fuel || "N/A"}</span></div>
                    <div><span class='extra-label'>Transmission</span><span class='extra-value'>${car.transmission || "N/A"}</span></div>
                    <div><span class='extra-label'>Odometer</span><span class='extra-value'>${car.odometer ? car.odometer.toLocaleString() + " mi" : "N/A"}</span></div>
                    <div><span class='extra-label'>Body Type</span><span class='extra-value'>${car.body_type || "N/A"}</span></div>
                    <div><span class='extra-label'>Condition</span><span class='extra-value'>${car.condition || "N/A"}</span></div>
                    <div><span class='extra-label'>State</span><span class='extra-value'>${car.state ? car.state.toUpperCase() : "N/A"}</span></div>
                </div>
                <div style='margin-top:20px'>
                    <a href='similar.html?id=${car.listing_id}' class='btn btn-secondary' style='font-size:0.9rem; padding: 10px 20px'>Find Similar Cars</a>
                </div>
            </div>`;
    } catch {
        resultDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}