<script setup lang="ts">
import type { Category } from "~/types";

export interface DashboardFormData {
  title: string;
  slug: string;
  description: string;
  businessPurpose: string;
  reportUrl: string;
  reportKind: string;
  categoryId: number | null;
  accessLevel: string;
  status: string;
  tags: string;
}

const props = defineProps<{
  modelValue: DashboardFormData;
  categories: Category[];
  submitting?: boolean;
  submitLabel?: string;
}>();
const emit = defineEmits<{
  "update:modelValue": [DashboardFormData];
  submit: [];
}>();

const accessLevels = [
  "ADMIN_ONLY", "ANALYST_ONLY", "MANAGER", "EMPLOYEE", "PUBLIC_INTERNAL",
];
const statuses = ["DRAFT", "PUBLISHED", "ARCHIVED"];
const reportKinds = ["QLIK", "WEB", "BOT"];

function update<K extends keyof DashboardFormData>(
  key: K,
  value: DashboardFormData[K],
) {
  emit("update:modelValue", { ...props.modelValue, [key]: value });
}
</script>

<template>
  <form class="card p-6 space-y-4 max-w-2xl" @submit.prevent="emit('submit')">
    <div>
      <label class="label">Title *</label>
      <input
        :value="modelValue.title"
        class="input"
        required
        @input="update('title', ($event.target as HTMLInputElement).value)"
      />
    </div>
    <div>
      <label class="label">Slug *</label>
      <input
        :value="modelValue.slug"
        class="input"
        required
        placeholder="revenue-overview"
        @input="update('slug', ($event.target as HTMLInputElement).value)"
      />
    </div>
    <div>
      <label class="label">Description</label>
      <textarea
        :value="modelValue.description"
        class="input"
        rows="2"
        @input="update('description', ($event.target as HTMLTextAreaElement).value)"
      />
    </div>
    <div>
      <label class="label">Business purpose</label>
      <textarea
        :value="modelValue.businessPurpose"
        class="input"
        rows="2"
        @input="update('businessPurpose', ($event.target as HTMLTextAreaElement).value)"
      />
    </div>
    <div class="grid sm:grid-cols-3 gap-4">
      <div class="sm:col-span-2">
        <label class="label">Report URL</label>
        <input
          :value="modelValue.reportUrl"
          class="input"
          placeholder="https://qtest/sense/app/…/overview"
          @input="update('reportUrl', ($event.target as HTMLInputElement).value)"
        />
      </div>
      <div>
        <label class="label">Report kind</label>
        <select
          :value="modelValue.reportKind"
          class="input"
          @change="update('reportKind', ($event.target as HTMLSelectElement).value)"
        >
          <option v-for="k in reportKinds" :key="k" :value="k">{{ k }}</option>
        </select>
      </div>
    </div>
    <div class="grid sm:grid-cols-2 gap-4">
      <div>
        <label class="label">Category *</label>
        <select
          :value="modelValue.categoryId ?? ''"
          class="input"
          required
          @change="update('categoryId', Number(($event.target as HTMLSelectElement).value))"
        >
          <option value="" disabled>Select category</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </div>
      <div>
        <label class="label">Access level *</label>
        <select
          :value="modelValue.accessLevel"
          class="input"
          @change="update('accessLevel', ($event.target as HTMLSelectElement).value)"
        >
          <option v-for="a in accessLevels" :key="a" :value="a">{{ a }}</option>
        </select>
      </div>
    </div>
    <div class="grid sm:grid-cols-2 gap-4">
      <div>
        <label class="label">Status *</label>
        <select
          :value="modelValue.status"
          class="input"
          @change="update('status', ($event.target as HTMLSelectElement).value)"
        >
          <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div>
        <label class="label">Tags (comma-separated)</label>
        <input
          :value="modelValue.tags"
          class="input"
          placeholder="revenue, regions"
          @input="update('tags', ($event.target as HTMLInputElement).value)"
        />
      </div>
    </div>

    <div class="flex gap-3 pt-2">
      <button type="submit" class="btn-primary" :disabled="submitting">
        {{ submitting ? "Saving…" : submitLabel || "Save" }}
      </button>
      <NuxtLink to="/admin/dashboards" class="btn-secondary">Cancel</NuxtLink>
    </div>
  </form>
</template>
