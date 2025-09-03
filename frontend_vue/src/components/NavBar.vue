<script setup lang="ts">

import { ref } from 'vue'
import MenuButton from '@/components/MenuButton.vue'
import IconMenu from '@/icons/IconMenu.vue'
import { useRouter } from 'vue-router'

const isSidenav = ref<boolean>();
const menuPaths = {"Home": '/',
  "Remote": '/remote',
  "IPTV": '/iptv',
  "Settings": '/admin',
  }
const router = useRouter();



function toggleNav() {
  isSidenav.value = !isSidenav.value;
}
function goToPath(path: string) {
  router.push(path);
}

</script>

<template>
  <div class="navbar-menu">
    <div v-if="!isSidenav" class="icon-place">
      <IconMenu @click="toggleNav"/>
    </div>
  <div  v-if="isSidenav" id="Sidenav" class="sidenav" @click.stop="toggleNav">
      <div class="nav-bar">
        <MenuButton v-for="(value, key) in menuPaths" :key="key" :title="key" @click="goToPath(value)">{{ key }}</MenuButton>
      </div>
  </div>
  </div>
</template>

<style scoped>
.navbar-menu {
  position: sticky;
  top: 0;
  z-index: 3;

  height: 100%;
}

.nav-bar {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 40px;
  font-size: 30px;
  font-weight: bold;
  padding: 20px;
  height: 100vh;
  background: var(--color-bg);
}

</style>
