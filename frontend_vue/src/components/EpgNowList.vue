<script setup lang="ts">
import ListButton from '@/components/ListButton.vue'
import IconList from '@/icons/IconList.vue'

const emit = defineEmits(['clickEpgButton'])
const {channel_id } = defineProps<{channel_id: string}>()

</script>

<template>

    <div class="channel-epg">
      <slot />
      <div>
        <ListButton @click="emit('clickEpgButton', channel_id)"><IconList :size="20"/></ListButton>
      </div>
    </div>

</template>

<style scoped>
.channel-epg {
  display: flex;
  flex-direction: row;
  overflow: hidden;
  list-style: none;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-card);
  font-size: 22px;
  border-bottom: 2px solid var(--color-text-card);
}
</style>
