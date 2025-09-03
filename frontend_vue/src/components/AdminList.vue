<script setup lang="ts">
import { onMounted, ref } from 'vue'

const buttonsPath = {
  "Library": "/admin/library",
  "LocalDB": '/admin/db',
  "Kinopoisk": "/admin/kinopoisk",
  "BackUp": '/admin/backups',
}
const selectValue = ref(buttonsPath["Library"] as string);
const emit = defineEmits(['change']);

onMounted(() => {
  emit('change', selectValue.value);
});

function handleChange() {
  emit('change', selectValue.value);
}

</script>

<template>
  <select class="admin-tab-select" v-model="selectValue" @change="handleChange">
    <option
      v-for="(value, key) in buttonsPath"
      :key="value"
      :value="value"
      v-text="key"
    ></option>
  </select>
</template>

<style scoped>
.admin-tab-select {
  width: 100%;
  padding: 10px;
  border: 3px solid var(--color-text-card);
  border-radius: 5px;
  font-size: 30px;
  color: var(--color-text-card);
  background-color: var(--color-bg-card);
}
</style>
