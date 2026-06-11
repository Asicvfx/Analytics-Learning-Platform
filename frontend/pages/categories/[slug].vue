<script setup lang="ts">
import type { Category, DashboardCard } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const route = useRoute();
const slug = route.params.slug as string;

const category = ref<Category | null>(null);
const dashboards = ref<DashboardCard[]>([]);
const loading = ref(true);
const search = ref("");

const filtered = computed(() => {
  if (!search.value) return dashboards.value;
  const t = search.value.toLowerCase();
  return dashboards.value.filter(
    (d) =>
      d.title.toLowerCase().includes(t) ||
      d.description.toLowerCase().includes(t),
  );
});

onMounted(async () => {
  try {
    const [cat, dash] = await Promise.all([
      api<Category>(`/categories/${slug}`),
      api<DashboardCard[]>(`/dashboards?category=${slug}&size=50`),
    ]);
    category.value = cat.data;
    dashboards.value = dash.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <StateBlocks v-if="loading" variant="loading" />
    <template v-else-if="category">
      <PageHeader :title="category.name" :subtitle="category.description">
        <template #actions>
          <NuxtLink to="/categories" class="btn-secondary">Все категории</NuxtLink>
        </template>
      </PageHeader>

      <div class="card p-4 mb-6 max-w-md">
        <input v-model="search" class="input" placeholder="Поиск в категории…" />
      </div>

      <StateBlocks
        v-if="!filtered.length"
        variant="empty"
        title="Отчёты не найдены"
        message="Измените запрос поиска."
      />
      <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <DashboardCard v-for="d in filtered" :key="d.id" :dashboard="d" />
      </div>
    </template>
  </div>
</template>
