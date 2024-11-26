<script setup>
import Graph from "@/components/Graph.vue";

defineProps({
  msg: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="container">
    <div class="greetings">
      <h1 class="green">{{ msg }}</h1>
      <p>
        ChinaCoal Lorem Ipsum: Coal mining and consumption have significant impacts on the environment. The extraction process can lead to deforestation, habitat destruction, and soil erosion. Burning coal releases pollutants such as sulfur dioxide, nitrogen oxides, and particulate matter, contributing to air pollution and respiratory problems. Additionally, coal combustion is a major source of carbon dioxide emissions, driving climate change and global warming. Efforts to mitigate these effects include transitioning to cleaner energy sources and implementing stricter environmental regulations.
      </p>
    </div>
    <div class="graph-container">
      <Graph />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  align-items: stretch; /* Ensure both children stretch to the same height */
}

.greetings {
  flex: 2; /* Increase the flex value to give more width */
  margin-right: 1rem;
}

.graph-container {
  flex: 1;
  padding-left: 1rem;
  display: flex;
  align-items: center; /* Center the graph vertically */
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

p {
  font-size: 1rem;
  margin-top: 1rem;
  text-align: justify;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>