<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header class="app-bar">
    <RouterLink to="/">
      <img alt="China coal logo" class="logo" src="./assets/ChinaCoal.svg" width="200" height="50" />
    </RouterLink>
    <div class="title"></div>
    <nav class="nav-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About us</RouterLink>
    </nav>
  </header>

  <main>
    <div class="wrapper">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>
.app-bar {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Space between logo and nav links */
  background-color: White;
  color: Black;
  padding: 0.5rem 1rem;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.logo {
  height: 50px;
}

.title {
  font-size: 1.5rem;
  margin-left: 1rem;
}

.nav-links {
  display: flex;
  gap: 1rem; /* Space between links */
  text-decoration: #181818;
}

main {
  margin-top: 4rem; /* Adjust based on the height of the app bar */
}

.wrapper {
  padding: 1rem;
}

.router-link {
  text-decoration: black;
  text-decoration: none;
}

.router-link-active {
  font-weight: bold;
}
</style>