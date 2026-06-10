<script setup lang="ts">
defineProps<{
  variant: "loading" | "empty" | "error";
  title?: string;
  message?: string;
}>();
</script>

<template>
  <div class="card flex flex-col items-center justify-center text-center py-16 px-6">
    <div
      v-if="variant === 'loading'"
      class="h-8 w-8 rounded-full border-2 border-brand-primary border-t-transparent
             animate-spin mb-4"
    />
    <div
      v-else
      class="h-12 w-12 rounded-2xl bg-brand-light flex items-center justify-center
             mb-4 text-2xl"
    >
      {{ variant === "error" ? "⚠️" : "📭" }}
    </div>
    <p class="font-semibold text-ink">
      {{ title || (variant === "loading" ? "Loading…" : "Nothing here") }}
    </p>
    <p v-if="message" class="text-muted text-sm mt-1 max-w-md">{{ message }}</p>
  </div>
</template>
