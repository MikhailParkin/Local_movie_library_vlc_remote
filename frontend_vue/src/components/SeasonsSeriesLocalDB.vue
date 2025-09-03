<script setup lang="ts">

import { computed, reactive, ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { ISeasons } from '@/interfaces/Seasons.interface.ts'

const props = defineProps<{
  seasons: ISeasons[]
}>()

const isForm = ref<boolean>(false);
const formData = reactive({
  name: '',
  type: '', // 'season' или 'episode'
  id: 0,
  originalName: '' // для отслеживания изменений
});

const changedFields = ref<Record<string, boolean>>({});
const selectedFile = ref<File | null>(null);
const hasChanges = computed(() => {
  return Object.values(changedFields.value).some(value => value) || selectedFile.value !== null
})

const updateData = (typeRecord: string, recordId: number, name: string) => {
  formData.type = typeRecord;
  formData.id = recordId;
  formData.name = name;
  formData.originalName = name;

  // Сбрасываем флаги изменений
  changedFields.value = {};
  selectedFile.value = null;

  toggleForm();
}

function markAsChanged(fieldKey: string) {
  changedFields.value[fieldKey] = true;
}

function toggleForm() {
  isForm.value = !isForm.value;
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0];
    markAsChanged('poster');
  }
}

function resetForm() {
  formData.name = formData.originalName;
  changedFields.value = {};
  selectedFile.value = null;
}

async function handleSubmit() {
  try {
    const formDataToSend = new FormData();
    if (changedFields.value['name']) {
      formDataToSend.append('name', formData.name);
    }
    if (selectedFile.value) {
      formDataToSend.append('poster', selectedFile.value);
    }
    formDataToSend.append('rec_id', String(formData['id']));
    formDataToSend.append('database', formData['type']);


    const { data } = await http.post(API_URL.local_db_multiseries_update, formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  console.log(data);
  toggleForm();

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
  <div v-if="!isForm" class="seasons-container">
    <div
      v-for="season in props.seasons"
      :key="season.season_id"
      class="season-item"
      @click.stop="updateData('Seasons', season.season_id, season.season_name)"
    >
      <div class="season-header" >
        <h3>{{ season.season_name }}</h3>
      </div>

      <div class="episodes-list">
        <div
          v-for="episode in season.series"
          :key="episode.episode_id"
          class="episode-item"
          @click.stop="updateData('Series', episode.episode_id, episode.episode_name)"
        >
          {{ episode.episode_name }}
        </div>
      </div>
    </div>
  </div>

  <div v-if="isForm" class="form-overlay" @click.self="toggleForm">
    <div class="form-container">
      <div class="form-header">
        Редактирование {{ formData.type === 'Seasons' ? 'сезона:' : 'эпизода:' }} {{formData.name}}
      </div>

      <form @submit.prevent="handleSubmit" class="edit-form">
        <div class="form-field">
          <label>Название</label>
          <input
            type="text"
            id="name"
            v-model="formData.name"
            @input="markAsChanged('name')"
            :class="{ changed: changedFields['name'] }"
          />
        </div>
          <label>Загрузить постер</label>
          <input
            type="file"
            id="poster"
            @change="handleFileChange"
            :class="{ changed: changedFields['poster'] }"
          />

        <div class="form-actions">
          <button type="submit" :disabled="!hasChanges">Сохранить</button>
          <button type="button" @click="resetForm" :disabled="!hasChanges">Сбросить</button>
          <button type="button" @click="toggleForm">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.seasons-container {
  max-width: 600px;
  margin-top: 10px;
  width: 100%;
}

.season-item {
  margin-bottom: 1rem;
  border: 1px solid var(--color-text-card);
  border-radius: 5px;
  overflow: hidden;
}

.season-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--color-bg-card-header);
  cursor: pointer;
  transition: background-color 0.2s;
}

.season-header:hover {
  background-color: var(--color-bg-card);
}

.season-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.episodes-list {
  padding: 0.5rem;
  background-color: var(--color-bg-card);
}

.episode-item {
  padding: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.episode-item:last-child {
  border-bottom: none;
}

.episode-item:hover {
  background-color: #f9f9f9;
}

.form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  max-width: 100%;
  width: 100%;
}

.form-container {
  background-color: var(--color-bg-card-header);
  padding: 2rem;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;

}
.form-header {
  display: flex;
  font-size: 15px;
  margin: 10px;
  overflow: hidden;
}
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 90%;
  align-content: center;
  margin: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.form-field label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-field input {
  padding: 0.5rem;
  border: 1px solid var(--color-text-card);
  border-radius: 4px;
  background-color: var(--color-bg-card);
  color: var(--color-text-card);
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.form-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: var(--color-text-card);
}

.form-actions button[type="submit"] {
  background-color: var(--color-border-left-color);
  color: var(--color-bg-card);
}

.form-actions button[type="submit"]:disabled {
  background-color: var(--color-bg-card);
  cursor: not-allowed;
  color: var(--color-bg-card-header);
}

.form-actions button[type="button"] {
  background-color: var(--color-bg-card);
}
</style>
