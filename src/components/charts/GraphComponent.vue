<template>
  <div class="graph-container">
    <canvas ref="chartCanvas" width="1500" height="800"></canvas>
    <p class="source">Source: Our World in Data</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(...registerables, zoomPlugin);

const source = "Source: Our World in Data";

// Props for dynamic data
const props = defineProps({
  endpoint: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  xAxisLabel: {
    type: String,
    default: 'Year',
  },
  yAxisLabel: {
    type: String,
    default: 'Value',
  },
  chartTitle: {
    type: String,
    default: 'Dynamic Graph',
  },
});

let chartInstance = null;
const chartCanvas = ref(null);

const fetchData = async (endpoint, type) => {
  try {
    const response = await fetch(`http://localhost:5000/${endpoint}?type=${type}`);
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

const renderGraph = async () => {
  const data = await fetchData(props.endpoint, props.type);
  if (!data) return;

  await nextTick();

  const ctx = chartCanvas.value.getContext('2d');
  if (chartInstance) chartInstance.destroy();

  const datasets = [];
  if (props.type === 'fuel_emissions') {
    Object.keys(data).forEach((country, index) => {
      ['coal', 'oil', 'gas'].forEach((fuelType) => {
        datasets.push({
          label: `${country} (${fuelType})`,
          data: data[country][fuelType] || [],
          borderColor: `hsl(${index * 360 / Object.keys(data).length + (fuelType === 'coal' ? 0 : fuelType === 'oil' ? 120 : 240)}, 70%, 50%)`,
          borderWidth: 2,
          fill: false,
        });
      });
    });
  } else if (props.type === 'gdp_vs_co2') {
    Object.keys(data).forEach((country, index) => {
      datasets.push({
        label: `${country} GDP`,
        data: data[country].gdp || [],
        borderColor: `hsl(${index * 360 / Object.keys(data).length}, 70%, 50%)`,
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
      });
      datasets.push({
        label: `${country} CO₂`,
        data: data[country].co2 || [],
        borderColor: `hsl(${index * 360 / Object.keys(data).length}, 70%, 30%)`,
        borderWidth: 2,
        fill: false,
      });
    });
  } else {
    Object.keys(data).forEach((country, index) => {
      datasets.push({
        label: country,
        data: data[country].values || [],
        borderColor: `hsl(${index * 360 / Object.keys(data).length}, 70%, 50%)`,
        borderWidth: 2,
        fill: false,
      });
    });
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data[Object.keys(data)[0]].years,
      datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: props.chartTitle,
        },
        legend: {
          position: 'top',
        },
        zoom: {
          pan: { enabled: true, mode: 'x' },
          zoom: {
            wheel: { enabled: true },
            pinch: { enabled: true },
            mode: 'x',
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: props.xAxisLabel,
            color: 'rgba(255, 255, 255, 0.8)', // Semi-transparent text
          },
          ticks: { color: 'rgba(255, 255, 255, 0.6)' },
          grid: {
            color: 'rgba(255, 255, 255, 0.2)', // Transparent gridlines
            borderColor: 'rgba(255, 255, 255, 0.3)', // Transparent border
          },
        },
        y: {
          title: {
            display: true,
            text: props.yAxisLabel,
            color: 'rgba(255, 255, 255, 0.8)', // Semi-transparent text
          },
          ticks: { color: 'rgba(255, 255, 255, 0.6)' },
          grid: {
            color: 'rgba(255, 255, 255, 0.2)', // Transparent gridlines
            borderColor: 'rgba(255, 255, 255, 0.3)', // Transparent border
          },
        },
      },
    },
  });
};

watch(() => props.type, renderGraph, { immediate: true });
onMounted(renderGraph);
</script>

<style scoped>
.graph-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
}

canvas {
  max-width: 100%;
  height: 100%;
  background-color: #181818;
}

.source {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #aaa;
}
</style>
