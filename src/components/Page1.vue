<template>
  <div class="page1-container">
    <h1>This is page 1</h1>
    <p>Oscar yeet a graph here please</p>
    <CorrelationMatrix />
  </div>
</template>

<script setup>
import CorrelationMatrix from './charts/CorrelationMatrix.vue';



</script>

<style scoped>
.page1-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0 auto;
  text-align: center; /* Center text horizontally */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>