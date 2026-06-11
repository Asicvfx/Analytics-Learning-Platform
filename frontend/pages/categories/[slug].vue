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
      <div v-else class="space-y-4">
        <div
          v-for="(d, i) in filtered"
          :key="d.id"
          class="card p-5 flex flex-col md:flex-row md:items-start gap-4"
        >
          <div class="min-w-0 flex-1">
            <h3 class="font-semibold text-ink text-lg leading-snug">
              {{ i + 1 }}. {{ d.title }}
            </h3>
            <p class="text-muted mt-1">{{ d.description }}</p>
            <a
              v-if="d.reportUrl"
              :href="d.reportUrl"
              target="_blank"
              rel="noopener"
              class="text-sm text-brand-deep hover:underline break-all mt-2 inline-block"
            >
              {{ d.reportUrl }}
            </a>
          </div>
          <div class="flex flex-row md:flex-col gap-2 shrink-0">
            <a
              v-if="d.reportUrl"
              :href="d.reportUrl"
              target="_blank"
              rel="noopener"
              class="btn-primary text-center whitespace-nowrap"
            >
              Открыть отчёт ↗
            </a>
            <NuxtLink
              :to="`/dashboards/${d.slug}`"
              class="btn-secondary text-center whitespace-nowrap"
            >
              Инструкция и FAQ
            </NuxtLink>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
