<script setup lang="ts">
import { onMounted } from 'vue'
import { useCategoriesStore } from '@/stores/Categories.store.ts'
import MenuButton from '@/components/MenuButton.vue'
import router from '@/router/routes.ts'

const store = useCategoriesStore();


onMounted(() => {
  store.fetchCategories();
})

</script>

<template>


  <div class="category-menu" v-if="store.categories">

    <MenuButton  v-for="item in store.categories"
                 :key="item.id"
                 :title="item.name"
                 @click="() => router.push(`/list-videos/${item.category}`)">{{ item.name }}</MenuButton>

  </div>

</template>

<style scoped>
.category-menu  {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  font-size: 30px;
  font-weight: bold;
  padding: 20px;
}
</style>
