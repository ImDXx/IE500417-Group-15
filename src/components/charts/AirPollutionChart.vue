<script setup>
import { ref, onMounted } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Bar } from 'vue-chartjs';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = ref(null);

// Fetch the air pollution data from the backend
const fetchAirPollutionData = async () => {
  try {
    const response = await fetch('http://localhost:5000/air_pollution_data');
    const data = await response.json();
    console.log('Fetched Data:', data);

    const years = Object.keys(data[Object.keys(data)[0]]); // Extract years (2010-2019)
    const countries = Object.keys(data); // Extract countries (China, India, United States)

    // Prepare the datasets for each country
    const datasets = countries.map((country) => {
      const pollutionLevels = years.map((year) => data[country][year]);
      return {
        label: country, 
        data: pollutionLevels,
        backgroundColor: getRandomColor(), // Random color for each country
        borderColor: 'rgba(0, 0, 0, 0.1)', // Border color for the bars
        borderWidth: 1,
      };
    });

    // Set chart data
    chartData.value = {
      labels: years, // Years (2010-2019)
      datasets: datasets, // All datasets for each country
    };
  } catch (error) {
    console.error('Error fetching air pollution data:', error);
  }
};

// Helper function to generate random color for each country
const getRandomColor = () => {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `rgba(${r}, ${g}, ${b}, 0.5)`; // RGBA color with 50% opacity
};

// Fetch data when the component is mounted
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

<script>
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Allow chart to grow
  plugins: {
    title: {
      display: true,
      text: 'Air Pollution Attributable Deaths per Year by Country',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const year = context.label; // Year
          const pollution = context.raw.toFixed(2); 
          return `${year}: ${pollution} deaths`;
        },
      },
    },
    legend: {
      display: true, 
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Year',
      },
    },
    y: {
      title: {
        display: true,
        text: 'Deaths per Year',
      },
      min: 0,
      suggestedMax: 1000, // Adjust this value if needed based on data
    },
  },
};
</script>

<style scoped>
canvas {
  max-width: 100%; /* Allow canvas to resize dynamically */
  height: 600px; /* Set a larger height for better visibility */
}
</style>