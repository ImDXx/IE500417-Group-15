<script setup>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const chartData = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'CO2 Emissions',
      backgroundColor: '#42A5F5',
      borderColor: '#42A5F5',
      data: [10, 20, 30, 40, 50, 60, 70]
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
/* Add any styles you need for your graph component */
</style>