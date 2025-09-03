<script setup lang="ts">

import ListButton from '@/components/ListButton.vue'
import IconSettings from '@/icons/IconSettings.vue'

const {rec_name, rec_number} = defineProps<{rec_name: string, rec_number: number}>()
const emit = defineEmits(['clickSetting'])
</script>

<template>
<div class="record-container">
  <div class="record-name">
    {{rec_name}}
  </div>
  <div>
    <ListButton @click="emit('clickSetting', rec_number)"><IconSettings :size="30"/></ListButton>
  </div>
</div>
</template>

<style scoped>
.record-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 10px;
}
.record-name {
  font-size: 24px;
  overflow: hidden;
  margin-left: 10px;
  align-items: center;
  align-content: center;

}
</style>
