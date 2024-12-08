<template>
    <div class="chart-page">
      <StackedBarChart />
    </div>
  </template>
  
  <script setup>
  import StackedBarChart from './charts/StackedBarChart.vue';
  </script>
  
  <style scoped>
  .chart-page {
    width: 90vw; /* Full width of the viewport */
    height: 89vh; /* Subtract the height of the navigation bar (adjust height as needed) */
    display: flex;
    justify-content: center; /* Center the chart horizontally */
    align-items: center; /* Center the chart vertically */
    box-sizing: border-box;
    padding: 0; /* Remove padding */
    margin: 0; /* Remove margin */
  }
  </style>
  