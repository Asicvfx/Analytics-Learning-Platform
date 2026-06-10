<script setup lang="ts">
import type { DashboardCard } from "~/types";

const props = defineProps<{ dashboard: DashboardCard }>();

const updated = computed(() =>
  props.dashboard.lastUpdatedAt
    ? new Date(props.dashboard.lastUpdatedAt).toLocaleDateString()
    : "—",
);
</script>

<template>
  <div class="card p-5 flex flex-col gap-3 hover:shadow-lg transition">
    <div class="flex items-start justify-between gap-2">
      <UiBadge tone="blue">{{ dashboard.category.name }}</UiBadge>
      <UiBadge tone="gray">{{ dashboard.accessLevel }}</UiBadge>
    </div>

    <div>
      <h3 class="font-semibold text-ink text-lg leading-snug">
        {{ dashboard.title }}
      </h3>
      <p class="text-sm text-muted mt-1 line-clamp-2">
        {{ dashboard.description }}
      </p>
    </div>

    <div class="flex flex-wrap gap-1.5">
      <span
        v-for="tag in dashboard.tags.slice(0, 4)"
        :key="tag"
        class="text-xs text-muted bg-brand-light rounded-md px-2 py-0.5"
      >
        #{{ tag }}
      </span>
    </div>

    <div class="flex items-center justify-between text-xs text-muted mt-1">
      <span>{{ dashboard.sheetCount }} sheets</span>
      <span>Updated {{ updated }}</span>
    </div>

    <NuxtLink :to="`/dashboards/${dashboard.slug}`" class="btn-primary mt-1">
      Open Dashboard
    </NuxtLink>
  </div>
</template>
