<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocalDbStore } from '@/stores/LocalDB.store.ts'
import LocalDbListElement from '@/components/LocalDbListElement.vue'
import { useKpinfoStore } from '@/stores/KinopoiskBd.store.ts'
import BDListElementSimple from '@/components/BDListElementSimple.vue'
import IconBackArrow from '@/icons/IconBackArrow.vue'
import { API_URL, http } from '@/api.ts'
import SeasonsSeriesLocalDB from '@/components/SeasonsSeriesLocalDB.vue'
import type { ISeasons } from '@/interfaces/Seasons.interface.ts'
import IconTrash from '@/icons/IconTrash.vue'

const localStore = useLocalDbStore();
const kpinfoStore = useKpinfoStore();
const isLocalDbList = ref<boolean>(true);
const isSerialsList = ref<boolean>(false);
const fileID = ref<number>();
const seasonsData  = ref<ISeasons[]>([]);

onMounted(() => {
  localStore.fetchLocalDB()
})

function showListKpinfo(file_id: number) {
  // console.log('showListKpinfo', file_id);
  kpinfoStore.fetchKpinfo();
  isLocalDbList.value = !isLocalDbList.value;
  fileID.value = file_id;
}
function toggleTabs() {
  if (!isLocalDbList.value) {
    isLocalDbList.value = !isLocalDbList.value;
  }
  if (isSerialsList.value) {
    seasonsData.value = []
    isSerialsList.value = false;
  }

}

async function fetchUpdateLocalBd(file_id: number, kpinfo_id: number) {
  const { data } = await http.post(API_URL.local_db, {
    file_id: file_id,
    kpinfo_id: kpinfo_id,
  })
  console.log(data)
}

function selectDescribe(rec_id: number) {
  // console.log('kpID', rec_id);
  // console.log('fileID', fileID.value);
  isLocalDbList.value = !isLocalDbList.value;
  if (fileID.value) {
    fetchUpdateLocalBd(fileID.value, rec_id);
  }

}

async function fetchMultiseries(record_id: number) {
  const { data } = await http.get(API_URL.local_db_multiseries(record_id))
  console.log(data)
  seasonsData.value = data
}

function getMultiseries(rec_id: number) {
  fetchMultiseries(rec_id);
  isSerialsList.value = true;
  isLocalDbList.value = false;
}
</script>

<template>
  <IconBackArrow v-if="!isLocalDbList || isSerialsList" :size="30" @click="toggleTabs()"/>
  <div v-if="isLocalDbList">
    <div class="record-container" v-if="localStore.local_db">
      <div class="record-item" v-for="item in localStore.local_db" :key="item.id">
        <div class="category-name"  v-if="item.category === 'Serials'">
          <div>
            <IconTrash :size="17"/>
          </div>
          <div @click="getMultiseries(item.id)">
            {{ item.category }}
          </div>
        </div>
        <div class="category-name" v-else>
          <div>
            <IconTrash :size="17"/>
          </div>
          <div>
            {{ item.category}}
          </div>
        </div>
        <LocalDbListElement :kpinfo_id="item.kpinfo_id" :filename="item.file_name" :file_id="item.id" @clickRecord="showListKpinfo"/>
      </div>
    </div>
  </div>

  <div v-if="!isLocalDbList && !isSerialsList">
    <div v-if="kpinfoStore.kpinfo">
      <div v-for="item in kpinfoStore.kpinfo" :key="item.id">
          <BDListElementSimple :name="item.name" :rec_id="item.id" @clickKpRecord="selectDescribe"/>
      </div>
    </div>
  </div>

  <div v-if="!isLocalDbList && isSerialsList">
    <div v-if="seasonsData">
      <SeasonsSeriesLocalDB :seasons="seasonsData"/>
    </div>

  </div>


</template>

<style scoped>
.record-container {
  max-width: 600px;
  margin-top: 10px;
  width: 100%;
}

.record-item {
  margin-bottom: 1rem;
  border: 1px solid var(--color-text-card);
  border-radius: 5px;
  overflow: hidden;
}

.category-name {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--color-bg-card-header);
  cursor: pointer;
  transition: background-color 0.2s;

}

.category-name:hover {
  background-color: var(--color-bg-card);
}

</style>
