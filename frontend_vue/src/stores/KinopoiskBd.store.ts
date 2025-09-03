import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { IKpinfo } from '@/interfaces/KPinfo.interface.ts'


export const useKpinfoStore = defineStore('kpinfo', () => {
  const kpinfo  = ref<IKpinfo[]>()
  async function fetchKpinfo() {
    const { data } =  await http.get<IKpinfo[]>(API_URL.kp_info)
    kpinfo.value = data
  }
  return { kpinfo, fetchKpinfo}
});
