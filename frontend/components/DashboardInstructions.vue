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
        <p class="font-semibold text-ink">▶ Video lesson</p>
        <p class="text-sm text-muted mt-1">Watch how to use this dashboard.</p>
      </a>
      <a
        v-if="material.presentationUrl"
        :href="material.presentationUrl"
        target="_blank"
        rel="noopener"
        class="card p-5 block hover:shadow-lg transition"
      >
        <p class="font-semibold text-ink">📊 Presentation</p>
        <p class="text-sm text-muted mt-1">Open the dashboard presentation.</p>
      </a>
    </div>
  </div>

  <StateBlocks
    v-else
    variant="empty"
    title="No instructions yet"
    message="Learning materials have not been added for this dashboard."
  />
</template>
