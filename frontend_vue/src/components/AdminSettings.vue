<script setup lang="ts">

import type { ISettings } from '@/interfaces/Backup.interface.ts'
import { computed, reactive, ref } from 'vue'
import { API_URL, http } from '@/api.ts'

const props = defineProps<{settings: ISettings}>();
const formData = reactive({ ...props.settings });
const changedFields = ref<Record<string, boolean>>({});
const hasChanges = computed(() => {
  return Object.values(changedFields.value).some(value => value)
})
const emit = defineEmits(['change-data'])

const markAsChanged = (fieldKey: string) => {
  changedFields.value[fieldKey] = true
}
const handleSubmit = async () => {
  try {
    const formDataToSend = new FormData();

    for (const key in changedFields.value) {
      if (changedFields.value[key] && key in formData) {
        // Приводим key к типу ключей formData
        const formKey = key as keyof typeof formData;
        formDataToSend.append(key, String(formData[formKey]));
      }
    }

    const { data } = await http.post(API_URL.admin_settings, formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log('Данные успешно сохранены:', data);
    changedFields.value = {};
    emit('change-data');


  } catch (error) {
    console.error('Ошибка при сохранении:', error);
  }
}

</script>

<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit" class="edit-form">
      <div class="form-field">
        <label>Playlist URL</label>
        <input type="text" id="playlist_url" v-model="formData.playlist_url"
               @input="markAsChanged('playlist_url')"
               :class="{ changed: changedFields['playlist_url'] }" />
      </div>
      <div class="form-field">
        <label>EPG URL</label>
        <input type="text" id="epg_url" v-model="formData.epg_url"
               @input="markAsChanged('epg_url')"
               :class="{ changed: changedFields['epg_url'] }"/>
      </div>
      <div class="form-actions">
        <button type="submit" :disabled="!hasChanges" >Change</button>
      </div>
    </form>
  </div>


</template>

<style scoped>
.form-container {
  width: 100%;
  background-color: var(--color-bg-card);
  border-radius: 8px;
}
.edit-form {
  width: 100%;
  max-width: 600px;
  margin-top: 10px;
  padding-top: 10px;
}
.form-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 24px;
  margin-top: 10px;
  margin-left: 10px;
}
.form-field input {
  width: 90%;
  padding: 0.5rem;
  border: 1px solid var(--color-text-card);
  border-radius: 4px;
  overflow: hidden;
  background-color: var(--color-bg-card);
  color: var(--color-text-card);
  font-size: 20px;
  margin-left: 10px;
}

.form-field input.changed,
.form-field textarea.changed {
  border-color: var(--color-text-card);
  background-color: rgba(66, 184, 131, 0.1);
}
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  align-items: center;
}

.form-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 20px;
  margin-left: 20px;
  margin-bottom: 20px;

}

.form-actions button[type="submit"] {
  background-color: #42b883;
  color: white;

}

.form-actions button[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.form-actions button[type="button"] {
  background-color: #f0f0f0;
}

.form-actions button[type="button"]:disabled {
  cursor: not-allowed;
}
</style>
