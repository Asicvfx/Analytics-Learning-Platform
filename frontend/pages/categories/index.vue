<script setup lang="ts">
import type { Category } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const categories = ref<Category[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api<Category[]>("/categories?active=true");
    categories.value = res.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <PageHeader
      title="Categories"
      subtitle="Browse dashboards by business category."
    />
    <StateBlocks v-if="loading" variant="loading" />
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <NuxtLink
        v-for="c in categories"
        :key="c.id"
        :to="`/categories/${c.slug}`"
        class="card p-6 hover:shadow-lg transition"
      >
        <h3 class="font-semibold text-ink text-lg">{{ c.name }}</h3>
        <p class="text-sm text-muted mt-1">{{ c.description }}</p>
        <p class="text-sm text-brand-deep font-medium mt-3">
          {{ c.dashboardCount ?? 0 }} dashboards →
        </p>
      </NuxtLink>
    </div>
  </div>
</template>
