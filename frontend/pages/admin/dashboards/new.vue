<script setup lang="ts">
import type { Category } from "~/types";
import type { DashboardFormData } from "~/components/AdminDashboardForm.vue";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const categories = ref<Category[]>([]);
const submitting = ref(false);
const error = ref("");

const form = reactive<DashboardFormData>({
  title: "",
  slug: "",
  description: "",
  businessPurpose: "",
  categoryId: null,
  accessLevel: "EMPLOYEE",
  status: "DRAFT",
  tags: "",
});

async function submit() {
  error.value = "";
  submitting.value = true;
  try {
    await api("/admin/dashboards", {
      method: "POST",
      body: {
        title: form.title,
        slug: form.slug,
        description: form.description,
        businessPurpose: form.businessPurpose,
        categoryId: form.categoryId,
        accessLevel: form.accessLevel,
        status: form.status,
        tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
      },
    });
    await navigateTo("/admin/dashboards");
  } catch (e: any) {
    error.value = e?.data?.message || "Could not create dashboard.";
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  const res = await api<Category[]>("/categories?active=true");
  categories.value = res.data;
});
</script>

<template>
  <div>
    <PageHeader title="Create dashboard" subtitle="Add a new dashboard." />
    <p v-if="error" class="text-danger mb-3">{{ error }}</p>
    <AdminDashboardForm
      v-model="form"
      :categories="categories"
      :submitting="submitting"
      submit-label="Create dashboard"
      @submit="submit"
    />
  </div>
</template>
