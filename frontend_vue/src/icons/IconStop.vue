<script setup lang="ts">
const { size } = defineProps<{size: number}>()
</script>

<template>
  <svg :style="`width:${size}px; height:${size}px;`" x="0px" y="0px" viewBox="0 0 121.53 122.88" style="enable-background:new 0 0 121.53 122.88" xml:space="preserve">
  <g><polygon class="st0" points="0,0 121.53,0 121.53,122.88 0,122.88 0,0"/></g></svg>
</template>

<style scoped>
.st0 {
  fill-rule: evenodd;
  clip-rule: evenodd;
  color: var(--color-text-card);
  fill: var(--color-text-card);

}
</style>
