<script setup>
import { ref, onMounted, computed } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom'; // Import zoom plugin
import { Bar } from 'vue-chartjs';

// Register Chart.js components and zoom plugin
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, zoomPlugin);

const chartData = ref(null);
const selectedContributors = ref([]); // Stores user-selected contributors
const contributors = ref(['Coal CO₂', 'Oil CO₂', 'Gas CO₂', 'Flaring CO₂', 'Other Industry CO₂']); // Available contributors

// Dynamic Chart Options
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Greenhouse Gas Contributors in China',
    },
    tooltip: {
      callbacks: {
        label: (context) => `${context.dataset.label}: ${context.raw.toLocaleString()} Mt`,
      },
    },
    legend: {
      position: 'top',
    },
    zoom: {
      pan: {
        enabled: true, // Enable panning
        mode: 'x', // Pan along x-axis
      },
      zoom: {
        wheel: {
          enabled: true, // Enable zoom via mouse wheel
        },
        pinch: {
          enabled: true, // Enable pinch zoom on touch devices
        },
        mode: 'x', // Zoom along x-axis
      },
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
      stacked: true, // Enable stacking
      title: {
        display: true,
        text: 'Emissions (Million Tonnes)',
      },
    },
  },
}));

// Fetch Data and Compute Total GHG Line
const fetchGHGContributors = async () => {
  try {
    // Fetch data from the Flask API
    const response = await fetch('http://localhost:5000/ghg_contributors');
    const data = await response.json();

    // Calculate total GHG emissions for each year
    const totalGHG = data.year.map((_, index) =>
      data.coal_co2[index] +
      data.oil_co2[index] +
      data.gas_co2[index] +
      data.flaring_co2[index] +
      data.other_industry_co2[index]
    );

    // Prepare chart data
    chartData.value = {
      labels: data.year, // Years on the x-axis
      datasets: [
        {
          label: 'Coal CO₂',
          data: data.coal_co2,
          backgroundColor: '#FF5733', // Orange-red for coal
        },
        {
          label: 'Oil CO₂',
          data: data.oil_co2,
          backgroundColor: '#4287f5', // Blue for oil
        },
        {
          label: 'Gas CO₂',
          data: data.gas_co2,
          backgroundColor: '#42f54e', // Green for gas
        },
        {
          label: 'Flaring CO₂',
          data: data.flaring_co2,
          backgroundColor: '#f5e642', // Yellow for flaring
        },
        {
          label: 'Other Industry CO₂',
          data: data.other_industry_co2,
          backgroundColor: '#8e44ad', // Purple for other industries
        },
        {
          label: 'Total GHG',
          type: 'line', // Line chart for total GHG emissions
          data: totalGHG,
          borderColor: '#000000',
          borderWidth: 2,
          fill: false,
        },
      ],
    };

    // Set all contributors as initially selected
    selectedContributors.value = contributors.value;
  } catch (error) {
    console.error('Error fetching GHG contributors:', error);
  }
};

// Filter Data Dynamically Based on User Selection
const filteredData = computed(() => {
  if (!chartData.value) return null;

  const filteredDatasets = chartData.value.datasets.filter(dataset =>
    selectedContributors.value.includes(dataset.label)
  );

  return {
    ...chartData.value,
    datasets: filteredDatasets,
  };
});

// Reset Zoom Function
const resetZoom = () => {
  const chartInstance = ChartJS.getChart(document.querySelector('canvas'));
  if (chartInstance) chartInstance.resetZoom();
};

// Fetch data on mount
onMounted(fetchGHGContributors);
</script>

<template>
    <div>
      <!-- Contributor Filters -->
      <div class="filters">
        <label v-for="(contributor, index) in contributors" :key="index">
          <input
            type="checkbox"
            :value="contributor"
            v-model="selectedContributors"
          />
          {{ contributor }}
        </label>
      </div>
  
      <!-- Reset Zoom Button -->
      <button @click="resetZoom" style="margin: 10px;">Reset Zoom</button>
  
      <!-- Chart Container -->
      <div style="width: 90vw; height: 85vh; margin: auto; overflow-x: auto;"> <!-- Adjusted width and height -->
        <Bar v-if="filteredData" :data="filteredData" :options="chartOptions" />
        <p v-else>Loading...</p>
      </div>
    </div>
  </template>
  

<style scoped>
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

canvas {
  width: 100% !important; /* Stretch canvas to full width of the container */
  height: 100% !important; /* Stretch canvas to full height of the container */
  max-height: 85vh; /* Prevent canvas from exceeding 85% of viewport height */
  max-width: 90vw; /* Prevent canvas from exceeding 90% of viewport width */
}

</style>