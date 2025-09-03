<script setup lang="ts">

import type { IVideoCard } from '@/interfaces/VideoCard.interface.ts'

const { file_name, poster } = defineProps<IVideoCard>()

</script>

<template>
  <div class="video-card">
    <div class="video-card__image" :style="{ backgroundImage: `url(${poster})` }"></div>
    <div class="video-card__title">{{ file_name }}</div>
  </div>

</template>

<style scoped>
@media (max-width: 390px) {
.video-card {
  border-radius: 7px;
  max-width: 163px;
  background: var(--color-bg-card);
  padding: 5px;
}
.video-card__image {
  min-height: 230px;
  background-size: cover;
  background-repeat: no-repeat;
}}

@media (min-width: 768px) {
  .video-card {
    border-radius: 7px;
    max-width: 200px;
    background: var(--color-bg-card);
    padding: 5px;
  }

.video-card__image {
  min-height: 300px;
  background-size: cover;
  background-repeat: no-repeat;
}
}

.video-card__title {
  color: var(--color-text-card);
  font-size: 20px;
  text-align: center;
  overflow: hidden;
  border-radius: 7px;
  margin-top: 10px;
}

</style>
