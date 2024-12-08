<template>
  <Bar v-if="filteredData" :data="filteredData" :options="chartOptions" />
  <p v-else>Loading...</p>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import { Bar } from 'vue-chartjs';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, zoomPlugin);

const chartData = ref(null);
const contributors = ref(['Coal CO₂', 'Oil CO₂', 'Gas CO₂', 'Flaring CO₂', 'Other Industry CO₂']);
const selectedContributors = ref(contributors.value);

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
      pan: { enabled: true, mode: 'x' },
      zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'x' },
    },
  },
  scales: {
    x: {
      title: { display: true, text: 'Year', color: '#FFFFFF' },
      ticks: { color: '#FFFFFF' },
      grid: {
        color: 'rgba(255, 255, 255, 0.2)', // Transparent white gridlines
        borderColor: 'rgba(255, 255, 255, 0.3)', // Slightly darker grid border
      },
    },
    y: {
      stacked: true,
      title: { display: true, text: 'Emissions (Million Tonnes)', color: '#FFFFFF' },
      ticks: { color: '#FFFFFF' },
      grid: {
        color: 'rgba(255, 255, 255, 0.2)', // Transparent white gridlines
        borderColor: 'rgba(255, 255, 255, 0.3)', // Slightly darker grid border
      },
    },
  },
}));

const fetchGHGContributors = async () => {
  try {
    const response = await fetch('http://localhost:5000/ghg_contributors');
    const data = await response.json();
    chartData.value = {
      labels: data.year,
      datasets: [
        { label: 'Coal CO₂', data: data.coal_co2, backgroundColor: '#FF5733' },
        { label: 'Oil CO₂', data: data.oil_co2, backgroundColor: '#4287f5' },
        { label: 'Gas CO₂', data: data.gas_co2, backgroundColor: '#42f54e' },
        { label: 'Flaring CO₂', data: data.flaring_co2, backgroundColor: '#f5e642' },
        { label: 'Other Industry CO₂', data: data.other_industry_co2, backgroundColor: '#8e44ad' },
        {
          label: 'Total GHG',
          type: 'line',
          data: data.year.map((_, i) => data.coal_co2[i] + data.oil_co2[i] + data.gas_co2[i] + data.flaring_co2[i] + data.other_industry_co2[i]),
          borderColor: '#FFFFFF',
          borderWidth: 2,
        },
      ],
    };
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const filteredData = computed(() =>
  chartData.value
    ? {
        ...chartData.value,
        datasets: chartData.value.datasets.filter((dataset) => selectedContributors.value.includes(dataset.label)),
      }
    : null
);

onMounted(fetchGHGContributors);
</script>

<style scoped>
canvas {
  width: 100% !important; /* Make canvas scale with container */
  height: 100% !important;
  background-color: #181818;
}
</style>
