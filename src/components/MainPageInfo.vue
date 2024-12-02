<template>
  <div class="container">
    <div class="greetings">
      <h1 class="green">China's Coal Story: Powering Progress, Shaping the Future</h1>
      <p>
        China stands as one of the world's largest consumers of coal, a resource that has fueled its rapid economic
        growth and industrialization. However, this dependence comes with significant environmental and social costs.
      </p>
      <select v-model="selectedVisualization">
        <option value="co2_emissions">CO₂ Emissions Over Time</option>
        <option value="fuel_emissions">CO₂ Emissions by Fuel Type</option>
        <option value="gdp_vs_co2">GDP vs. CO₂ Emissions</option>
      </select>
      <select v-model="selectedCountry">
        <option value="China">China</option>
        <option value="United States">United States</option>
        <option value="India">India</option>
      </select>
    </div>

    <GraphComponent
      v-if="selectedVisualization === 'co2_emissions'"
      :endpoint="'co2_emissions'"
      :selectedCountry="selectedCountry"
      :fields="['total_emissions', 'per_capita_emissions']"
      :labels="['Total Emissions', 'Per Capita Emissions']"
      xAxisLabel="Year"
      yAxisLabel="CO₂ Emissions (Million Tonnes)"
      chartTitle="CO₂ Emissions Over Time"
    />

    <GraphComponent
      v-if="selectedVisualization === 'fuel_emissions'"
      :endpoint="'fuel_emissions'"
      :selectedCountry="selectedCountry"
      :fields="['coal', 'oil', 'gas']"
      :labels="['Coal', 'Oil', 'Gas']"
      xAxisLabel="Year"
      yAxisLabel="CO₂ Emissions (Million Tonnes)"
      chartTitle="CO₂ Emissions by Fuel Type"
    />

    <GraphComponent
      v-if="selectedVisualization === 'gdp_vs_co2'"
      :endpoint="'gdp_vs_co2'"
      :selectedCountry="selectedCountry"
      :fields="['gdp', 'co2']"
      :labels="['GDP', 'CO₂ Emissions']"
      xAxisLabel="Year"
      yAxisLabel="GDP / CO₂ Emissions"
      chartTitle="GDP vs. CO₂ Emissions"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import GraphComponent from './GraphComponent.vue';

const selectedVisualization = ref('co2_emissions');
const selectedCountry = ref('China');
</script>

<style scoped>
/* Style as needed */
</style>
