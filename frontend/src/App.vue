<template>
  <!-- App root: 공통 헤더를 추가하고 페이지를 렌더링합니다. -->
  <Header />
  <router-view />
</template>

<script setup>
import Header from "./components/Header.vue";
</script>
