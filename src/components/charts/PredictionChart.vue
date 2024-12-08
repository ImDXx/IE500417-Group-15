<template>
    <div>
      <h2>Comparison of Actual, Predicted, and Reduced Predicted Deaths</h2>
      <!-- Chart Container -->
      <div class="chart-container">
        <!-- Render chart only when chartData is not null -->
        <BarChart v-if="chartData" :data="chartData" :options="chartOptions" />
        <p v-else>Loading chart data...</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { Bar } from "vue-chartjs";
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
  } from "chart.js";
  
  // Register Chart.js components
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
  
  export default {
    name: "PredictionChart",
    components: {
      BarChart: Bar, // Correctly register the Bar component as BarChart
    },
    setup() {
      const chartData = ref(null); // Initialize chartData as null
      const chartOptions = ref({
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          tooltip: {
            enabled: true,
          },
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "Deaths",
            },
          },
          x: {
            title: {
              display: true,
              text: "Category",
            },
          },
        },
      });
  
      const fetchChartData = async () => {
        try {
          const response = await fetch("http://localhost:5000/chart_data");
          const data = await response.json();
  
          if (data.error) {
            throw new Error(data.error);
          }
  
          // Populate chartData with fetched API response
          chartData.value = {
            labels: data.labels,
            datasets: [
              {
                label: "Deaths",
                backgroundColor: ["blue", "orange", "green"],
                data: data.values,
              },
            ],
          };
        } catch (error) {
          console.error("Error fetching chart data:", error);
        }
      };
  
      onMounted(fetchChartData);
  
      return {
        chartData,
        chartOptions,
      };
    },
  };
  </script>
  
  <style scoped>
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .chart-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    position: relative;
  }
  </style>
  