<script setup lang="ts">
import type { DashboardData, DashboardDetail } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api, exportUrl, authHeader } = useApi();
const route = useRoute();
const slug = route.params.id as string;

const detail = ref<DashboardDetail | null>(null);
const data = ref<DashboardData | null>(null);
const loading = ref(true);
const loadingData = ref(false);
const error = ref("");
const activeTab = ref<string>("");
const exporting = ref(false);

const filters = reactive({
  dateFrom: "",
  dateTo: "",
  region: "",
  status: "",
});

const regions = ["Almaty", "Astana", "Shymkent", "Karaganda", "Aktobe"];

function buildQuery() {
  const p = new URLSearchParams();
  Object.entries(filters).forEach(([k, v]) => {
    if (v) p.set(k, v);
  });
  return p.toString();
}

async function loadData() {
  loadingData.value = true;
  try {
    const res = await api<DashboardData>(
      `/dashboards/${slug}/data?${buildQuery()}`,
    );
    data.value = res.data;
  } finally {
    loadingData.value = false;
  }
}

function resetFilters() {
  filters.dateFrom = "";
  filters.dateTo = "";
  filters.region = "";
  filters.status = "";
  loadData();
}

async function exportCsv() {
  exporting.value = true;
  try {
    const res = await fetch(
      exportUrl(`/dashboards/${slug}/export.csv?${buildQuery()}`),
      { headers: authHeader() },
    );
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      alert(body.message || "Export failed.");
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${slug}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  } finally {
    exporting.value = false;
  }
}

const isInstructions = computed(() => activeTab.value === "__instructions");

onMounted(async () => {
  try {
    const res = await api<DashboardDetail>(`/dashboards/${slug}`);
    detail.value = res.data;
    activeTab.value = res.data.sheets[0]?.slug || "__instructions";
    await loadData();
  } catch (e: any) {
    error.value = e?.data?.message || "Dashboard not found.";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <StateBlocks v-if="loading" variant="loading" />
    <StateBlocks
      v-else-if="error"
      variant="error"
      title="Unable to open dashboard"
      :message="error"
    />

    <template v-else-if="detail">
      <!-- Header -->
      <div class="card p-6 mb-6">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <UiBadge tone="blue">{{ detail.category.name }}</UiBadge>
              <UiBadge tone="gray">{{ detail.accessLevel }}</UiBadge>
            </div>
            <h1 class="text-2xl font-bold text-ink">{{ detail.title }}</h1>
            <p class="text-muted mt-1 max-w-2xl">{{ detail.description }}</p>
            <p class="text-sm text-muted mt-2">
              Owner: <span class="text-ink">{{ detail.ownerName || "—" }}</span>
              · Updated
              {{
                detail.lastUpdatedAt
                  ? new Date(detail.lastUpdatedAt).toLocaleDateString()
                  : "—"
              }}
            </p>
          </div>
          <button class="btn-primary" :disabled="exporting" @click="exportCsv">
            {{ exporting ? "Exporting…" : "Export CSV" }}
          </button>
        </div>
      </div>

      <!-- Sheet tabs -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button
          v-for="sheet in detail.sheets"
          :key="sheet.id"
          class="px-4 py-2 rounded-xl text-sm font-medium transition"
          :class="
            activeTab === sheet.slug
              ? 'bg-brand-primary text-white'
              : 'bg-white border border-cardborder text-muted hover:text-brand-deep'
          "
          @click="activeTab = sheet.slug"
        >
          {{ sheet.title }}
        </button>
        <button
          class="px-4 py-2 rounded-xl text-sm font-medium transition"
          :class="
            isInstructions
              ? 'bg-brand-primary text-white'
              : 'bg-white border border-cardborder text-muted hover:text-brand-deep'
          "
          @click="activeTab = '__instructions'"
        >
          Instructions
        </button>
      </div>

      <!-- Instructions tab -->
      <DashboardInstructions
        v-if="isInstructions"
        :material="detail.learningMaterial"
      />

      <!-- Analytics tab -->
      <template v-else>
        <!-- Filters -->
        <div class="card p-4 mb-6 flex flex-wrap gap-3 items-end">
          <div>
            <label class="label">Date from</label>
            <input v-model="filters.dateFrom" type="date" class="input" />
          </div>
          <div>
            <label class="label">Date to</label>
            <input v-model="filters.dateTo" type="date" class="input" />
          </div>
          <div class="min-w-[160px]">
            <label class="label">Region</label>
            <select v-model="filters.region" class="input">
              <option value="">All regions</option>
              <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>
          <button class="btn-primary" @click="loadData">Apply filters</button>
          <button class="btn-secondary" @click="resetFilters">Reset filters</button>
        </div>

        <StateBlocks v-if="loadingData" variant="loading" />
        <template v-else-if="data">
          <!-- KPI -->
          <div
            v-if="data.kpis.length"
            class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
          >
            <KpiCard v-for="k in data.kpis" :key="k.key" :kpi="k" />
          </div>

          <!-- Charts -->
          <div
            v-if="data.charts.length"
            class="grid lg:grid-cols-2 gap-5 mb-6"
          >
            <ChartCard
              v-for="(c, i) in data.charts"
              :key="i"
              :chart="c"
            />
          </div>

          <!-- Table -->
          <DataTable
            :columns="data.table.columns"
            :rows="data.table.rows"
          />
        </template>
      </template>
    </template>
  </div>
</template>
