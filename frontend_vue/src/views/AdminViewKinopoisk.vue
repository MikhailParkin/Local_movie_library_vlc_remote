<script setup lang="ts">

import { useKpinfoStore } from '@/stores/KinopoiskBd.store.ts'
import { onMounted, ref } from 'vue'
import BDListRow from '@/components/BDListRow.vue'
import KpinfoForm from '@/components/KpinfoForm.vue'
import IconBackArrow from '@/icons/IconBackArrow.vue'
import MenuButton from '@/components/MenuButton.vue'

const kpinfoStore = useKpinfoStore();
const isListData = ref<boolean>(true);
const formData = ref();

onMounted(() => {
  kpinfoStore.fetchKpinfo()
})

function changeRec(index: number) {
  if (kpinfoStore.kpinfo) {
    isListData.value = !isListData.value
    formData.value = kpinfoStore.kpinfo[index]
  }

}

function toggleTabs() {
  if (!isListData.value) {
    isListData.value = !isListData.value
    formData.value = null
    kpinfoStore.fetchKpinfo()
  }
}
function addNewRecord() {
  isListData.value = !isListData.value
  formData.value = {
    id: 999999,
    kp_id: '',
    name: '',
    year: 0,
    poster: '',
    poster_filename: '',
    describe: '',
    rate: '',
  }
}
</script>

<template>
  <IconBackArrow :size="30" @click="toggleTabs()"/>
<div v-if="isListData">
  <div class="add-button">
    <MenuButton @click="addNewRecord()">Add new record</MenuButton>
  </div>

  <BDListRow v-for="(item, index) in kpinfoStore.kpinfo"
             :key="index"
             :rec_name="item.name"
             :rec_number="index" @clickSetting="changeRec"/>
</div>
<div  v-if="!isListData">
  <KpinfoForm :initial-data="formData" @buttonClick="toggleTabs"/>
</div>

</template>

<style scoped>
.add-button {
  display: flex;
  align-items: center;
  margin-top: 10px;
}
</style>
