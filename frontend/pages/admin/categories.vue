<script setup lang="ts">
import type { Category } from "~/types";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const categories = ref<Category[]>([]);
const loading = ref(true);
const error = ref("");

const form = reactive({ name: "", slug: "", description: "", icon: "" });

async function load() {
  loading.value = true;
  try {
    const res = await api<Category[]>("/categories");
    categories.value = res.data;
  } finally {
    loading.value = false;
  }
}

async function create() {
  error.value = "";
  try {
    await api("/admin/categories", { method: "POST", body: { ...form } });
    form.name = form.slug = form.description = form.icon = "";
    await load();
  } catch (e: any) {
    error.value = e?.data?.message || "Could not create category.";
  }
}

async function archive(c: Category) {
  if (!confirm(`Archive category "${c.name}"?`)) return;
  await api(`/admin/categories/${c.id}`, { method: "DELETE" });
  await load();
}

onMounted(load);
</script>

<template>
  <div>
    <PageHeader title="Categories" subtitle="Manage dashboard categories." />

    <div class="grid lg:grid-cols-3 gap-6">
      <form class="card p-6 space-y-3 h-fit" @submit.prevent="create">
        <h3 class="font-semibold text-ink">New category</h3>
        <div>
          <label class="label">Name *</label>
          <input v-model="form.name" class="input" required />
        </div>
        <div>
          <label class="label">Slug *</label>
          <input v-model="form.slug" class="input" required placeholder="revenue" />
        </div>
        <div>
          <label class="label">Description</label>
          <input v-model="form.description" class="input" />
        </div>
        <div>
          <label class="label">Icon</label>
          <input v-model="form.icon" class="input" placeholder="chart-line" />
        </div>
        <p v-if="error" class="text-danger text-sm">{{ error }}</p>
        <button type="submit" class="btn-primary w-full">Create category</button>
      </form>

      <div class="lg:col-span-2">
        <StateBlocks v-if="loading" variant="loading" />
        <div v-else class="card overflow-hidden">
          <table class="w-full text-sm">
            <thead class="bg-brand-light text-ink">
              <tr>
                <th class="text-left px-4 py-3 font-semibold">Name</th>
                <th class="text-left px-4 py-3 font-semibold">Slug</th>
                <th class="text-left px-4 py-3 font-semibold">Dashboards</th>
                <th class="text-right px-4 py-3 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="c in categories"
                :key="c.id"
                class="border-t border-cardborder"
              >
                <td class="px-4 py-3 text-ink font-medium">{{ c.name }}</td>
                <td class="px-4 py-3 text-muted">{{ c.slug }}</td>
                <td class="px-4 py-3 text-muted">{{ c.dashboardCount ?? 0 }}</td>
                <td class="px-4 py-3 text-right">
                  <button class="text-danger font-medium" @click="archive(c)">
                    Archive
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
