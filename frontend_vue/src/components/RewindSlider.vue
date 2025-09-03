<script setup lang="ts">
import { computed, ref, watch } from 'vue'


const { seconds, max } = defineProps<{seconds: number, max: number}>();
const sliderValue = ref(seconds);
const emit = defineEmits(['change'])

const formattedTime = computed(() => {
  const hours = Math.floor(sliderValue.value / 3600);
  const minutes = Math.floor((sliderValue.value % 3600) / 60);
  const remainingSeconds = sliderValue.value % 60;

  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
});

function handleChange() {
  emit('change', sliderValue.value);
}

watch(
  () => seconds,
  (newVal) => {
    sliderValue.value = newVal;
  }
);

</script>

<template>

  <div class="show-time">
    <h3>{{ formattedTime }}</h3>
  </div>
  <div class="slide-container">
    <input class="slider" type="range" v-model="sliderValue" :max="max" step="1" @change="handleChange"/>
  </div>
</template>

<style scoped>
.show-time {
  text-align: center;
}
.slide-container {
  width: 100%;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 15px;
  border-radius: 5px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 35px;
  border-radius: 10px;
  background: var(--color-bg-card);
  cursor: pointer;
  border: 2px solid var(--color-text-card);
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 35px;
  border-radius: 10px;
  background: var(--color-bg-card);
  cursor: pointer;
  border: 2px solid var(--color-text-card);
}
</style>
