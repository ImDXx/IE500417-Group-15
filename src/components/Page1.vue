<template>
  <div class="page1-container">
    <h1>Emissions Prediction</h1>
    <p>
      This chart compares actual deaths, predicted deaths, and reduced predicted deaths due to air pollution. 
      The predicted values are based on a machine learning model, and the reduced predicted deaths reflect a 
      scenario where emissions are reduced by 20%.
    </p>
    <p>
      By analyzing this chart, you can see the potential impact of reducing emissions on public health, 
      highlighting the importance of emission reduction policies.
    </p>
    <PredictionChart />
  </div>
</template>

<script setup>
import PredictionChart from './charts/PredictionChart.vue';
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

p {
  margin: 10px 0;
  font-size: 16px;
  color: #ffffff;
  max-width: 800px;
  line-height: 1.5;
}
</style>
