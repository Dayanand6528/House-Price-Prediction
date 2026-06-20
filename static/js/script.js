document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons//
    lucide.createIcons();

    // DOM References//
    const form = document.getElementById('prediction-form');
    const predictBtn = document.getElementById('predict-btn');
    const btnText = predictBtn.querySelector('.btn-text');
    const btnLoader = predictBtn.querySelector('.btn-loader');
    const priceDisplay = document.getElementById('predicted-price');
    
    const detailsSummary = document.getElementById('price-details-summary');
    const sumArea = document.getElementById('sum-area');
    const sumBeds = document.getElementById('sum-beds');
    const sumAge = document.getElementById('sum-age');

    const statTotal = document.getElementById('stat-total');
    const statAvg = document.getElementById('stat-avg');
    const historyTableBody = document.getElementById('history-table-body');

    // Chart References//
    let scatterChart = null;
    let bedroomChart = null;

    // --- Tab Navigation Setup ---//
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Toggle Active Tab Buttons//
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Toggle Active Tab Contents//
            tabContents.forEach(content => {
                if (content.id === targetTab) {
                    content.classList.add('active');
                } else {
                    content.classList.remove('active');
                }
            });

            // Re-render charts to solve resize issues inside hidden tabs//
            if (targetTab === 'analytics-tab') {
                if (scatterChart) scatterChart.resize();
                if (bedroomChart) bedroomChart.resize();
            }
        });
    });

    // --- Price Animation ---//
    function animatePrice(targetValue) {
        let start = 0;
        const duration = 1200; // ms
        let startTimestamp = null;
        
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            // Easing function: easeOutQuad//
            const easedProgress = progress * (2 - progress);
            const currentValue = Math.floor(easedProgress * targetValue);
            
            priceDisplay.innerHTML = currentValue.toLocaleString('en-US');
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // --- Chart.js Configurations ---//
    const chartDefaults = {
        color: '#9ca3af',
        font: {
            family: 'Outfit, Inter, sans-serif',
            size: 11
        },
        gridColor: 'rgba(255, 255, 255, 0.05)'
    };

    function initScatterChart(dataPoints) {
        const ctx = document.getElementById('scatterChart').getContext('2d');
        if (scatterChart) {
            scatterChart.destroy();
        }

        scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Properties Appraised',
                    data: dataPoints,
                    backgroundColor: 'rgba(6, 182, 212, 0.5)',
                    borderColor: '#06b6d4',
                    borderWidth: 1,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Area: ${context.parsed.x} sqft, Price: ₹${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: chartDefaults.gridColor },
                        ticks: { color: chartDefaults.color },
                        title: { display: true, text: 'Area (Square Feet)', color: chartDefaults.color }
                    },
                    y: {
                        grid: { color: chartDefaults.gridColor },
                        ticks: { 
                            color: chartDefaults.color,
                            callback: function(value) { return '₹' + value.toLocaleString(); }
                        },
                        title: { display: true, text: 'Predicted Price (₹)', color: chartDefaults.color }
                    }
                }
            }
        });
    }

    function initBedroomChart(labels, values) {
        const ctx = document.getElementById('bedroomChart').getContext('2d');
        if (bedroomChart) {
            bedroomChart.destroy();
        }

        bedroomChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.map(l => `${l} BHK`),
                datasets: [{
                    label: 'Average Price',
                    data: values,
                    backgroundColor: 'rgba(99, 102, 241, 0.45)',
                    borderColor: '#6366f1',
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Average Price: ₹${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: chartDefaults.color },
                        title: { display: true, text: 'Bedroom Count', color: chartDefaults.color }
                    },
                    y: {
                        grid: { color: chartDefaults.gridColor },
                        ticks: {
                            color: chartDefaults.color,
                            callback: function(value) { return '₹' + value.toLocaleString(); }
                        },
                        title: { display: true, text: 'Average Value (₹)', color: chartDefaults.color }
                    }
                }
            }
        });
    }

    // --- Fetch Dashboard Stats & Render Charts ---//
    async function updateDashboardData() {
        try {
            // 1. Fetch Stats & Aggregates//
            const statsRes = await fetch('/api/stats');
            const stats = await statsRes.json();

            if (stats.error) {
                console.error(stats.error);
                return;
            }

            // Update Counter metrics//
            statTotal.innerText = stats.total_predictions;
            statAvg.innerText = '₹' + Math.round(stats.average_price).toLocaleString();

            // Render Scatter//
            initScatterChart(stats.scatter_data);

            // Render Bar//
            initBedroomChart(stats.bar_data.labels, stats.bar_data.values);

            // 2. Fetch History Table//
            const historyRes = await fetch('/api/history');
            const history = await historyRes.json();

            renderHistoryTable(history);

        } catch (err) {
            console.error('Error loading dashboard analytics:', err);
        }
    }

    // --- Render History Table HTML ---//
    function renderHistoryTable(data) {
        if (!data || data.length === 0) {
            historyTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-state">
                        <i data-lucide="database-backup" class="empty-icon"></i>
                        <p>No appraisal records found. Submit property details to populate the database.</p>
                    </td>
                </tr>
            `;
            lucide.createIcons();
            return;
        }

        let html = '';
        data.forEach(row => {
            html += `
                <tr>
                    <td>${row.created_at}</td>
                    <td>${row.area.toLocaleString()}</td>
                    <td>${row.bedrooms} BHK</td>
                    <td>${row.bathrooms} Bath</td>
                    <td>${row.parking}</td>
                    <td>${row.house_age} Years</td>
                    <td>₹${row.predicted_price.toLocaleString()}</td>
                </tr>
            `;
        });
        historyTableBody.innerHTML = html;
    }

    // --- Handle Prediction Form Submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI states: Loading
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
        predictBtn.disabled = true;

        const formData = {
            area: document.getElementById('area').value,
            bedrooms: document.getElementById('bedrooms').value,
            bathrooms: document.getElementById('bathrooms').value,
            house_age: document.getElementById('house_age').value,
            parking: document.getElementById('parking').checked ? 1 : 0
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // Animate price display
                animatePrice(result.predicted_price);

                // Show details summary tag
                sumArea.innerText = Number(formData.area).toLocaleString();
                sumBeds.innerText = formData.bedrooms;
                sumAge.innerText = formData.house_age;
                detailsSummary.classList.remove('hidden');

                // Update charts & history dynamically
                await updateDashboardData();
            } else {
                alert(`Prediction Error: ${result.error}`);
            }

        } catch (err) {
            console.error(err);
            alert('Failed to connect to the prediction server. Please try again.');
        } finally {
            // UI states: Done Loading
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            predictBtn.disabled = false;
        }
    });

    // Initial Dashboard Load
    updateDashboardData();
});
