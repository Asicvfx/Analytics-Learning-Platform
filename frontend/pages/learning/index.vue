<script setup lang="ts">
import type { DashboardCard } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const dashboards = ref<DashboardCard[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api<DashboardCard[]>("/dashboards?size=50");
    dashboards.value = res.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <PageHeader
      title="Learning materials"
      subtitle="Open any dashboard's instructions, video lesson, and presentation."
    />
    <StateBlocks v-if="loading" variant="loading" />
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <NuxtLink
        v-for="d in dashboards"
        :key="d.id"
        :to="`/dashboards/${d.slug}`"
        class="card p-5 hover:shadow-lg transition"
      >
        <UiBadge tone="blue">{{ d.category.name }}</UiBadge>
        <h3 class="font-semibold text-ink mt-2">{{ d.title }}</h3>
        <p class="text-sm text-muted mt-1 line-clamp-2">{{ d.description }}</p>
        <p class="text-sm text-brand-deep font-medium mt-3">
          Open instructions →
        </p>
      </NuxtLink>
    </div>
  </div>
</template>
