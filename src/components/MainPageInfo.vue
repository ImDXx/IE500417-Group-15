<template>
  <div class="container">
    <div class="greetings">
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
    <GraphComponent
      :endpoint="'multi_country_data'"
      :type="selectedVisualization"
      :xAxisLabel="'Year'"
      :yAxisLabel="yAxisLabel"
      :chartTitle="chartTitle"
    />
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
