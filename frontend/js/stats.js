function renderTable(data, columns) {
    if (!data || data.length === 0) return "<p class='no-results'>No data available.</p>";
    return `
        <table class="stats-table">
            <thead>
                <tr>${columns.map(c => `<th>${c.label}</th>`).join("")}</tr>
            </thead>
            <tbody>
                ${data.map(row => `
                    <tr>${columns.map(c => `
                        <td>${c.format ? c.format(row[c.key]) : row[c.key]}</td>
                    `).join("")}</tr>
                `).join("")}
            </tbody>
        </table>`;
}

async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/stats/market-insights`);
        const data = await res.json();

        document.getElementById("manufacturers").innerHTML = renderTable(
            data.most_affordable_manufacturers,
            [
                { key: "manufacturer", label: "Manufacturer" },
                { key: "avg_price", label: "Avg Price", format: v => "$" + Number(v).toLocaleString() },
                { key: "listings", label: "Listings" }
            ]
        );

        document.getElementById("states").innerHTML = renderTable(
            data.best_value_states,
            [
                { key: "state", label: "State" },
                { key: "avg_price", label: "Avg Price", format: v => "$" + Number(v).toLocaleString() },
                { key: "listings", label: "Listings" }
            ]
        );

        document.getElementById("body-types").innerHTML = renderTable(
            data.price_by_body_type,
            [
                { key: "body_type", label: "Body Type" },
                { key: "avg_price", label: "Avg Price", format: v => "$" + Number(v).toLocaleString() },
                { key: "listings", label: "Listings" }
            ]
        );

        const trendsRes = await fetch(`${API_URL}/stats/price-trends`);
        const trendsData = await trendsRes.json();

        document.getElementById("price-trends").innerHTML = renderTable(
            trendsData.price_trends,
            [
                { key: "year", label: "Year" },
                { key: "avg_price", label: "Avg Price", format: v => "$" + Number(v).toLocaleString() },
                { key: "listings", label: "Listings" }
            ]
        );

    } catch (error) {
        console.error("Failed to load stats:", error);
    }
}

loadStats();