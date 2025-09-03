<script setup lang="ts">

const { name, rec_id } = defineProps<{name: string, rec_id: number}>();
const emit = defineEmits(['clickKpRecord'])
</script>

<template>
  <div class="local-db-record">
    <div class="local-db-name" @click="emit('clickKpRecord', rec_id)">
      {{name}}
    </div>
  </div>

</template>

<style scoped>
.local-db-record {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  max-width: 600px;
  align-content: center;
  align-items: center;
  margin-top: 15px;
}
.local-db-name {
  font-size: 24px;
  overflow: hidden;
  cursor: pointer;
}
</style>
