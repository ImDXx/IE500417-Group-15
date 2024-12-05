<template>
  <div class="page1-container">
    <h1>This is page 2</h1>
    <p>Oscar yeet a graph here please</p>
    <StackedBarChart />
  </div>
</template>

<script setup>
import StackedBarChart from './charts/StackedBarChart.vue';



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
</style>