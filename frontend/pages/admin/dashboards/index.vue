<script setup lang="ts">
import type { DashboardCard } from "~/types";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const dashboards = ref<DashboardCard[]>([]);
const loading = ref(true);

async function load() {
  loading.value = true;
  try {
    const res = await api<DashboardCard[]>("/dashboards?size=100");
    dashboards.value = res.data;
  } finally {
    loading.value = false;
  }
}

async function archive(d: DashboardCard) {
  if (!confirm(`Archive "${d.title}"? Users will no longer see it in the catalog.`))
    return;
  await api(`/admin/dashboards/${d.id}`, { method: "DELETE" });
  await load();
}

onMounted(load);
</script>

<template>
  <div>
    <PageHeader title="Dashboards" subtitle="Manage all dashboards.">
      <template #actions>
        <NuxtLink to="/admin/dashboards/new" class="btn-primary">
          Create Dashboard
        </NuxtLink>
      </template>
    </PageHeader>

    <StateBlocks v-if="loading" variant="loading" />
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-brand-light text-ink">
          <tr>
            <th class="text-left px-4 py-3 font-semibold">Title</th>
            <th class="text-left px-4 py-3 font-semibold">Category</th>
            <th class="text-left px-4 py-3 font-semibold">Access</th>
            <th class="text-left px-4 py-3 font-semibold">Status</th>
            <th class="text-right px-4 py-3 font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="d in dashboards"
            :key="d.id"
            class="border-t border-cardborder"
          >
            <td class="px-4 py-3 text-ink font-medium">{{ d.title }}</td>
            <td class="px-4 py-3 text-muted">{{ d.category.name }}</td>
            <td class="px-4 py-3"><UiBadge tone="gray">{{ d.accessLevel }}</UiBadge></td>
            <td class="px-4 py-3"><UiBadge tone="green">{{ d.status }}</UiBadge></td>
            <td class="px-4 py-3 text-right space-x-2">
              <NuxtLink
                :to="`/admin/dashboards/${d.id}/edit`"
                class="text-brand-deep font-medium"
              >
                Edit
              </NuxtLink>
              <button class="text-danger font-medium" @click="archive(d)">
                Archive
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
