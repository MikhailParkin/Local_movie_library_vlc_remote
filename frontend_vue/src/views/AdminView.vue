<script setup lang="ts">
import AdminList from '@/components/AdminList.vue'
import router from '@/router/routes.ts'


const handleChange = (selectedValue: string) => {
  // console.log('Выбрано значение:', selectedValue);
  router.push(selectedValue);
}
</script>

<template>
  <div class="admin-menu">
    <AdminList @change="handleChange"/>
  </div>

  <router-view />
</template>


<style scoped>
.admin-menu {
  display: flex;
  flex-direction: row;
}
</style>
