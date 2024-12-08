<script setup>
</script>

<template>
  <div class="about-container">
    <h1>About Us</h1>
    <p>
      This project is part of the IE500417 course at NTNU, focusing on data visualization and machine learning.
    </p>
    <p>
      Our target user is <strong>China Coal</strong>, and we aim to provide a specialized visualization platform tailored to their needs. 
      Using datasets from the <strong>World Health Organization (WHO)</strong> and <strong>Our World in Data</strong>, 
      we have created various visualizations to present insights into emissions and their health impacts.
    </p>
    <p>
      The project includes interactive visualizations that highlight key metrics and patterns related to emissions, 
      such as the contribution of different fuels to CO₂ levels and their corresponding impact on public health. 
      Additionally, we have employed machine learning techniques to predict how a 20% reduction in emissions 
      could potentially decrease the number of deaths attributable to air pollution.
    </p>
    <p>
      Our goal is to combine data-driven insights with user-friendly visualizations to empower decision-making 
      and promote better environmental practices.
    </p>
  </div>
</template>

<style scoped>
.about-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 600px; /* Restrict width for readability */
  padding: 20px;
  margin: 0 auto;
  border-radius: 10px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #181818;
  color: #ffffff; /* Ensure text contrast */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Add a subtle shadow for aesthetics */
}

h1 {
  margin-bottom: 20px;
}

p {
  margin-bottom: 15px;
  line-height: 1.6; /* Improve readability */
}

strong {
  color: #ff9800; /* Highlight key text */
}
</style>
