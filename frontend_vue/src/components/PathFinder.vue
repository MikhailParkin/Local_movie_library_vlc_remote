<script setup lang="ts">

import { API_URL, http } from '@/api.ts'
import { onMounted, ref } from 'vue'
import type { IPathList } from '@/interfaces/Admin.interface.ts'
import ListSimple from '@/components/ListSimple.vue'
import ListButton from '@/components/ListButton.vue'
import IconPlus from '@/icons/IconPlus.vue'

const paths_list = ref<IPathList[]>()
const path_depth = ref<number>(-1)
const path_now = ref<string>('')
const path_history = ref<string[]>([])
const emit = defineEmits(['add-path'])


async function fetchGetPath(dir_path: string) {
  const { data } = await http.post(API_URL.library_get_path, {
    path: dir_path
  })
  paths_list.value = data;
  path_depth.value = dir_path ? path_history.value.length : 0;
}

onMounted(() => {
  fetchGetPath('')
  path_depth.value = 0;
})

function pathClick(path: string) {
  path_now.value = path;
  path_history.value.push(path);
  fetchGetPath(path);
}

function find_prev_path() {
  if (path_depth.value <= 0) return;

  path_depth.value--;
  path_history.value.pop();
  const prev_path = path_history.value[path_history.value.length - 1];
  path_now.value = prev_path;
  fetchGetPath(prev_path);
}
</script>

<template>
  <div>

    <div class="path-finder-header">
      <h2>{{ path_now }}</h2>
      <ListButton @click="emit('add-path', path_now)"><IconPlus :size="30"/></ListButton>
    </div>
    <div v-show="path_depth > 0">
      <ul class="list-container">
        <li class="open-folder" @click="find_prev_path">..</li>
      </ul>
    </div>

    <div v-for="(value, key) in paths_list" :key="key">
      <ul>
        <ListSimple :path="value.dir_path" @pathButtonClick="pathClick">{{ value.dir_name }}</ListSimple>
      </ul>

    </div>

  </div>



</template>

<style scoped>
.path-finder-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  overflow: hidden;
}
.open-folder {
  list-style-type: none;
  padding-left: 5px;
  cursor: pointer;
}
.open-folder::marker {
  content: "\01F5C1";
  font-size: 25px;
}
</style>
