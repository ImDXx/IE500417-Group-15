<script setup>
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);


const source = "Source: Our World in Data";
// Example data, replace dynamically with props or API data
const chartData = {
  labels: ['1965', '1970', '1975', '1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2020'],
  datasets: [
    {
      label: 'Total CO₂ Emissions (Million Tonnes)',
      backgroundColor: '#42A5F5',
      borderColor: '#42A5F5',
      data: [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000],
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Total CO₂ Emissions Over Time', // Chart title
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Year', // X-axis label
      },
    },
    y: {
      title: {
        display: true,
        text: 'Million Tonnes of CO₂', // Y-axis label
      },
      ticks: {
        callback: (value) => `${value.toLocaleString()} MT`, // Format Y-axis values with units
      },
    },
  },
};
</script>

<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
/* Add any additional styles for your graph */
</style>
