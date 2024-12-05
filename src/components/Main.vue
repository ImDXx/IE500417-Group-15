<template>
  <div class="wrapper">
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
      <select v-model="selectedVisualization" class="dropdown-menu">
        <option value="co2_emissions">CO₂ Emissions Over Time</option>
        <option value="fuel_emissions">CO₂ Emissions by Fuel Type</option>
        <option value="gdp_vs_co2">GDP vs. CO₂ Emissions</option>
      </select>
    </div>
  </div>
  <div class="second-wrapper">
    <div class="chart-container">
      <RadarChart :selectedYear="selectedYear" :selectedCountry="selectedCountry" />
    </div>
    <div class="text-container">
      <h1 class="green">Radar Chart</h1>
      <p>
        Compare per capita greenhouse gas emissions between China and another country.
      </p>
      <select v-model="selectedCountry" class="dropdown-menu">
        <option value="India">India</option>
        <option value="United States">United States</option>
        <option value="Brazil">Brazil</option>
      </select>
      <select v-model="selectedYear" class="dropdown-menu">
        <option value="2020">2020</option>
        <option value="2019">2019</option>
        <option value="2018">2018</option>
      </select>
    </div>
  </div>
  <div class="third-wrapper">
    <div class="chart-container">
      <AirPollutionChart />
    </div>
    <div class="text-container">
      <h1 class="green">Air Pollution Levels</h1>
      <p>
        Compare PM2.5 levels across different countries over the years.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import GraphComponent from './charts/GraphComponent.vue';
import RadarChart from './charts/RadarChart.vue';
import AirPollutionChart from './charts/AirPollutionChart.vue';

const selectedVisualization = ref('co2_emissions');
const selectedYear = ref(2020);
const selectedCountry = ref('India');

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
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.wrapper, .second-wrapper, .third-wrapper {
  display: flex;
  justify-content: start;
  align-items: stretch;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  border-radius: 50px;
  background-color: #181818;
  margin-bottom: 30px;
  margin-top: 30px;
  opacity: 0;
  padding: 50px 20px;
  animation: fadeIn 1s forwards;
}

.wrapper.visible, .second-wrapper.visible, .third-wrapper.visible {
  opacity: 1;
}

.chart-container {
  flex: 0 0 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.text-container {
  flex: 0 0 30%;
  padding: 20px;
  text-align: right;
}

.dropdown-menu {
  position: relative;
  display: inline-block;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.dropdown-menu option {
  position: absolute;
}

.dropdown-menu select:hover {
  background-color: #e0e0e0;
  color: #333;
}

.dropdown-menu option:hover {
  background-color: #e0e0e0;
  color: #333;
}

.dropdown-menu:hover {
  background-color: #f0f0f0;
}


.green {
  color: green;
}
</style>