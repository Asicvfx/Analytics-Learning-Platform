<script setup lang="ts">
import type { LearningMaterial } from "~/types";

defineProps<{ material: LearningMaterial | null }>();
</script>

<template>
  <div v-if="material" class="grid lg:grid-cols-3 gap-5">
    <div class="card p-6 lg:col-span-2">
      <h2 class="text-lg font-semibold text-ink">{{ material.title }}</h2>
      <p class="text-ink/80 mt-3 whitespace-pre-line">{{ material.content }}</p>

      <div v-if="material.faq?.length" class="mt-6">
        <h3 class="font-semibold text-ink mb-2">FAQ</h3>
        <div class="space-y-3">
          <div
            v-for="(f, i) in material.faq"
            :key="i"
            class="rounded-xl bg-brand-light p-4"
          >
            <p class="font-medium text-ink">{{ f.question }}</p>
            <p class="text-sm text-muted mt-1">{{ f.answer }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <a
        v-if="material.videoUrl"
        :href="material.videoUrl"
        target="_blank"
        rel="noopener"
        class="card p-5 block hover:shadow-lg transition"
      >
        <p class="font-semibold text-ink">▶ Видеоурок</p>
        <p class="text-sm text-muted mt-1">Посмотрите, как пользоваться отчётом.</p>
      </a>
      <a
        v-if="material.presentationUrl"
        :href="material.presentationUrl"
        target="_blank"
        rel="noopener"
        class="card p-5 block hover:shadow-lg transition"
      >
        <p class="font-semibold text-ink">📊 Презентация</p>
        <p class="text-sm text-muted mt-1">Откройте презентацию отчёта.</p>
      </a>
    </div>
  </div>

  <StateBlocks
    v-else
    variant="empty"
    title="Материалы пока не добавлены"
    message="Для этого отчёта ещё нет инструкции."
  />
</template>
