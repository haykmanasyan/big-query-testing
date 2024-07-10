let chart;  // Declare chart variable globally

// Fetch data from the Flask endpoint
fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched data:', data);  // Debugging statement
        if (data.error) {
            throw new Error(data.error);
        }
        drawChart(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

function drawChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    const timestamps = data.map(d => new Date(d.time));
    const volumes = data.map(d => d.volume);

    const maxYValue = Math.max(...volumes);  // Find maximum volume value

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [{
                label: 'Volume',
                data: volumes,
                borderColor: 'orange',  // Change line color to orange
                backgroundColor: 'rgba(255, 159, 64, 0.2)',  // Orange background color
                borderWidth: 2,
                fill: true,
                hidden: false  // Initially show the dataset
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // Disable aspect ratio to adjust size
            plugins: {
                title: {
                    display: true,
                    text: 'Volume vs Time',  // Title text
                    font: {
                        size: 16,
                        weight: 'bold'  // Bold title
                    },
                    color: 'black'  // Title color
                },
                legend: {
                    position: 'right',  // Position legend to the right
                    labels: {
                        // Change legend label font color and size
                        font: {
                            size: 14,
                            color: 'black'
                        }
                    },
                    onClick: function(event, legendItem) {
                        // Prevent default toggle behavior
                        event.stopPropagation();
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Volume: ${tooltipItem.raw}`;
                        },
                        title: function(tooltipItems) {
                            return `Time: ${tooltipItems[0].label}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    },
                    title: {
                        display: true,
                        text: 'Timestamp',
                        font: {
                            size: 14,
                            weight: 'bold'  // Make x-axis title bold
                        },
                        color: 'black'  // Set x-axis title color
                    },
                    ticks: {
                        font: {
                            size: 12  // Increase font size for x-axis ticks
                        },
                        color: 'black'  // Set x-axis tick color
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Volume',
                        font: {
                            size: 14,
                            weight: 'bold'  // Make y-axis title bold
                        },
                        color: 'black'  // Set y-axis title color
                    },
                    ticks: {
                        font: {
                            size: 12  // Increase font size for y-axis ticks
                        },
                        color: 'black'  // Set y-axis tick color
                    },
                    suggestedMax: maxYValue + 10  // Add some padding above the highest data point
                }
            }
        }
    });
}
