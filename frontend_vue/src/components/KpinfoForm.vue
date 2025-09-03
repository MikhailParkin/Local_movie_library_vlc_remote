<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { API_POSTER_URL, API_URL, http } from '@/api.ts'
import type { IKpinfo } from '@/interfaces/KPinfo.interface.ts'

const props = defineProps<{ initialData: IKpinfo }>();
const poster = ref<string>(API_POSTER_URL(props.initialData.poster_filename));
const selectedFile = ref<File | null>(null);
const emit = defineEmits(['buttonClick'])

const formData = reactive({ ...props.initialData });
const changedFields = ref<Record<string, boolean>>({});

const hasChanges = computed(() => {
  return Object.values(changedFields.value).some(value => value)
})

const markAsChanged = (fieldKey: string) => {
  changedFields.value[fieldKey] = true
}

const resetForm = () => {

  formData.id = props.initialData.id;
  formData.kp_id = props.initialData.kp_id;
  formData.name = props.initialData.name;
  formData.year = props.initialData.year;
  formData.poster = props.initialData.poster;
  formData.poster_filename = props.initialData.poster_filename;
  formData.describe = props.initialData.describe;
  formData.rate = props.initialData.rate;

  changedFields.value = {}
  selectedFile.value = null;
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0];
    markAsChanged('poster');
  }
}

// Функция отправки формы
const handleSubmit = async () => {
  try {
    const formDataToSend = new FormData();

    if (changedFields.value.id) formDataToSend.append('id', String(formData.id));
    if (changedFields.value.kp_id) formDataToSend.append('kp_id', formData.kp_id);
    if (changedFields.value.name) formDataToSend.append('name', formData.name);
    if (changedFields.value.year) formDataToSend.append('year', String(formData.year));
    if (changedFields.value.poster) formDataToSend.append('poster', formData.poster);
    if (changedFields.value.poster_filename) formDataToSend.append('poster_filename', formData.poster_filename);
    if (changedFields.value.describe) formDataToSend.append('describe', formData.describe);
    if (changedFields.value.rate) formDataToSend.append('rate', formData.rate);


    if (selectedFile.value) {
      formDataToSend.append('poster', selectedFile.value);
    }

    // Отправляем данные на сервер
    const { data } = await http.post(API_URL.kp_info_update(props.initialData.id), formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log('Данные успешно сохранены:', data);

    // После успешного сохранения сбрасываем отслеживание изменений
    changedFields.value = {};
    selectedFile.value = null;

    // Обновляем изображение постера, если файл был изменен
    if (changedFields.value['poster'] && selectedFile.value) {
      poster.value = URL.createObjectURL(selectedFile.value);
    }

  } catch (error) {
    console.error('Ошибка при сохранении:', error);
  }
  emit('buttonClick')
}

// Следим за изменением initialData (если объект может меняться извне)
watch(() => props.initialData, (newValue) => {
  formData.id = newValue.id;
  formData.kp_id = newValue.kp_id;
  formData.name = newValue.name;
  formData.year = newValue.year;
  formData.poster = newValue.poster;
  formData.poster_filename = newValue.poster_filename;
  formData.describe = newValue.describe;
  formData.rate = newValue.rate;

  changedFields.value = {}
  selectedFile.value = null;
  // Обновляем URL постера
  poster.value = API_POSTER_URL(newValue.poster_filename);
}, { deep: true })
</script>

<template>
  <form @submit.prevent="handleSubmit" class="edit-form">
    <div class="form-field">
      <label>Название</label>
      <input type="text" id="name" v-model="formData.name" @input="markAsChanged('name')"
             :class="{ changed: changedFields['name'] }" />
    </div>
    <div class="short-value">
      <div class="form-field">
        <label>КПID</label>
        <input type="text" id="kp_id" v-model="formData.kp_id" @input="markAsChanged('kp_id')"
               :class="{ changed: changedFields['kp_id'] }"/>
      </div>
      <div class="form-field">
        <label>Год</label>
        <input type="text" id="year" v-model="formData.year" @input="markAsChanged('year')"
               :class="{ changed: changedFields['year'] }"/>
      </div>
      <div class="form-field">
        <label>Рейтинг</label>
        <input type="text" id="rate" v-model="formData.rate" @input="markAsChanged('rate')"
               :class="{ changed: changedFields['rate'] }"/>
      </div>
    </div>
    <div class="poster-container">
      <img class="poster-img" :src="poster" alt="Poster">
    </div>
    <div class="form-field">
      <label>Загрузить постер</label>
      <input
        type="file"
        id="poster"
        @change="handleFileChange"
        :class="{ changed: changedFields['poster'] }"
      />
    </div>
    <div class="form-field">
      <label>Описание</label>
      <textarea id="describe" v-model="formData.describe" @input="markAsChanged('describe')"
                :class="{ changed: changedFields['describe'] }"/>
    </div>

    <div class="form-actions">
      <button type="submit" :disabled="!hasChanges">Сохранить</button>
      <button type="button" @click="resetForm" :disabled="!hasChanges">Сбросить</button>
    </div>
  </form>
</template>

<style scoped>
.short-value {
  display: flex;
  flex-direction: row;
  width: 97%;
  max-width: 600px;
  gap: 20px;
}
.poster-container {
  display: flex;
  max-width: 500px;
  width: 100%;
  justify-content: center;
  margin-top: 10px;
}
.poster-img {
  max-width: 300px;
  width: 100%;
}
.edit-form {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.form-field {
  position: relative;
}

.form-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 24px;
  margin-top: 10px;
}

.form-field textarea {
  width: 95%;
  height: 150px;
  padding: 0.5rem;
  border: 1px solid var(--color-text-card);
  border-radius: 4px;
  background-color: var(--color-bg-card);
  color: var(--color-text-card);
  font-size: 17px;
}

.form-field input {
  width: 95%;
  padding: 0.5rem;
  border: 1px solid var(--color-text-card);
  border-radius: 4px;
  overflow: hidden;
  background-color: var(--color-bg-card);
  color: var(--color-text-card);
  font-size: 17px;
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
}

.form-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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
