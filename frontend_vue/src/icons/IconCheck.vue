<script setup lang="ts">
const { size } = defineProps<{size: number}>()
</script>

<template>

  <svg class="check-icon" :style="`width:${size}px; height:${size}px;`" x="0px" y="0px" viewBox="0 0 122.88 109.76" xml:space="preserve">
    <g><path class="st0" d="M0,52.88l22.68-0.3c8.76,5.05,16.6,11.59,23.35,19.86C63.49,43.49,83.55,19.77,105.6,0h17.28 C92.05,34.25,66.89,70.92,46.77,109.76C36.01,86.69,20.96,67.27,0,52.88L0,52.88z"/></g></svg>

</template>

<style scoped>
.check-icon {
  fill-rule: evenodd;
  clip-rule: evenodd;
  fill: #42b883;
}
</style>
