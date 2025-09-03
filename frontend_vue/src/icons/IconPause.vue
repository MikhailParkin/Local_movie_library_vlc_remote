<script setup lang="ts">
const { size } = defineProps<{size: number}>()
</script>

<template>
 <svg :style="`width:${size}px; height:${size}px;`" x="0px" y="0px" viewBox="0 0 87.72 122.88" style="enable-background:new 0 0 87.72 122.88" xml:space="preserve">
   <g><path class="st0" d="M0,0h35.54v122.88l-35.54,0V0L0,0z M52.18,0h35.54v122.88l-35.54,0V0L52.18,0z"/></g></svg>
</template>

<style scoped>
.st0 {
  fill-rule:evenodd;clip-rule:evenodd;
  color: var(--color-text-card);
  fill: var(--color-text-card);
}
</style>
