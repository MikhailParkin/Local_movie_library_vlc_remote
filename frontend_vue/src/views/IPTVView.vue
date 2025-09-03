<script setup lang="ts">

import { API_URL, http } from '@/api.ts'
import { nextTick, onMounted, ref, watch } from 'vue'
import MenuButton from '@/components/MenuButton.vue'
import ChannelList from '@/components/ChannelList.vue'
import { useChannelStore, useEpgChannelStore, useEpgNowStore } from '@/stores/Channels.store.ts'
import EpgNowList from '@/components/EpgNowList.vue'
import EpgChannel from '@/components/EpgChannel.vue'
import IconBackArrow from '@/icons/IconBackArrow.vue'

const groups = ref<string[]>()
const isGroup = ref<boolean>(true)
const isChannels = ref<boolean>(false)
const isEpg = ref<boolean>(false)
const channelStore = useChannelStore()
const epgChannelsNow = useEpgNowStore()
const epgChannelStore  = useEpgChannelStore()
const epgListContainer = ref<HTMLElement | null>(null)


async function fetchPlaylistGroup() {
  const { data } = await http.get(API_URL.iptv_group)
  // console.log(data)
  groups.value = data
}

onMounted(() => {
    fetchPlaylistGroup()
  if (isEpg.value) {
    scrollToCurrentProgram();
  }
  }

)

function getListChannels(group: string) {
  isGroup.value = !isGroup.value;
  isChannels.value = !isChannels.value;

  channelStore.channels = [];
  epgChannelsNow.epgNow = [];
  epgChannelStore.epgChannel = [];

  channelStore.fetchChannels(group);
  epgChannelsNow.fetchEpgNow(group);
}

function getEpgForChannel(channel_id: string) {
  // console.log(channel_id);
  isEpg.value = !isEpg.value;
  isChannels.value = !isChannels.value;
  epgChannelStore.fetchEpgChannel(channel_id);
}

function toggleTabs() {
  // console.log('arrow')
  if (isEpg.value) {
    isEpg.value = !isEpg.value;
    isChannels.value = true;

    epgChannelStore.epgChannel = [];

  }
  else { if(isChannels.value) {
    isChannels.value = !isChannels.value;
    isGroup.value = !isGroup.value;

    channelStore.channels = [];
    epgChannelsNow.epgNow = [];
  }
  }
}

async function fetchPlay(play_url: string) {
  const { data } = await http.post(API_URL.iptv_play, {
    url: play_url
  })
  console.log(data)
}

function playChannelNow(channel_url: string) {
  // console.log(channel_url);
  fetchPlay(channel_url);
}

const scrollToCurrentProgram = async () => {
  await nextTick();

  setTimeout(() => {
    const currentProgram = epgListContainer.value?.querySelector('.epg-channel.current');
    if (currentProgram) {
      currentProgram.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }
  }, 100);
};
watch(() => epgChannelStore.epgChannel, () => {
  if (isEpg.value) {
    scrollToCurrentProgram();
  }
});
watch(() => epgChannelsNow.epgNow, () => {
  console.log(epgChannelsNow.epgNow)
});
</script>

<template>
  <IconBackArrow v-if="!isGroup" :size="70" @click="toggleTabs"/>
  <div v-if="isGroup && !isChannels && !isEpg" class="playlist-group">
    <MenuButton v-for="(item, index) in groups" :key="index" @click="getListChannels(item)">{{ item }}</MenuButton>
  </div>
  <div v-if="isChannels && !isGroup && !isEpg" class="playlist-channels">
    <div v-for="(item, index) in channelStore.channels" :key="item.id">
      <ChannelList :channel_url="item.url" :channel-number="index + 1" :channel-img="item.tvg_logo" :tvgID="item.tvg_id" :channel-name="item.channel_name" @clickChannel="playChannelNow">
      </ChannelList>
      <div v-if="epgChannelsNow.epgNow && epgChannelsNow.epgNow[item.id]">
        <EpgNowList :channel_id="item.tvg_id" @clickEpgButton="getEpgForChannel">{{ epgChannelsNow.epgNow[item.id] }}</EpgNowList>
      </div>
    </div>
  </div>
  <div v-if="isEpg && !isGroup && !isChannels">
    <div v-if="epgChannelStore.epgChannel"
         class="epg-list-container"
         ref="epgListContainer">
      <div v-for="(item, index) in epgChannelStore.epgChannel" :key="index">
        <EpgChannel
          :epg_url="item.url"
          :start="item.start"
          :end="item.end"
          :title="item.title"
          @clickEpgHistory="playChannelNow">
        </EpgChannel>
      </div>
    </div>

  </div>

</template>

<style scoped>
.playlist-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.epg-list-container {
  max-height: 80vh;
  overflow-y: auto;
}
</style>
