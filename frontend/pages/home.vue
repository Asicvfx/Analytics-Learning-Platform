<script setup lang="ts">
import type { Category, DashboardCard } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const auth = useAuthStore();

const categories = ref<Category[]>([]);
const dashboards = ref<DashboardCard[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const [cat, dash] = await Promise.all([
      api<Category[]>("/categories?active=true"),
      api<DashboardCard[]>("/dashboards?size=6"),
    ]);
    categories.value = cat.data;
    dashboards.value = dash.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <div
      class="rounded-2xl bg-gradient-to-br from-brand-deep to-brand-primary
             text-white p-8 mb-8"
    >
      <h1 class="text-2xl md:text-3xl font-bold">
        С возвращением, {{ auth.user?.fullName }}
      </h1>
      <p class="text-white/85 mt-1">
        Находите отчёты, открывайте аналитику и учитесь работать с каждым отчётом.
      </p>
    </div>

    <StateBlocks v-if="loading" variant="loading" />

    <template v-else>
      <section class="mb-8">
        <h2 class="text-lg font-semibold text-ink mb-3">Категории</h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <NuxtLink
            v-for="c in categories"
            :key="c.id"
            :to="`/categories/${c.slug}`"
            class="card p-4 hover:shadow-lg transition"
          >
            <p class="font-semibold text-ink">{{ c.name }}</p>
            <p class="text-xs text-muted mt-1 line-clamp-2">{{ c.description }}</p>
            <p class="text-xs text-brand-deep mt-2 font-medium">
              Отчётов: {{ c.dashboardCount ?? 0 }}
            </p>
          </NuxtLink>
        </div>
      </section>

      <section>
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-lg font-semibold text-ink">Недавние отчёты</h2>
          <NuxtLink to="/dashboards" class="text-sm text-brand-deep font-medium">
            Все отчёты →
          </NuxtLink>
        </div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <DashboardCard
            v-for="d in dashboards"
            :key="d.id"
            :dashboard="d"
          />
        </div>
      </section>
    </template>
  </div>
</template>
