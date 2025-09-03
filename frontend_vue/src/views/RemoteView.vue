<script setup lang="ts">

import MenuButton from '@/components/MenuButton.vue'
import IconBackward from '@/icons/IconBackward.vue'
import IconForward from '@/icons/IconForward.vue'
import IconPause from '@/icons/IconPause.vue'
import IconStop from '@/icons/IconStop.vue'
import { onMounted, ref, watchEffect } from 'vue'
import IconPlay from '@/icons/IconPlay.vue'
import { useRemoteCommandStore, useStatusVlcStore } from '@/stores/Remote.store.ts'
import { API_URL, http } from '@/api.ts'
import type { IStreams } from '@/interfaces/AudioStreams.interface.ts'
import RewindSlider from '@/components/RewindSlider.vue'
import { usePlayingVideoStore } from '@/stores/PlayingVideo.store.ts'

const isPause = ref<boolean>(false);
const isStreams = ref<boolean>(false);
const statusStore = useStatusVlcStore();
const commandStore = useRemoteCommandStore();
const audioStreams = ref<IStreams[]>();
const playingStore = usePlayingVideoStore();

async function fetchAudioStreams() {
  const { data } = await http.get<IStreams[]>(API_URL.remote('audio_list'))
  audioStreams.value = data
}

onMounted(() => {
  checkVLCStatus()
})

function checkVLCStatus() {
  statusStore.fetchStatusVlc();

  if (statusStore.statusVlcNow?.status === 'Pause') {
    isPause.value = true;
  }
}

watchEffect( () => {
    console.log(statusStore.statusVlcNow)
  }
)

function clickPause(command: string): void {
  isPause.value = !isPause.value
  commandStore.fetchRemoteCommand(command)
}
function sendCommand(command: string): void {
  if (command == 'audio_list') {
    if (statusStore.statusVlcNow?.status !== 'Close') {
        // console.log(command)
        fetchAudioStreams()
        isStreams.value = !isStreams.value
    }
  }
  else {
    commandStore.fetchRemoteCommand(command)
    // console.log(command)
    // console.log(commandStore.remoteRequest)
  }
}

const handleChange = (event: string) => {
  // console.log(event);
  sendCommand(`seek?q=${event}`)

}
</script>

<template>
  <div class="video-title">
    <h1 v-if="statusStore.statusVlcNow">{{ statusStore.statusVlcNow.title }}</h1>
  </div>
  <div v-show="isStreams" class="streams-window" @click.stop="() => isStreams = !isStreams">
    <div v-if="audioStreams">
      <MenuButton v-for="item in audioStreams" :key="item.stream_index" @click="sendCommand(`atrack?q=${item.stream_index}`)">{{ item.title }}</MenuButton>
    </div>
  </div>
  <div class="main-remote-menu">
    <MenuButton title="" @click="clickPause('pause')"><IconPause v-if="!isPause" :size="20"/><IconPlay v-if="isPause" :size="20"/></MenuButton>
    <MenuButton title="" @click="sendCommand('quit')"><IconStop :size="20"/></MenuButton>
    <MenuButton title="" @click="sendCommand('sub_off')">Sub OFF</MenuButton>
    <MenuButton title="" @click="sendCommand('audio_list')">Audio Stream</MenuButton>
    <MenuButton v-if="playingStore.playingvideo" title="" @click="sendCommand(`seek?=q${playingStore.playingvideo.video_length}`)">Resume</MenuButton>

    <div v-if="!playingStore" class="remote-playlist">
      <MenuButton title="" @click="sendCommand('prev')"><icon-backward :size="20"/></MenuButton>
      <MenuButton title="" @click="sendCommand('next')"><IconForward :size="20"/></MenuButton>
    </div>
    <div v-if="statusStore.statusVlcNow">
      <RewindSlider :max="statusStore.statusVlcNow.duration" :seconds="statusStore.statusVlcNow.time" @change="handleChange"/>
    </div>
  </div>

</template>

<style scoped>
.main-remote-menu {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}
.video-title {
  font-size: 10px;
  text-align: center;
  overflow: hidden;
  width: 100%;

}
.remote-playlist {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.streams-window {
  display: flex;
  position: absolute;
  top: 0;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  padding: 20px;
  height: 100vh;
  background: var(--color-bg);
  z-index: 5;
}

</style>
