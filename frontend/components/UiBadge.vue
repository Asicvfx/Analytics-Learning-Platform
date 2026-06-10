<script setup lang="ts">
const props = defineProps<{ tone?: "blue" | "green" | "amber" | "gray" }>();
const tones: Record<string, string> = {
  blue: "bg-brand-light text-brand-deep",
  green: "bg-emerald-50 text-emerald-700",
  amber: "bg-amber-50 text-amber-700",
  gray: "bg-slate-100 text-slate-600",
};
const cls = computed(() => tones[props.tone || "blue"]);
</script>

<template>
  <span
    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
    :class="cls"
  >
    <slot />
  </span>
</template>
