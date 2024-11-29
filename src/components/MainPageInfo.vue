<template>
  <div class="container">
    <div class="greetings">
      <h1 class="green">China's Coal Story: Powering Progress, Shaping the Future</h1>
      <p>
        China stands as one of the world's largest consumers of coal, a resource that has fueled its rapid economic growth and industrialization. However, this dependence comes with significant environmental and social costs. From air pollution and greenhouse gas emissions to habitat destruction and public health challenges, the impact of coal reaches far beyond the mines and power plants.
        This visualization tool unpacks the story of China’s coal usage—its scale, consequences, and the country's journey toward a more sustainable energy future. Explore interactive data on coal production, consumption trends, and environmental effects, alongside insights into China's efforts to balance energy demands with ecological responsibility.
      </p>
      <select v-model="selectedCountry" @change="updateGraph">
        <option value="China">China</option>
        <option value="United States">United States</option>
        <option value="India">India</option>
        <!-- These are the top 3 countries that use coal -->
      </select>
    </div>
    <div class="graph-container">
      <canvas id="coalConsumptionGraph" width="800" height="600"></canvas>
      <p class="source">Source: Our world in data</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

// Register the necessary components, including scales
Chart.register(...registerables);

defineProps({
  msg: {
    type: String,
    required: true,
  },
});

const selectedCountry = ref('China');
let chartInstance = null;

const updateGraph = async () => {
  try {
    const response = await fetch(`http://localhost:5000/coal_consumption?country=${selectedCountry.value}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Fetched data:', data);

    await nextTick(); // Wait for the DOM to update

    const ctx = document.getElementById('coalConsumptionGraph').getContext('2d');
    if (chartInstance) {
      chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.years,
        datasets: [{
          label: 'Coal Consumption',
          data: data.values,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            type: 'category',
            title: {
              display: true,
              text: 'Year'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Consumption'
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching or updating graph:', error);
  }
};

onMounted(() => {
  updateGraph();
});

watch(selectedCountry, updateGraph);
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column; /* Stack text above image */
  align-items: center; /* Center children horizontally */
  justify-content: center; /* Center children vertically */
  height: 100vh; /* Full viewport height */
  margin: 0 auto; /* Center container horizontally */
  margin-left: 65px; /* Add left margin to move it to the right */
  padding-left: 200px;
}

.greetings, .graph-container {
  width: 80%; /* Set a fixed width for both containers */
  padding: 0.6rem;
  box-sizing: border-box; /* Include padding in the element's total width and height */
  text-align: center; /* Center text */
}

.graph-container {
  display: flex;
  flex-direction: column; /* Stack image and source text */
  justify-content: center; /* Center the graph horizontally */
  align-items: center; /* Center the graph vertically */
  width: 600px;
}

canvas {
  max-width: 100%; /* Ensure the canvas scales with the container */
  height: auto; /* Maintain aspect ratio */
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
}

h3 {
  font-size: 1.2rem;
}

p {
  font-size: 1rem;
  margin-top: 1rem;
  text-align: justify;
}

.source {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #555;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
</style>