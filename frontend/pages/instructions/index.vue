<script setup lang="ts">
definePageMeta({ layout: "app", middleware: "auth" });

const guides = [
  {
    title: "How to navigate dashboards",
    text: "Open the Dashboards page, use search or pick a category, then click Open Dashboard.",
  },
  {
    title: "How to switch between sheets",
    text: "Inside a dashboard, use the sheet tabs at the top to move between Overview, Regions, Details, and more.",
  },
  {
    title: "How to use filters",
    text: "Set the date range and region in the filter bar, then click Apply filters. Use Reset filters to clear them.",
  },
  {
    title: "How to export data",
    text: "Click Export CSV on the dashboard. The export respects your current filters and your role permissions.",
  },
  {
    title: "How to read KPI cards",
    text: "KPI cards at the top show headline numbers for the selected period and filters.",
  },
  {
    title: "How to use tables",
    text: "Click a column header to sort. Use pagination at the bottom to browse all rows.",
  },
];
</script>

<template>
  <div>
    <PageHeader
      title="Instructions"
      subtitle="General guidance on how to use the platform."
    />
    <div class="grid sm:grid-cols-2 gap-5">
      <div v-for="g in guides" :key="g.title" class="card p-6">
        <h3 class="font-semibold text-ink">{{ g.title }}</h3>
        <p class="text-sm text-muted mt-1.5">{{ g.text }}</p>
      </div>
    </div>
  </div>
</template>
