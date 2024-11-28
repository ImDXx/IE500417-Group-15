<template>
  <div class="container">
    <div class="greetings">
      <h1 class="green">{{ msg }}</h1>
      <p>
        ChinaCoal Lorem Ipsum: Coal mining and consumption have significant impacts on the environment. The extraction process can lead to deforestation, habitat destruction, and soil erosion. Burning coal releases pollutants such as sulfur dioxide, nitrogen oxides, and particulate matter, contributing to air pollution and respiratory problems. Additionally, coal combustion is a major source of carbon dioxide emissions, driving climate change and global warming. Efforts to mitigate these effects include transitioning to cleaner energy sources and implementing stricter environmental regulations.
      </p>
      <select v-model="selectedCountry" @change="updateGraph">
        <option value="China">China</option>
        <option value="United States">United States</option>
        <option value="Russia">Russia</option>
        <!-- Add more countries as needed -->
      </select>
    </div>
    <div class="graph-container">
      <img :src="imageUrl" alt="Coal Consumption Graph" />
      <p class="source">Source: Our world in data</p>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue';

defineProps({
  msg: {
    type: String,
    required: true,
  },
});

const selectedCountry = ref('China');
const imageUrl = ref('');

const updateGraph = () => {
  imageUrl.value = `http://localhost:5000/coal_consumption?country=${selectedCountry.value}`;
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
}

.greetings, .graph-container {
  width: 80%; /* Set a fixed width for both containers */
  padding: 1rem;
  box-sizing: border-box; /* Include padding in the element's total width and height */
  text-align: center; /* Center text */
}

.graph-container {
  display: flex;
  flex-direction: column; /* Stack image and source text */
  justify-content: center; /* Center the graph horizontally */
  align-items: center; /* Center the graph vertically */
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