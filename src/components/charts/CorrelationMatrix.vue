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
      text: 'Top and Bottom 10 Correlations with Coal CO₂ Emissions',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const featureName = context.label; // Feature name
          const correlation = context.raw.toFixed(2); // Correlation value
          return `${featureName}: Correlation = ${correlation}`;
        },
      },
    },
    legend: {
      display: false, // We don't need a legend
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Features',
      },
      ticks: {
        autoSkip: false, // Do not skip labels
        maxRotation: 45, // Rotate labels
        minRotation: 45,
      },
    },
    y: {
      title: {
        display: true,
        text: 'Correlation Coefficient',
      },
      min: -1, // Range of correlation coefficients
      max: 1,
    },
  },
};

const fetchCorrelationMatrix = async () => {
  try {
    // Fetch data from the Flask API
    const response = await fetch('http://localhost:5000/correlation_matrix');
    const data = await response.json();

    // Prepare data for Chart.js
    chartData.value = {
      labels: data.map((item) => item.Feature), // Features on x-axis
      datasets: [
        {
          label: 'Correlation',
          data: data.map((item) => item.Correlation), // Correlation values
          backgroundColor: data.map((item) =>
            item.Correlation > 0
              ? `rgba(0, 128, 0, ${Math.abs(item.Correlation)})` // Green for positive
              : `rgba(255, 0, 0, ${Math.abs(item.Correlation)})` // Red for negative
          ),
          borderColor: 'rgba(0, 0, 0, 0.1)',
          borderWidth: 1,
        },
      ],
    };
  } catch (error) {
    console.error('Error fetching correlation matrix:', error);
  }
};

onMounted(fetchCorrelationMatrix);
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
