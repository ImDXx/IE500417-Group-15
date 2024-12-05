<script setup>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

import { ref, onMounted } from 'vue';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = ref(null);
const source = "Source: Our World in Data";
const chartOptions = {
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: 'Top Features Affecting Coal CO₂ Emissions',
    },
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Feature',
      },
    },
    y: {
      title: {
        display: true,
        text: 'Importance Score',
      },
    },
  },
};

const fetchFeatureImportance = async () => {
  try {
    const response = await fetch('http://localhost:5000/feature_importance');
    const data = await response.json();

    chartData.value = {
      labels: data.map((item) => item.Feature),
      datasets: [
        {
          label: 'Feature Importance',
          data: data.map((item) => item.Importance),
          backgroundColor: '#42A5F5',
        },
      ],
    };
  } catch (error) {
    console.error('Error fetching feature importance:', error);
  }
};

onMounted(fetchFeatureImportance);
</script>

<template>
  <div>
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    <p v-else>Loading...</p>
  </div>
</template>

<style scoped>
/* Add any custom styles here */
</style>
