<script setup lang="ts">
import type { IBackUp } from '@/interfaces/Backup.interface.ts'
import ListButton from '@/components/ListButton.vue'
import IconRestore from '@/icons/IconRestore.vue'

const {backups} = defineProps<{backups: IBackUp[]}>()
const emit = defineEmits(['backupClick'])
</script>

<template>

  <div v-for="item in backups" :key="item.id">
    <div class="backup-record">
      {{item.file_name}}
      <ListButton @click="emit('backupClick', 'restore', item.id)"><IconRestore :size="15"/></ListButton>
    </div>
  </div>

</template>

<style scoped>
.backup-record {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  align-content: center;
  font-size: 20px;
  width: 90%;
  max-width: 500px;
  margin-left: 15px;
  margin-top: 10px;
}
</style>
