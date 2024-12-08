<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { Chart } from 'chart.js';


const props = defineProps({
  selectedDeaths: {
    type: String,
    required: true,
  },
  selectedFilter: {
    type: String,
    required: true,
  },
});


const chartCanvas = ref(null);
let chartInstance = null;


const fetchAirPollutionData = async (metric, filter) => {
  try {
    const response = await fetch(`http://localhost:5000/air_pollution_data?metric=${metric}&filter=${filter}`);;
    const data = await response.json();

    const years = Object.keys(data[Object.keys(data)[0]]); 
    const countries = Object.keys(data); 

    const datasets = countries.map((country) => {
      const pollutionLevels = years.map((year) => data[country][year]);
      return {
        label: country,
        data: pollutionLevels,
        backgroundColor: getRandomColor(), 
        borderColor: 'rgba(0, 0, 0, 0.1)',
        borderWidth: 1,
      };
    });

    return {
      labels: years,
      datasets,
    };
  } catch (error) {
    console.error('Error fetching air pollution data:', error);
    return {
      labels: [],
      datasets: [],
    };
  }
};

const getRandomColor = () => {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `rgba(${r}, ${g}, ${b}, 0.5)`;
};


const renderAirPollutionChart = async () => {
  const data = await fetchAirPollutionData(props.selectedDeaths, props.selectedFilter);

  await nextTick(); 

  if (!chartCanvas.value) {
    console.error("Canvas element not found.");
    return;
  }

  const ctx = chartCanvas.value.getContext('2d');

  if (chartInstance) {
    chartInstance.destroy(); 
  }

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: `Air Pollution Attributable Deaths (${props.selectedDeaths})`,
          color: '#FFFFFF',
        },
        legend: {
          display: true,
          labels: {
            color: '#FFFFFF',
          },
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const year = context.label;
              const pollution = context.raw.toFixed(2);
              return `${year}: ${pollution} deaths`;
            },
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Year',
            color: '#FFFFFF',
          },
          ticks: {
            color: '#FFFFFF',
          },
        },
        y: {
          title: {
            display: true,
            text: 'Deaths',
            color: '#FFFFFF',
          },
          ticks: {
            color: '#FFFFFF',
          },
          beginAtZero: true,
        },
      },
    },
  });
};

watch(
  () => [props.selectedDeaths, props.selectedFilter],
  async ([newMetric, newFilter]) => {
    const chartData = await fetchAirPollutionData(newMetric, newFilter);
    renderAirPollutionChart(chartData);  // Ensure this function updates the chart
  },
  { immediate: true }
);

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

onMounted(renderAirPollutionChart);
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 600px; 
}
</style>