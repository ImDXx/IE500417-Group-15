<template>
  <div class="wrapper">
    <div class="flex-container">
      <div class="chart-container">
        <GraphComponent
            :endpoint="'multi_country_data'"
            :type="selectedVisualization"
            :xAxisLabel="'Year'"
            :yAxisLabel="yAxisLabel"
            :chartTitle="chartTitle"
        />
      </div>
      <div class="text-container">
        <h1 class="green">Global CO₂ Emissions</h1>
        <p>
          Compare CO₂ emissions across China, India, and the United States to see trends and differences.
        </p>
        <select v-model="selectedVisualization">
          <option value="co2_emissions">CO₂ Emissions Over Time</option>
          <option value="fuel_emissions">CO₂ Emissions by Fuel Type</option>
          <option value="gdp_vs_co2">GDP vs. CO₂ Emissions</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import GraphComponent from './charts/GraphComponent.vue';

const selectedVisualization = ref('co2_emissions');

const yAxisLabel = computed(() => {
  switch (selectedVisualization.value) {
    case 'co2_emissions':
      return 'CO₂ Emissions (TWh)';
    case 'fuel_emissions':
      return 'CO₂ Emissions by Fuel Type (TWh)';
    case 'gdp_vs_co2':
      return 'GDP / CO₂ Emissions';
    default:
      return 'Value';
  }
});

const chartTitle = computed(() => {
  switch (selectedVisualization.value) {
    case 'co2_emissions':
      return 'CO₂ Emissions Over Time';
    case 'fuel_emissions':
      return 'CO₂ Emissions by Fuel Type';
    case 'gdp_vs_co2':
      return 'GDP vs. CO₂ Emissions';
    default:
      return 'Dynamic Graph';
  }
});
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 50vh;
  box-sizing: border-box;
}

.flex-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: stretch;
  width: 80vw;
  height: 50vh;
  box-sizing: border-box;
  margin: auto;
}

.chart-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.text-container {
  flex: 1;
  padding: 20px;
}

.green {
  color: green;
}
</style>