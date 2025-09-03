<script setup lang="ts">

import ListButton from '@/components/ListButton.vue'
import IconAddFolder from '@/icons/IconAddFolder.vue'

const { path } = defineProps<{path: string}>()
const emit = defineEmits(['buttonClick'])

</script>

<template>
  <li class="list-item">
    <div class="list-container">
      <slot/>
      <list-button  @click="emit('buttonClick', path)"><IconAddFolder :size="30"/></list-button>
    </div>
  </li>
</template>

<style scoped>
.list-item {
  list-style-type: none;
  padding-left: 5px;
}
.list-item::marker {
  content: "\01F5C0";
  font-size: 25px;
}
.list-container  {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 25px;
  list-style-type: none;
  cursor: pointer;
}
</style>
