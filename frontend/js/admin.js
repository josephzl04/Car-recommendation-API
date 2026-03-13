let storedApiKey = "";

async function unlockAdmin() {
    const key = document.getElementById("api_key").value;
    if (!key) return showResult("auth-result", "Please enter your API key.", false);

    try {
        const res = await fetch(`${API_URL}/admin/test`, {
            headers: { "X-API-Key": key }
        });
        if (res.status === 200) {
            storedApiKey = key;
            document.getElementById("admin-content").style.display = "block";
            document.querySelector(".search-form").style.display = "none";
            showResult("auth-result", "Access granted.", true);
        } else {
            showResult("auth-result", "Invalid API key.", false);
        }
    } catch {
        showResult("auth-result", "Error connecting to API.", false);
    }
}

function getApiKey() {
    return storedApiKey;
}
function showResult(elementId, message, success) {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = "form-result " + (success ? "result-success" : "result-error");
}

async function createCar() {
    const key = getApiKey();
    if (!key) return showResult("create-result", "Please enter your API key.", false);

    const body = {
        manufacturer: document.getElementById("c_manufacturer").value,
        model: document.getElementById("c_model").value,
        year: parseInt(document.getElementById("c_year").value),
        price: parseInt(document.getElementById("c_price").value),
        transmission: document.getElementById("c_transmission").value,
        fuel: document.getElementById("c_fuel").value || null,
        odometer: parseInt(document.getElementById("c_odometer").value) || null,
        state: document.getElementById("c_state").value || null,
        condition: document.getElementById("c_condition").value || null,
        body_type: document.getElementById("c_body_type").value || null,
    };

    if (!body.manufacturer || !body.model || !body.year || !body.price || !body.transmission) {
    return showResult("create-result", "Manufacturer, model, year, price and transmission are required.", false);
    }

    console.log("Sending content:", JSON.stringify(body));

    try {
        const res = await fetch(`${API_URL}/cars`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-API-Key": key },
            body: JSON.stringify(body)
        });
        const data = await res.json();
        if (res.status === 201) {
            showResult("create-result", `Car created successfully. Listing ID: ${data.listing_id}`, true);
        } else if (res.status === 401) {
            showResult("create-result", "Invalid API key.", false);
        } else {
            showResult("create-result", "Failed to create car.", false);
        }
    } catch {
        showResult("create-result", "Error connecting to API.", false);
    }
}

async function updateCar() {
    const key = getApiKey();
    if (!key) return showResult("update-result", "Please enter your API key.", false);

    const listingId = document.getElementById("u_listing_id").value;
    if (!listingId) return showResult("update-result", "Please enter a listing ID.", false);

   const body = {};
    const fields = {
        manufacturer: document.getElementById("u_manufacturer").value,
        model: document.getElementById("u_model").value,
        year: document.getElementById("u_year").value,
        price: document.getElementById("u_price").value,
        transmission: document.getElementById("u_transmission").value,
        fuel: document.getElementById("u_fuel").value,
        odometer: document.getElementById("u_odometer").value,
        state: document.getElementById("u_state").value,
        condition: document.getElementById("u_condition").value,
        body_type: document.getElementById("u_body_type").value,
    };

    const intFields = ["year", "price", "odometer"];
    for (const [key, value] of Object.entries(fields)) {
        if (value) {
            body[key] = intFields.includes(key) ? parseInt(value) : value;
        }
    }

    if (Object.keys(body).length === 0) {
        return showResult("update-result", "Please enter at least one field to update.", false);
    }

    try {
        const res = await fetch(`${API_URL}/cars/${listingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json", "X-API-Key": key },
            body: JSON.stringify(body)
        });
        if (res.status === 200) {
            showResult("update-result", `Listing ${listingId} updated successfully.`, true);
        } else if (res.status === 401) {
            showResult("update-result", "Invalid API key.", false);
        } else if (res.status === 404) {
            showResult("update-result", "Listing not found.", false);
        } else {
            showResult("update-result", "Failed to update listing.", false);
        }
    } catch {
        showResult("update-result", "Error connecting to API.", false);
    }
}

async function deleteCar() {
    const key = getApiKey();
    if (!key) return showResult("delete-result", "Please enter your API key.", false);

    const listingId = document.getElementById("d_listing_id").value;
    if (!listingId) return showResult("delete-result", "Please enter a listing ID.", false);

    try {
        const res = await fetch(`${API_URL}/cars/${listingId}`, {
            method: "DELETE",
            headers: { "X-API-Key": key }
        });
        if (res.status === 200) {
            showResult("delete-result", `Listing ${listingId} deleted successfully.`, true);
        } else if (res.status === 401) {
            showResult("delete-result", "Invalid API key.", false);
        } else if (res.status === 404) {
            showResult("delete-result", "Listing not found.", false);
        } else {
            showResult("delete-result", "Failed to delete listing.", false);
        }
    } catch {
        showResult("delete-result", "Error connecting to API.", false);
    }
}