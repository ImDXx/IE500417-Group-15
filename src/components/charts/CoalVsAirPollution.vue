<template>
    <div class="graph-container">
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(...registerables, zoomPlugin);

const chartCanvas = ref(null);
const source = "Source: Our World in Data and World Health Organization";
let chartInstance = null;

const fetchCoalVsAirPollutionData = async () => {
    const response = await fetch('http://localhost:5000/coal_vs_air_pollution');
    return response.json();
};

const renderGraph = async () => {
    const data = await fetchCoalVsAirPollutionData();

    const years = data.year;
    const coalEmissions = data.coal_co2;
    const nonCoalEmissions = data.non_coal_co2;
    const airPollutionDeaths = data.air_pollution_deaths;

    const ctx = chartCanvas.value.getContext('2d');

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Coal CO₂ Emissions (Million Tonnes)',
                    data: coalEmissions,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    yAxisID: 'y1',
                    borderWidth: 2,
                },
                {
                    label: 'Non-Coal CO₂ Emissions (Million Tonnes)',
                    data: nonCoalEmissions,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    yAxisID: 'y1',
                    borderWidth: 2,
                },
                {
                    label: 'Air Pollution Deaths (Thousands)',
                    data: airPollutionDeaths,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    yAxisID: 'y2',
                    borderWidth: 2,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Impact of Coal CO₂ Emissions on Air Pollution Deaths in China',
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const datasetLabel = context.dataset.label || '';
                            const value = context.raw || 0;
                            if (context.dataset.yAxisID === 'y1') {
                                return `${datasetLabel}: ${value.toLocaleString()} MT`;
                            } else if (context.dataset.yAxisID === 'y2') {
                                return `${datasetLabel}: ${value.toLocaleString()} Deaths`;
                            }
                            return `${datasetLabel}: ${value}`;
                        },
                    },
                },
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x', // Allow panning only along the x-axis
                    },
                    zoom: {
                        wheel: {
                            enabled: true, // Enable zooming with mouse wheel
                        },
                        pinch: {
                            enabled: true, // Enable zooming with touch gestures
                        },
                        mode: 'x', // Allow zooming only along the x-axis
                    },
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year',
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.3)',
                    },
                },
                y1: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Coal CO₂ Emissions (Million Tonnes)',
                    },
                    ticks: {
                        callback: (value) => `${value} MT`,
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.3)',
                    },
                },
                y2: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Average Yearly Air Pollution Deaths',
                    },
                    grid: {
                        drawOnChartArea: false, // Prevent gridlines overlap
                    },
                    ticks: {
                        callback: (value) => `${value}`,
                    },
                },
            },
        },
    });
};

onMounted(renderGraph);

</script>

<style scoped>
.graph-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 80vh;
    background-color: #181818;
}

canvas {
    max-width: 100%;
    max-height: 100%;
}
</style>