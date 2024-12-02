<template>
  <div class="graph-container">
    <canvas ref="chartCanvas" width="800" height="600"></canvas>
    <p class="source">Source: Our World in Data</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

// Props for dynamic data and options
const props = defineProps({
  endpoint: {
    type: String,
    required: true,
  },
  selectedCountry: {
    type: String,
    required: true,
  },
  fields: {
    type: Array,
    required: true,
  },
  labels: {
    type: Array,
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

// Chart instance
let chartInstance = null;
const chartCanvas = ref(null);

// Fetch data from the server
const fetchData = async (endpoint, country) => {
  try {
    const response = await fetch(`http://localhost:5000/${endpoint}?country=${country}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

// Render chart dynamically
const renderGraph = async () => {
  const data = await fetchData(props.endpoint, props.selectedCountry);
  if (!data) return;

  await nextTick(); // Ensure canvas is ready

  const ctx = chartCanvas.value.getContext('2d');
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.years,
      datasets: props.fields.map((field, index) => ({
        label: props.labels[index],
        data: data[field],
        borderColor: `hsl(${index * 120}, 70%, 50%)`,
        borderWidth: 2,
        fill: false,
      })),
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
      },
      scales: {
        x: {
          title: {
            display: true,
            text: props.xAxisLabel,
          },
        },
        y: {
          title: {
            display: true,
            text: props.yAxisLabel,
          },
          ticks: {
            callback: (value) => value.toLocaleString(),
          },
        },
      },
    },
  });
};

// Watch for changes in props
watch([() => props.selectedCountry, () => props.endpoint], renderGraph, { immediate: true });

onMounted(renderGraph);
</script>

<style scoped>
.graph-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

canvas {
  max-width: 100%;
  height: auto;
}

.source {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #555;
}
</style>
