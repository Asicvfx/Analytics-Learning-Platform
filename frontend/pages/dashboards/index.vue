<script setup lang="ts">
import type { Category, DashboardCard } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const route = useRoute();

const dashboards = ref<DashboardCard[]>([]);
const categories = ref<Category[]>([]);
const loading = ref(true);
const search = ref((route.query.search as string) || "");
const category = ref((route.query.category as string) || "");

async function load() {
  loading.value = true;
  try {
    const params = new URLSearchParams({ size: "50" });
    if (search.value) params.set("search", search.value);
    if (category.value) params.set("category", category.value);
    const res = await api<DashboardCard[]>(`/dashboards?${params}`);
    dashboards.value = res.data;
  } finally {
    loading.value = false;
  }
}

function reset() {
  search.value = "";
  category.value = "";
  load();
}

onMounted(async () => {
  const cat = await api<Category[]>("/categories?active=true");
  categories.value = cat.data;
  await load();
});
</script>

<template>
  <div>
    <PageHeader
      title="Dashboard catalog"
      subtitle="Browse all dashboards available to you."
    />

    <div class="card p-4 mb-6 flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-[200px]">
        <label class="label">Search</label>
        <input
          v-model="search"
          class="input"
          placeholder="Search by title or description…"
          @keyup.enter="load"
        />
      </div>
      <div class="min-w-[200px]">
        <label class="label">Category</label>
        <select v-model="category" class="input">
          <option value="">All categories</option>
          <option v-for="c in categories" :key="c.id" :value="c.slug">
            {{ c.name }}
          </option>
        </select>
      </div>
      <button class="btn-primary" @click="load">Apply</button>
      <button class="btn-secondary" @click="reset">Reset</button>
    </div>

    <StateBlocks v-if="loading" variant="loading" />
    <StateBlocks
      v-else-if="!dashboards.length"
      variant="empty"
      title="No dashboards found"
      message="Try changing your search or filters."
    />
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <DashboardCard v-for="d in dashboards" :key="d.id" :dashboard="d" />
    </div>
  </div>
</template>
