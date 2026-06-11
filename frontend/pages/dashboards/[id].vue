<script setup lang="ts">
import type { DashboardDetail } from "~/types";

definePageMeta({ layout: "app", middleware: "auth" });

const { api } = useApi();
const route = useRoute();
const slug = route.params.id as string;

const detail = ref<DashboardDetail | null>(null);
const loading = ref(true);
const error = ref("");

const openLabel = computed(() => {
  switch (detail.value?.reportKind) {
    case "BOT":
      return "Открыть в Telegram";
    case "WEB":
      return "Открыть приложение";
    default:
      return "Открыть в Qlik Sense";
  }
});

onMounted(async () => {
  try {
    const res = await api<DashboardDetail>(`/dashboards/${slug}`);
    detail.value = res.data;
  } catch (e: any) {
    error.value = e?.data?.message || "Отчёт не найден.";
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
      title="Не удалось открыть отчёт"
      :message="error"
    />

    <template v-else-if="detail">
      <!-- Header -->
      <div class="card p-6 mb-6">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <UiBadge tone="blue">{{ detail.category.name }}</UiBadge>
              <UiBadge tone="gray">{{ detail.reportKind }}</UiBadge>
            </div>
            <h1 class="text-2xl font-bold text-ink">{{ detail.title }}</h1>
            <p class="text-muted mt-1 max-w-2xl">{{ detail.description }}</p>
            <p class="text-sm text-muted mt-2">
              Владелец: <span class="text-ink">{{ detail.ownerName || "—" }}</span>
              · Обновлено
              {{
                detail.lastUpdatedAt
                  ? new Date(detail.lastUpdatedAt).toLocaleDateString()
                  : "—"
              }}
            </p>
          </div>

          <div class="text-right">
            <a
              v-if="detail.reportUrl"
              :href="detail.reportUrl"
              target="_blank"
              rel="noopener"
              class="btn-primary inline-block"
            >
              {{ openLabel }} ↗
            </a>
            <span v-else class="text-sm text-muted">Ссылка не задана</span>
            <p
              v-if="detail.reportUrl"
              class="text-xs text-muted mt-2 max-w-[220px]"
            >
              Откроется во внешней системе. Доступ — по учётным данным CDN
              (для qtest/внутренних ресурсов нужна корпоративная сеть).
            </p>
          </div>
        </div>
      </div>

      <!-- Learning materials + FAQ -->
      <DashboardInstructions :material="detail.learningMaterial" />
    </template>
  </div>
</template>
