<script setup lang="ts">
const auth = useAuthStore();
const search = ref("");

function submitSearch() {
  if (!search.value.trim()) return;
  navigateTo({ path: "/dashboards", query: { search: search.value.trim() } });
}

const initials = computed(() => {
  const name = auth.user?.fullName ?? "U";
  return name.split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();
});
</script>

<template>
  <header
    class="sticky top-0 z-10 flex items-center gap-4 bg-white/80 backdrop-blur
           border-b border-cardborder px-4 md:px-8 h-16"
  >
    <form class="flex-1 max-w-lg" @submit.prevent="submitSearch">
      <input
        v-model="search"
        type="search"
        placeholder="Search dashboards…"
        class="input"
      />
    </form>

    <div class="ml-auto flex items-center gap-3">
      <div class="text-right hidden sm:block">
        <p class="text-sm font-semibold text-ink leading-tight">
          {{ auth.user?.fullName }}
        </p>
        <p class="text-xs text-muted">{{ auth.roles.join(", ") }}</p>
      </div>
      <div
        class="h-9 w-9 rounded-full bg-brand-deep text-white flex items-center
               justify-center text-sm font-semibold"
      >
        {{ initials }}
      </div>
    </div>
  </header>
</template>
