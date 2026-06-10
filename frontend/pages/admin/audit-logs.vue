<script setup lang="ts">
import type { AuditLog } from "~/types";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const logs = ref<AuditLog[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api<AuditLog[]>("/admin/audit-logs?size=100");
    logs.value = res.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <PageHeader title="Audit logs" subtitle="Important actions across the platform." />
    <StateBlocks v-if="loading" variant="loading" />
    <StateBlocks
      v-else-if="!logs.length"
      variant="empty"
      title="No audit logs yet"
    />
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-brand-light text-ink">
          <tr>
            <th class="text-left px-4 py-3 font-semibold">User</th>
            <th class="text-left px-4 py-3 font-semibold">Action</th>
            <th class="text-left px-4 py-3 font-semibold">Target</th>
            <th class="text-left px-4 py-3 font-semibold">IP</th>
            <th class="text-left px-4 py-3 font-semibold">When</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="l in logs" :key="l.id" class="border-t border-cardborder">
            <td class="px-4 py-3 text-ink">{{ l.user?.fullName || "—" }}</td>
            <td class="px-4 py-3">
              <UiBadge tone="blue">{{ l.action }}</UiBadge>
            </td>
            <td class="px-4 py-3 text-muted">
              {{ l.targetType }}{{ l.targetId ? " #" + l.targetId : "" }}
            </td>
            <td class="px-4 py-3 text-muted">{{ l.ipAddress || "—" }}</td>
            <td class="px-4 py-3 text-muted">
              {{ new Date(l.createdAt).toLocaleString() }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
