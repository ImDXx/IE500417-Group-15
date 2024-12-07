<template>
  <div class="wrapper">
    <div class="top-text-container">
      <h1>Welcome to the China Coal Emissions and Pollution Dashboard</h1>
      <p>This platform is your gateway to understanding the environmental impact of coal in China. Explore interactive visualizations and detailed data to uncover the role of coal in shaping China's emissions landscape:</p>
      <ul class="bullet-list">
        <li>CO₂ Emissions Over Time: Track China's coal-related emissions and observe trends over the years.</li>
        <li>Fuel-Type Analysis: Dive into the breakdown of emissions by coal and other energy sources.</li>
        <li>Per Capita Comparisons: See how China's coal emissions compare with other nations and their per capita impacts.</li>
        <li>Air Pollution Metrics: Analyze PM2.5 levels linked to coal usage and their effects on air quality.</li>
      </ul>
    </div>
  </div>
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
      <div class="button-group">
        <button
            v-for="country in ['India', 'United States', 'Brazil']"
            :key="country"
            :class="{ active: selectedCountry === country }"
            @click="selectedCountry = country"
        >
          {{ country }}
        </button>
      </div>
      <div class="button-group">
        <input
            type="range"
            min="1900"
            max="2020"
            step="1"
            v-model="tempYear"
            @input="debounceUpdateYear"
            class="slider"
        />
        <span>{{ selectedYear }}</span>
      </div>
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
      <button @click="redirectToPage2" class="see-more-button">See more</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import GraphComponent from './charts/GraphComponent.vue';
import RadarChart from './charts/RadarChart.vue';
import AirPollutionChart from './charts/AirPollutionChart.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selectedVisualization = ref('co2_emissions');
const selectedYear = ref(2020);
const selectedCountry = ref('India');

const tempYear = ref(2020);

const debounce = (func, delay) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
};

const updateYear = () => {
  selectedYear.value = tempYear.value;
};

const debounceUpdateYear = debounce(updateYear, 300);

const redirectToPage2 = () => {
  router.push('/page2');
};

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
  align-items: center;
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

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  justify-content: flex-end;
  margin-top: 10px;
}

.button-group button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-group button.active {
  background-color: #4caf50;
  color: #fff;
}

.button-group button:hover {
  background-color: #e0e0e0;
}

.see-more-button {
  margin-top: 20px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.see-more-button:hover {
  background-color: #45a049;
}

.top-text-container {
  text-align: start;
  margin: 0 auto;
}

.top-text-container h1 {
  color: green;
}

.bullet-list {
  list-style-position: inside;
  padding-left: 0;
}

.slider {
  width: 100%;
  margin: 10px 0;
}

.green {
  color: green;
}
</style>