<template>
  <div class="page1-container">
    <CoalVsAirPollution />
    <div class="text-container">This graph shows the relationship between CO2 emissions in China and Air Pollution deaths in China</div>
  </div>
</template>

<script setup>
import CoalVsAirPollution from './charts/CoalVsAirPollution.vue';



</script>

<style scoped>
.page1-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  margin: 0 auto;
  text-align: center; /* Center text horizontally */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.text-container {
  color: #ffffff;
  font-size: 20px;
  margin-top: 20px;
  max-width: 800px;
  line-height: 1.5;
  background-color: #181818;
}
</style>