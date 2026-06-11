<script setup lang="ts">
const auth = useAuthStore();
const route = useRoute();

interface Item {
  label: string;
  to: string;
  show: () => boolean;
}

const items = computed<Item[]>(() => [
  { label: "Главная", to: "/home", show: () => true },
  { label: "Отчёты", to: "/dashboards", show: () => true },
  { label: "Категории", to: "/categories", show: () => true },
  { label: "Обучающие материалы", to: "/learning", show: () => true },
  { label: "Инструкции", to: "/instructions", show: () => true },
  { label: "Админ-панель", to: "/admin", show: () => auth.canManage },
  { label: "Пользователи", to: "/admin/users", show: () => auth.isAdmin },
  { label: "Журнал аудита", to: "/admin/audit-logs", show: () => auth.isAdmin },
  { label: "Настройки", to: "/settings", show: () => true },
]);

const visible = computed(() => items.value.filter((i) => i.show()));

function isActive(to: string) {
  return route.path === to || (to !== "/home" && route.path.startsWith(to));
}
</script>

<template>
  <aside
    class="hidden md:flex flex-col w-64 shrink-0 bg-white border-r border-cardborder
           min-h-screen px-4 py-6"
  >
    <NuxtLink to="/home" class="flex items-center gap-2 px-2 mb-8">
      <div
        class="h-9 w-9 rounded-xl bg-gradient-to-br from-brand-primary to-brand-deep
               flex items-center justify-center text-white font-bold"
      >
        A
      </div>
      <span class="font-bold text-ink leading-tight">Kazakhtelecom<br />Business BI</span>
    </NuxtLink>

    <nav class="flex flex-col gap-1">
      <NuxtLink
        v-for="item in visible"
        :key="item.to"
        :to="item.to"
        class="rounded-xl px-3 py-2.5 text-sm font-medium transition"
        :class="
          isActive(item.to)
            ? 'bg-brand-light text-brand-deep'
            : 'text-muted hover:bg-brand-light hover:text-brand-deep'
        "
      >
        {{ item.label }}
      </NuxtLink>
    </nav>

    <button
      class="mt-auto rounded-xl px-3 py-2.5 text-sm font-medium text-danger
             hover:bg-red-50 text-left"
      @click="auth.logout()"
    >
      Выйти
    </button>
  </aside>
</template>
