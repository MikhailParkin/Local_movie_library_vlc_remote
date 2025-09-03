<script setup lang="ts">
import MenuButton from '@/components/MenuButton.vue'
import { onMounted, ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { IBackUp, ISettings } from '@/interfaces/Backup.interface.ts'
import AdminBackupList from '@/components/AdminBackupList.vue'
import AdminSettings from '@/components/AdminSettings.vue'


const backUpRecords = ref<IBackUp[]>();
const settingsRecords = ref<ISettings>();
const isListBackup = ref<boolean>(false);
const isIptv = ref<boolean>(false);

async function fetchBackupRecords() {
  const { data } = await http.get(API_URL.admin_page_backup_list)
  console.log(data);
  backUpRecords.value = data;
}

async function fetchSettingsRecords() {
  const { data } = await http.get(API_URL.admin_settings)
  console.log(data);
  settingsRecords.value = data;
}

async function fetchAction(action: string, q: string ) {
  const { data } = await http.get(API_URL.admin_page_action(action, q));
  console.log(data);
}
onMounted(() => {
  fetchBackupRecords();
  fetchSettingsRecords();
})

function updatePlaylist() {
  isIptv.value = !isIptv.value;
  fetchSettingsRecords();
}

</script>

<template>
  <div  class="admin-backup-menu">
    <MenuButton @click="fetchAction('backup', '')">BackUp</MenuButton>
    <MenuButton @click="() => {isListBackup = !isListBackup}">Restore</MenuButton>
    <div v-if="isListBackup">
      <div v-if="backUpRecords">
        <AdminBackupList :backups="backUpRecords" @backupClick="fetchAction"></AdminBackupList>
      </div>
    </div>
    <MenuButton @click="() => {isIptv = !isIptv}">IPTV</MenuButton>
    <div v-if="isIptv">
      <div v-if="settingsRecords">
        <AdminSettings :settings="settingsRecords" @change-data="updatePlaylist"/>
        <div class="manage-buttons">
          <MenuButton @click="fetchAction('playlist-update', '')">Playlist Update</MenuButton>
          <MenuButton @click="fetchAction('epg_update', '')">EPG Update</MenuButton>
        </div>
      </div>
    </div>
  </div>





</template>

<style scoped>
.admin-backup-menu {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.manage-buttons {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  padding: 0.5rem;
}
</style>
