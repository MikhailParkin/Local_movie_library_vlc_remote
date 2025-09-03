<script setup lang="ts">

const { path } = defineProps<{path: string}>()
const emit = defineEmits(['pathButtonClick'])
</script>

<template>
  <li class="list-item" @click="emit('pathButtonClick', path)">
      <slot/>
  </li>
</template>

<style scoped>
.list-item {
  list-style-type: none;
  padding-left: 5px;
  cursor: pointer;
  font-size: 20px;
}
.list-item::marker {
  content: "\01F5C0";
  font-size: 25px;
}

</style>
