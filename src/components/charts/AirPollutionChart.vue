<script setup>
import { ref, onMounted } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Bar } from 'vue-chartjs';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = ref(null);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Allow chart to grow
  plugins: {
    title: {
      display: true,
      text: 'Air Pollution (PM2.5) Levels by Country and Year',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const country = context.dataset.label; // Country name
          const year = context.label; // Year
          const pollution = context.raw.toFixed(2); // Pollution value (formatted)
          return `${country} - ${year}: PM2.5 = ${pollution} µg/m³`;
        },
      },
    },
    legend: {
      display: true, // Show the legend to distinguish between countries
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Year',
      },
      ticks: {
        autoSkip: false, // Do not skip labels
        maxRotation: 45, // Rotate labels for better visibility
        minRotation: 45,
      },
    },
    y: {
      title: {
        display: true,
        text: 'PM2.5 (µg/m³)',
      },
      min: 0, // Minimum value for y-axis
      suggestedMax: 6000, // Maximum value for y-axis (adjust as needed)
    },
  },
};

// Fetch air pollution data from the backend
const fetchAirPollutionData = async () => {
  try {
    const response = await fetch('http://localhost:5000/air_pollution_data');
    const data = await response.json();

    // Prepare data for the chart
    const years = Object.keys(data[Object.keys(data)[0]]); // Extract years from the first country's data
    const countries = Object.keys(data); // Extract countries from the data

    const datasets = countries.map((country) => {
      const pollutionLevels = countries.map(
        (year) => data[country][year] || 0
      );
      return {
        label: country, // Country name as label
        data: pollutionLevels, // Pollution levels for each year
        backgroundColor: getRandomColor(), // Generate random color for each country
        borderColor: 'rgba(0, 0, 0, 0.1)', // Border color for the bars
        borderWidth: 1,
      };
    });

    chartData.value = {
      labels: years, // Years on x-axis
      datasets: datasets, // Multiple datasets for each country
    };
  } catch (error) {
    console.error('Error fetching air pollution data:', error);
  }
};

// Function to generate random colors for each country
const getRandomColor = () => {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `rgba(${r},${g},${b},0.6)`; // RGBA format
};

// Fetch data on component mount
onMounted(fetchAirPollutionData);
</script>

<template>
  <div style="overflow-x: auto; width: 100%; max-height: 700px;"> <!-- Horizontal scrolling and larger size -->
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    <p v-else>Loading...</p>
  </div>
</template>

<style scoped>
canvas {
  max-width: 100%; /* Allow canvas to resize dynamically */
  height: 600px; /* Set a larger height for better visibility */
}
</style>