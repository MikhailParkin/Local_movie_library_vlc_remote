<script setup lang="ts">
import ListButton from '@/components/ListButton.vue'
import IconAddRecord from '@/icons/IconAddRecord.vue'
import IconCheck from '@/icons/IconCheck.vue'

const { filename, file_id, kpinfo_id } = defineProps<{
  filename: string,
  file_id: number,
  kpinfo_id: number | null}>();

const emit = defineEmits(['clickRecord'])
</script>

<template>
  <div class="local-db-rec-container">
    <div class="check" v-if="kpinfo_id != null">
      <IconCheck :size="15"/>
    </div>
    <div class="local-db-record">
      <div class="local-db-name">
        {{filename}}
      </div>
      <div>
        <ListButton @click="emit('clickRecord', file_id)"><IconAddRecord :size="20"/></ListButton>
      </div>
    </div>


  </div>

</template>

<style scoped>
.local-db-rec-container {
  display: flex;
  flex-direction: row;
  background-color: var(--color-bg-card);
  max-width: 600px;
  align-items: center;
}
.check {
  margin-left: 10px;
}
.local-db-record {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
  align-items: center;
  overflow: hidden;


}
.local-db-name {
  font-size: 24px;
  overflow: hidden;
  cursor: pointer;
  padding: 0.5rem;
}
</style>
