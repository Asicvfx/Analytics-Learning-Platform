<script setup lang="ts">
import type { Kpi } from "~/types";

const props = defineProps<{ kpi: Kpi }>();

const formatted = computed(() => {
  const v = props.kpi.value ?? 0;
  if (props.kpi.format === "currency") {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "KZT",
      maximumFractionDigits: 0,
    }).format(v);
  }
  return new Intl.NumberFormat("en-US").format(v);
});
</script>

<template>
  <div class="card p-5">
    <p class="text-sm text-muted">{{ kpi.label }}</p>
    <p class="text-2xl font-bold text-ink mt-1">{{ formatted }}</p>
  </div>
</template>
