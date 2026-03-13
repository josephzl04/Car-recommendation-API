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
        const trends = trendsData.price_trends.reverse(); // oldest to newest

        const ctx = document.getElementById("price-chart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: trends.map(t => t.year),
                datasets: [{
                    label: "Average Price ($)",
                    data: trends.map(t => t.avg_price),
                    backgroundColor: "rgba(233, 69, 96, 0.7)",
                    borderColor: "#e94560",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: "white" } }
                },
                scales: {
                    x: { ticks: { color: "white" }, grid: { color: "rgba(255,255,255,0.1)" } },
                    y: { ticks: { color: "white", callback: v => "$" + v.toLocaleString() }, grid: { color: "rgba(255,255,255,0.1)" } }
                }
            }
        });

    } catch (error) {
        console.error("Failed to load stats:", error);
    }
}

loadStats();