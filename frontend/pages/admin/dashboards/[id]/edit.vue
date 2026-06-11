<script setup lang="ts">
import type { Category, DashboardDetail } from "~/types";
import type { DashboardFormData } from "~/components/AdminDashboardForm.vue";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const route = useRoute();
const id = route.params.id as string;

const categories = ref<Category[]>([]);
const loading = ref(true);
const submitting = ref(false);
const error = ref("");

const form = reactive<DashboardFormData>({
  title: "",
  slug: "",
  description: "",
  businessPurpose: "",
  reportUrl: "",
  reportKind: "QLIK",
  categoryId: null,
  accessLevel: "EMPLOYEE",
  status: "DRAFT",
  tags: "",
});

async function submit() {
  error.value = "";
  submitting.value = true;
  try {
    await api(`/admin/dashboards/${id}`, {
      method: "PUT",
      body: {
        title: form.title,
        slug: form.slug,
        description: form.description,
        businessPurpose: form.businessPurpose,
        reportUrl: form.reportUrl,
        reportKind: form.reportKind,
        categoryId: form.categoryId,
        accessLevel: form.accessLevel,
        status: form.status,
        tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
      },
    });
    await navigateTo("/admin/dashboards");
  } catch (e: any) {
    error.value = e?.data?.message || "Could not update dashboard.";
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  const [cat, dash] = await Promise.all([
    api<Category[]>("/categories?active=true"),
    api<DashboardDetail>(`/dashboards/${id}`),
  ]);
  categories.value = cat.data;
  const d = dash.data;
  form.title = d.title;
  form.slug = d.slug;
  form.description = d.description;
  form.businessPurpose = d.businessPurpose;
  form.reportUrl = d.reportUrl;
  form.reportKind = d.reportKind;
  form.categoryId = d.category.id;
  form.accessLevel = d.accessLevel;
  form.status = d.status;
  form.tags = d.tags.join(", ");
  loading.value = false;
});
</script>

<template>
  <div>
    <PageHeader title="Edit dashboard" subtitle="Update dashboard details." />
    <StateBlocks v-if="loading" variant="loading" />
    <template v-else>
      <p v-if="error" class="text-danger mb-3">{{ error }}</p>
      <AdminDashboardForm
        v-model="form"
        :categories="categories"
        :submitting="submitting"
        submit-label="Save changes"
        @submit="submit"
      />
    </template>
  </div>
</template>
