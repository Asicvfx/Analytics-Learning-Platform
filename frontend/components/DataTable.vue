<script setup lang="ts">
import type { TableColumn } from "~/types";

const props = defineProps<{
  columns: TableColumn[];
  rows: Record<string, any>[];
  pageSize?: number;
}>();

const page = ref(0);
const sortKey = ref<string | null>(null);
const sortDir = ref<"asc" | "desc">("asc");
const size = computed(() => props.pageSize ?? 10);

const sortedRows = computed(() => {
  if (!sortKey.value) return props.rows;
  const key = sortKey.value;
  const dir = sortDir.value === "asc" ? 1 : -1;
  return [...props.rows].sort((a, b) => {
    if (a[key] < b[key]) return -1 * dir;
    if (a[key] > b[key]) return 1 * dir;
    return 0;
  });
});

const totalPages = computed(() =>
  Math.max(1, Math.ceil(sortedRows.value.length / size.value)),
);
const pagedRows = computed(() =>
  sortedRows.value.slice(page.value * size.value, (page.value + 1) * size.value),
);

function toggleSort(key: string) {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = key;
    sortDir.value = "asc";
  }
}

watch(() => props.rows, () => (page.value = 0));
</script>

<template>
  <div class="card overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-brand-light text-ink">
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              class="text-left font-semibold px-4 py-3 cursor-pointer select-none
                     whitespace-nowrap"
              @click="toggleSort(col.key)"
            >
              {{ col.label }}
              <span v-if="sortKey === col.key" class="text-brand-primary">
                {{ sortDir === "asc" ? "▲" : "▼" }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in pagedRows"
            :key="i"
            class="border-t border-cardborder hover:bg-brand-light/50"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-3 text-ink whitespace-nowrap"
            >
              {{ row[col.key] }}
            </td>
          </tr>
          <tr v-if="!pagedRows.length">
            <td :colspan="columns.length" class="px-4 py-8 text-center text-muted">
              No data available for the selected filters.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="totalPages > 1"
      class="flex items-center justify-between px-4 py-3 border-t border-cardborder
             text-sm text-muted"
    >
      <span>Page {{ page + 1 }} of {{ totalPages }}</span>
      <div class="flex gap-2">
        <button
          class="btn-secondary px-3 py-1.5"
          :disabled="page === 0"
          @click="page--"
        >
          Prev
        </button>
        <button
          class="btn-secondary px-3 py-1.5"
          :disabled="page >= totalPages - 1"
          @click="page++"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
