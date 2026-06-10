<script setup lang="ts">
import type { User } from "~/types";

definePageMeta({ layout: "app", middleware: "admin" });

const { api } = useApi();
const users = ref<User[]>([]);
const loading = ref(true);
const error = ref("");

const roles = ["ADMIN", "ANALYST", "MANAGER", "EMPLOYEE"];
const form = reactive({
  fullName: "",
  email: "",
  password: "",
  role: "EMPLOYEE",
  department: "",
});

async function load() {
  loading.value = true;
  try {
    const res = await api<User[]>("/admin/users?size=100");
    users.value = res.data;
  } finally {
    loading.value = false;
  }
}

async function create() {
  error.value = "";
  try {
    await api("/admin/users", {
      method: "POST",
      body: {
        fullName: form.fullName,
        email: form.email,
        password: form.password,
        roles: [form.role],
        department: form.department,
      },
    });
    form.fullName = form.email = form.password = form.department = "";
    await load();
  } catch (e: any) {
    error.value = e?.data?.message || "Could not create user.";
  }
}

onMounted(load);
</script>

<template>
  <div>
    <PageHeader title="Users" subtitle="Manage users and roles." />

    <div class="grid lg:grid-cols-3 gap-6">
      <form class="card p-6 space-y-3 h-fit" @submit.prevent="create">
        <h3 class="font-semibold text-ink">New user</h3>
        <div>
          <label class="label">Full name *</label>
          <input v-model="form.fullName" class="input" required />
        </div>
        <div>
          <label class="label">Email *</label>
          <input v-model="form.email" type="email" class="input" required />
        </div>
        <div>
          <label class="label">Password *</label>
          <input v-model="form.password" type="password" class="input" required />
        </div>
        <div>
          <label class="label">Role *</label>
          <select v-model="form.role" class="input">
            <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>
        <div>
          <label class="label">Department</label>
          <input v-model="form.department" class="input" />
        </div>
        <p v-if="error" class="text-danger text-sm">{{ error }}</p>
        <button type="submit" class="btn-primary w-full">Create user</button>
      </form>

      <div class="lg:col-span-2">
        <StateBlocks v-if="loading" variant="loading" />
        <div v-else class="card overflow-hidden">
          <table class="w-full text-sm">
            <thead class="bg-brand-light text-ink">
              <tr>
                <th class="text-left px-4 py-3 font-semibold">Name</th>
                <th class="text-left px-4 py-3 font-semibold">Email</th>
                <th class="text-left px-4 py-3 font-semibold">Roles</th>
                <th class="text-left px-4 py-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="u in users"
                :key="u.id"
                class="border-t border-cardborder"
              >
                <td class="px-4 py-3 text-ink font-medium">{{ u.fullName }}</td>
                <td class="px-4 py-3 text-muted">{{ u.email }}</td>
                <td class="px-4 py-3">
                  <UiBadge v-for="r in u.roles" :key="r" tone="blue">
                    {{ r }}
                  </UiBadge>
                </td>
                <td class="px-4 py-3">
                  <UiBadge :tone="u.status === 'ACTIVE' ? 'green' : 'gray'">
                    {{ u.status }}
                  </UiBadge>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
