<template>
    <div class="graph-container">
        <canvas ref="chartCanvas" width="800" height="600"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

let chartInstance = null; // Chart.js instance
const chartCanvas = ref(null); // Reference to the canvas element

const props = defineProps({
    selectedYear: {
        type: Number,
        required: true,
    },
    selectedCountry: {
        type: String,
        required: true,
    },
});

// Fetch emissions data for the radar chart
const fetchRadarData = async (year, country) => {
    const chinaResponse = await fetch(
        `http://localhost:5000/emissions_by_year?country=China&year=${year}`
    );
    const chinaData = await chinaResponse.json();

    const otherCountryResponse = await fetch(
        `http://localhost:5000/emissions_by_year?country=${country}&year=${year}`
    );
    const otherCountryData = await otherCountryResponse.json();

    // Map attributes to labels with units
    const attributeLabelsWithUnits = {
        "Coal CO₂ (per capita)": "Coal CO₂ (Tonnes per Capita)",
        "Flaring CO₂ (per capita)": "Flaring CO₂ (Tonnes per Capita)",
        "Gas CO₂ (per capita)": "Gas CO₂ (Tonnes per Capita)",
        "Oil CO₂ (per capita)": "Oil CO₂ (Tonnes per Capita)",
        "Other CO₂ (per capita)": "Other CO₂ (Tonnes per Capita)",
    };


    return {
        labels: Object.keys(chinaData.emissions).map(
            (key) => attributeLabelsWithUnits[key]
        ), // Update labels to include units
        datasets: [
            {
                label: `China (${year}, per capita)`,
                data: Object.values(chinaData.emissions),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
            },
            {
                label: `${country} (${year}, per capita)`,
                data: Object.values(otherCountryData.emissions),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
            },
        ],
    };
};


// Render the radar chart
const renderRadarChart = async () => {
    const data = await fetchRadarData(props.selectedYear, props.selectedCountry);

    await nextTick(); // Ensure the canvas is ready

    const ctx = chartCanvas.value.getContext('2d'); // Get canvas context
    if (chartInstance) {
        chartInstance.destroy(); // Destroy the old chart instance
    }

    chartInstance = new Chart(ctx, {
        type: 'radar',
        data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#FFFFFF', // Make legend labels white
                    },
                },
                title: {
                    display: true,
                    text: `Per Capita Greenhouse Gas Emissions (Tonnes per Capita): China vs. ${props.selectedCountry} (${props.selectedYear})`,
                    color: '#FFFFFF', // Make the title white
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const label = context.dataset.label || '';
                            const value = context.raw || 0;
                            const attribute = context.label; // Use the updated label with units
                            return `${label} - ${attribute}: ${value.toFixed(2)} Tonnes per Capita`;
                        },
                    },
                },
            },
            scales: {
                r: {
                    angleLines: {
                        color: '#FFFFFF', // Make angle lines white
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.2)', // Make gridlines light gray
                    },
                    pointLabels: {
                        color: '#FFFFFF', // Make labels at each point (axes) white
                        font: {
                            size: 14, // Increase font size for better visibility
                        },
                    },
                    ticks: {
                        color: '#FFFFFF', // Make ticks white
                        backdropColor: '#181818', // Match backdrop color with the chart background
                        callback: (value) => `${value.toFixed(2)}`, // Format ticks with two decimal places
                    },
                },
            },
        },
    });



};

// Watch for changes in props and re-render the chart
watch(
    () => [props.selectedYear, props.selectedCountry],
    renderRadarChart,
    { immediate: true }
);

onMounted(renderRadarChart);
</script>

<style scoped>
.graph-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 80vh;
    max-width: 630px; /*Limited the width of the graph, if not it will overflow*/
    max-height: 480px;
}

canvas {
    max-width: 100%;
    max-height: 100%;
}
</style>