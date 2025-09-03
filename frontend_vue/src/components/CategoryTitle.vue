<script setup lang="ts">

import IconRefresh from '@/icons/IconRefresh.vue'
import IconAddFolder from '@/icons/IconAddFolder.vue'
import ListButton from '@/components/ListButton.vue'

const { service } = defineProps<{service: string | number}>()
const emit = defineEmits(['buttonClick'])


</script>

<template>
<div class="title-container">
  <h1 class="category-title"><slot /></h1>
  <div class="button-container">
    <ListButton @click="emit('buttonClick', 'add', service)"><IconAddFolder :size="30"/></ListButton>
    <ListButton @click="emit('buttonClick', 'refresh', service)"><IconRefresh :size="30"/></ListButton>
  </div>

</div>


</template>

<style scoped>
.title-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.button-container {
  display: flex;
  flex-direction: row;
  flex-wrap: inherit;
  gap: 20px;
}
.category-title {
  align-items: center;
  font-size: 28px;
  color: var(--color-text-card);
}
</style>
