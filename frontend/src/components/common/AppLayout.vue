<template>
  <div class="layout-wrapper">
    <AppNavbar />
    <main class="layout-main" id="main-content">
      <slot />
    </main>
    <AppFooter />
    <!-- Global Toast Notifications -->
    <ToastContainer />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/common/AppNavbar.vue";
import AppFooter from "@/components/common/AppFooter.vue";
import ToastContainer from "@/components/ui/ToastContainer.vue";
</script>

<style scoped>
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.layout-main {
  flex: 1;
}
</style>
