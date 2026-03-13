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

                <h3 style='color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin: 16px 0 10px'>Vehicle Info</h3>
                <div class='extra-grid'>
                    <div><span class='extra-label'>Listing ID</span><span class='extra-value'>${car.listing_id}</span></div>
                    <div><span class='extra-label'>Manufacturer</span><span class='extra-value'>${car.manufacturer}</span></div>
                    <div><span class='extra-label'>Model</span><span class='extra-value'>${car.model}</span></div>
                    <div><span class='extra-label'>Year</span><span class='extra-value'>${car.year}</span></div>
                </div>

                <h3 style='color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin: 16px 0 10px'>Condition & Specs</h3>
                <div class='extra-grid'>
                    <div><span class='extra-label'>Condition</span><span class='extra-value'>${car.condition || "N/A"}</span></div>
                    <div><span class='extra-label'>Odometer</span><span class='extra-value'>${car.odometer ? car.odometer.toLocaleString() + " mi" : "N/A"}</span></div>
                    <div><span class='extra-label'>Fuel</span><span class='extra-value'>${car.fuel || "N/A"}</span></div>
                    <div><span class='extra-label'>Transmission</span><span class='extra-value'>${car.transmission || "N/A"}</span></div>
                </div>

                <h3 style='color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin: 16px 0 10px'>Listing Info</h3>
                <div class='extra-grid'>
                    <div><span class='extra-label'>Body Type</span><span class='extra-value'>${car.body_type || "N/A"}</span></div>
                    <div><span class='extra-label'>State</span><span class='extra-value'>${car.state ? car.state.toUpperCase() : "N/A"}</span></div>
                    <div><span class='extra-label'>Price</span><span class='extra-value'>$${car.price.toLocaleString()}</span></div>
                </div>

                <div style='margin-top:20px; display:flex; gap:12px'>
                    <a href='similar.html?id=${car.listing_id}' class='btn btn-secondary' style='font-size:0.9rem; padding:10px 20px'>Find Similar Cars</a>
                </div>
            </div>`;
    } catch {
        resultDiv.innerHTML = "<p class='no-results'>Error connecting to API.</p>";
    }
}