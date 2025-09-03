import { defineStore } from 'pinia'
import type { ICategory } from '@/interfaces/categories.interface.ts'
import { ref } from 'vue'
import { API_URL, http } from '@/api.ts'

export const useCategoriesStore = defineStore('Categories', () => {
  const categories = ref<ICategory[]>()

  async function fetchCategories(): Promise<void> {

    const { data } = await  http.get<ICategory[]>(API_URL.categories)
    categories.value = data;
  }

  return { categories, fetchCategories}
});
