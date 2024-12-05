<template>
  <div class="page1-container">
    <h1>This is page 1</h1>
    <p>Select a year and a country to compare with China:</p>
    <div class="dropdowns">
      <div>
        <label for="year-select">Select Year:</label>
        <select id="year-select" v-model="selectedYear">
          <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>
      <div>
        <label for="country-select">Compare with:</label>
        <select id="country-select" v-model="selectedCountry">
          <option value="United States">United States</option>
          <option value="India">India</option>
          <option value="Russia">Russia</option>
          <option value="Japan">Japan</option>
        </select>
      </div>
    </div>
    <RadarChart :selectedYear="selectedYear" :selectedCountry="selectedCountry" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import RadarChart from './charts/RadarChart.vue';

const availableYears = ref([]);
const selectedYear = ref(2020);
const selectedCountry = ref('United States');

// Fetch available years from the backend
const fetchAvailableYears = async () => {
  const response = await fetch('http://localhost:5000/available_years');
  availableYears.value = await response.json();
};

onMounted(fetchAvailableYears);
</script>

<style scoped>
.page1-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
  background-color: #181818;
}

.dropdowns {
  display: flex;
  flex-direction: row;
  gap: 20px;
  margin-bottom: 20px;
}

label {
  margin-right: 10px;
}

select {
  padding: 10px;
  font-size: 1rem;
}
</style>
