<script setup lang="ts">

const { start, end, title, epg_url } = defineProps<{start: string, end: string, title: string, epg_url: string}>()
const emit = defineEmits(['clickEpgHistory'])

const getProgramStatus = () => {
  const now = new Date();
  const startTime = new Date(start);
  const endTime = new Date(end);

  if (now > endTime) return 'past';
  if (now >= startTime && now <= endTime) return 'current';
  return 'future';
};


function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    month: '2-digit',
    day: '2-digit',
    weekday: 'short'
  });
}
function formatTime(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}
</script>

<template>
<div class="epg-channel"
     :class="getProgramStatus()"
     @click="emit('clickEpgHistory', epg_url)"
     ref="programStatus">
  <div class="epg-date">
    {{formatDate(start)}}  {{formatTime(start)}}
  </div>
  <div class="epg-channel-title">
    {{title}}
  </div>
</div>
</template>

<style scoped>
.epg-channel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  cursor: pointer;
}
.epg-channel.past {
  color: var(--color-text-card);
}

.epg-channel.current {
  border-left-color: var(--color-border-left-color); /* Зеленая полоса для текущей программы */
  font-weight: bold;
  color: var(--color-border-left-color);
}

.epg-channel.future {
  color: var(--color-past-programm);
}

.epg-date {
  margin-top: 25px;
  margin-bottom: 5px;
  font-size: 18px;
}
.epg-channel-title {
  font-size: 25px;
}
</style>
