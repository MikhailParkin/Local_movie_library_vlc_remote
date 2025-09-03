<script setup lang="ts">
</script>

<template>
<button class="menu-button"><slot></slot></button>
</template>

<style scoped>
.menu-button {
  width: 100%;
  cursor: pointer;
  text-align: center;
  justify-content: center;
  background-color: var(--color-bg-card);
  border-radius: 5px;
  border: 2px solid var(--color-text-card);
  color: var(--color-text-card);
  font-size: 20px;
  font-weight: bold;
  padding: 20px;
}
</style>
