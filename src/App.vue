<script setup>
import MainPageInfo from "@/components/MainPageInfo.vue";
</script>

<template>
  <header class="app-bar">
    <RouterLink to="/">
      <img alt="China coal logo" class="logo" src="./assets/ChinaCoal.svg" width="200" height="50" />
    </RouterLink>
    <div class="title"></div>
  </header>

  <main>
    <div class="wrapper">
      <MainPageInfo msg="China coal" />
    </div>
  </main>
</template>

<style scoped>
.app-bar {
  display: flex;
  align-items: center;
  justify-content: flex-start;
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

main {
  margin-top: 4rem; /* Adjust based on the height of the app bar */
}

.wrapper {
  padding: 1rem;
}
</style>