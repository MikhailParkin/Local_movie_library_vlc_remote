<script setup lang="ts">
</script>

<template>
  <button class="menu-button"><slot></slot></button>
</template>

<style scoped>
.menu-button {
  max-width: 45px;
  max-height: 45px;
  cursor: pointer;
  text-align: center;
  justify-content: center;
  background-color: var(--color-bg-card);
  border-radius: 5px;
  border: 2px solid var(--color-text-card);
  color: var(--color-text-card);
  font-size: 20px;
  font-weight: bold;
  padding: 5px;
}
</style>
