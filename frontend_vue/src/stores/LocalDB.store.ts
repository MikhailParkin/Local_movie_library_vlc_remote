import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { ILocalDb } from '@/interfaces/LocalDB.interface.ts'


export const useLocalDbStore = defineStore('localDB', () => {
  const local_db  = ref<ILocalDb[]>()
  async function fetchLocalDB() {
    const { data } =  await http.get<ILocalDb[]>(API_URL.local_db)
    local_db.value = data
  }
  return { local_db, fetchLocalDB}
});
