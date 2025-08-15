"use strict";

async function loadEntries(query = "") {
    try {
        const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
        if (!res.ok)
            throw new Error(`Failed to fetch entries: ${res.statusText}`);
        const entries = await res.json();
        const table = document.getElementById("entries-table");
        if (!table)
            return;
        table.innerHTML = "<tr><th>Timestamp</th><th>Entry</th></tr>";
        entries.forEach(([ts, text]) => {
            const row = table.insertRow();
            row.insertCell().innerText = ts;
            row.insertCell().innerText = text;
        });
    }
    catch (error) {
        console.error(error);
    }
}
function setupFormHandler() {
    const form = document.getElementById("entry-form");
    if (!form)
        return;
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData(form);
            const res = await fetch("/add-entry", { method: "POST", body: formData });
            if (!res.ok)
                throw new Error(`Failed to add entry: ${res.statusText}`);
            const data = await res.json();
            if (data.success) {
                const imageEl = document.getElementById("chart-img");
                if (imageEl) {
                    imageEl.src = `/chart.png?${Date.now()}`;
                }
                await loadEntries();
                form.reset();
            }
        }
        catch (error) {
            console.error(error);
        }
    });
}
function setupSearchHandler() {
    const searchBox = document.getElementById("search-box");
    if (!searchBox)
        return;
    searchBox.addEventListener("input", () => {
        loadEntries(searchBox.value);
    });
}
document.addEventListener("DOMContentLoaded", () => {
    setupFormHandler();
    setupSearchHandler();
    loadEntries();
});
