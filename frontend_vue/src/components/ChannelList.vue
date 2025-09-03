<script setup lang="ts">

const { channelNumber, channelImg, channelName, channel_url } = defineProps<{channelNumber: number, channelImg: string, tvgID: string, channelName: string, channel_url: string}>();
const emit = defineEmits(['clickChannel'])
</script>

<template>
  <div class="channel-list">
      <div class="channel-name" @click="emit('clickChannel', channel_url)">
        {{ channelNumber }}
        <img class="channel-logo" :src="channelImg" alt="Channel Icon">
        {{ channelName }}
      </div>
  </div>
</template>

<style scoped>
.channel-name {
  font-size: 24px;
  cursor: pointer;
  background: var(--color-bg-card-header);
}
.channel-logo {
  height: 50px;
  width: 70px;
  max-height: 70px;
  max-width: 70px;
}
</style>
