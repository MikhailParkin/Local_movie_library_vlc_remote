import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'
import type { IStatusVLC } from '@/interfaces/StatusVLC.inteface.ts'

export const useStatusVlcStore = defineStore('statusVlc', () => {
  const statusVlcNow  = ref<IStatusVLC>()
  async function fetchStatusVlc() {
    const { data } =  await http.get<IStatusVLC>(API_URL.status_vlc)
    statusVlcNow.value = data
  }

  return { statusVlcNow, fetchStatusVlc }
})

export const useRemoteCommandStore = defineStore('remote_command', () => {
  const remoteRequest  = ref<IStatusVLC>()
  async function fetchRemoteCommand(command: string) {
    const { data } =  await http.get<IStatusVLC>(API_URL.remote(command))
    remoteRequest.value = data
  }

  return { remoteRequest, fetchRemoteCommand }
})
