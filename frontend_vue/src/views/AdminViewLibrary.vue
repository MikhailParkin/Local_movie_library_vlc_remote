<script setup lang="ts">

import { API_URL, http } from '@/api.ts'
import { onMounted, ref } from 'vue'
import type { ILibraryList } from '@/interfaces/Admin.interface.ts'
import CategoryTitle from '@/components/CategoryTitle.vue'
import PathList from '@/components/PathList.vue'
import PathFinder from '@/components/PathFinder.vue'

const librariesPath = ref<ILibraryList>()
const isPathFinder = ref<boolean>(false)
const categorySelect = ref<string>()
const addPath = ref<string>()


async function fetchLibraryPath() {
  const { data } = await http.get<ILibraryList>(API_URL.library_list)
  librariesPath.value = data
  console.log(data)
}

onMounted( () => {
    fetchLibraryPath()
  }
)

async function fetchUpdateLibrary(library: string) {
  const { data } = await http.get(API_URL.library_update(library))
  console.log(data)
}

async function fetchPathDelete(path_id: number) {
  const { data } = await http.delete(API_URL.library_path_delete(path_id))
  console.log(data)
}

async function fetchAddPath() {
  const { data } = await http.post(API_URL.library_add_path, {
    service: categorySelect.value,
    path: addPath.value,
  })
  console.log(data)
}

function titleButtonAction(action: string, value: string) {
    // console.log(action, ' ', value)
    if (action === 'refresh') {
      fetchUpdateLibrary(value)
    }
    if (action === 'add') {
      categorySelect.value = value
      togglePathList()
    }
}

function deleteLibraryPath(path_id: number){
    // console.log(path_id);
    fetchPathDelete(path_id);
    fetchLibraryPath();
}

function togglePathList() {
  isPathFinder.value = !isPathFinder.value
}

function addLibraryPath(dir_path: string) {
  addPath.value = dir_path;
  fetchAddPath();
  isPathFinder.value = !isPathFinder.value;
  fetchLibraryPath()
}

</script>

<template>
  <div v-show="isPathFinder">
    <PathFinder @add-path="addLibraryPath"></PathFinder>
  </div>
  <div v-show="!isPathFinder">
    <div class="library-list" v-for="( value, key ) in librariesPath" :key="key">
      <CategoryTitle :service="key" @buttonClick="titleButtonAction">{{ key }}</CategoryTitle>
        <div class="path-list" v-for="item in value" :key="item.id">
          <ul>
            <PathList :path_id="item.id" @buttonClick="deleteLibraryPath"> {{ item.category_path }} </PathList>
          </ul>
          <label></label>
        </div>
    </div>
  </div>
</template>

<style scoped>
.library-list {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
}
.path-list {
  max-height: 60px;
}
</style>
