<script setup lang="ts">
const { size } = defineProps<{size: number}>()
</script>

<template>
<svg  class="back-arrow"  :style="`width:${size}px; height:${size}px;`" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" viewBox="0 0 298 511.93"><path fill-rule="nonzero" d="M285.77 441c16.24 16.17 16.32 42.46.15 58.7-16.16 16.24-42.45 16.32-58.69.16l-215-214.47c-16.24-16.16-16.32-42.45-.15-58.69L227.23 12.08c16.24-16.17 42.53-16.09 58.69.15 16.17 16.24 16.09 42.54-.15 58.7l-185.5 185.04L285.77 441z"/></svg>
</template>

<style scoped>
.back-arrow {
  position: absolute;
  top: 30px;
  right: 30px;
  color: var(--color-text-card);
  fill: var(--color-text-card);
  cursor: pointer;
  z-index: 5;
}
</style>
