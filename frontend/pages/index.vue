<script setup lang="ts">
const features = [
  {
    title: "Dashboard Catalog",
    text: "Organize all analytics dashboards by category, owner, access level, and business purpose.",
  },
  {
    title: "Interactive Analytics",
    text: "Use KPI cards, charts, tables, filters, and dashboard sheets to explore demo business data.",
  },
  {
    title: "Learning Materials",
    text: "Attach instructions, video lessons, presentations, FAQ, and metric explanations to every dashboard.",
  },
  {
    title: "Role-Based Access",
    text: "Control who can view, edit, export, and manage dashboards.",
  },
  {
    title: "Admin Management",
    text: "Create categories, dashboards, sheets, widgets, learning materials, users, roles, and permissions.",
  },
  {
    title: "Future Enterprise Deployment",
    text: "Prepare the platform for internal company networks, VPN-only access, and private infrastructure.",
  },
];

const categories = [
  "Revenue", "Orders", "BIN Analytics", "Contacts",
  "Education & Healthcare", "Provider SpeedTest", "Government Procurement",
  "Sales Tools", "AI Tools", "Instructions",
];
</script>

<template>
  <div>
    <!-- Hero -->
    <section
      class="relative overflow-hidden bg-gradient-to-br from-brand-deep
             via-brand-primary to-brand-cyan text-white"
    >
      <div class="max-w-6xl mx-auto px-6 py-20 md:py-28">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span
              class="inline-block bg-white/15 rounded-full px-3 py-1 text-sm
                     font-medium mb-5"
            >
              Independent Corporate BI Platform
            </span>
            <h1 class="text-4xl md:text-5xl font-extrabold leading-tight">
              Corporate analytics, dashboards, and learning materials in one
              secure platform.
            </h1>
            <p class="mt-5 text-lg text-white/90 max-w-xl">
              Build a single internal workspace where employees can explore
              dashboards, switch between sheets, filter data, export tables, and
              learn how to use every report.
            </p>
            <div class="mt-8 flex flex-wrap gap-3">
              <NuxtLink to="/login" class="btn bg-white text-brand-deep
                       hover:bg-brand-light font-semibold">
                Open Platform
              </NuxtLink>
              <NuxtLink to="/login" class="btn border border-white/40 text-white
                       hover:bg-white/10">
                Explore Dashboards
              </NuxtLink>
            </div>
          </div>

          <div class="relative">
            <div class="card p-6 text-ink rotate-1">
              <div class="flex gap-3 mb-4">
                <div class="flex-1 bg-brand-light rounded-xl p-3">
                  <p class="text-xs text-muted">Total Revenue</p>
                  <p class="text-xl font-bold">₸ 125M</p>
                </div>
                <div class="flex-1 bg-brand-light rounded-xl p-3">
                  <p class="text-xs text-muted">Orders</p>
                  <p class="text-xl font-bold">1,204</p>
                </div>
              </div>
              <div class="h-32 flex items-end gap-2">
                <div
                  v-for="(h, i) in [60, 80, 45, 95, 70, 88]"
                  :key="i"
                  class="flex-1 rounded-t-lg bg-gradient-to-t from-brand-primary
                         to-brand-cyan"
                  :style="{ height: h + '%' }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="max-w-6xl mx-auto px-6 py-20">
      <h2 class="text-3xl font-bold text-center text-ink">
        Everything your analytics needs
      </h2>
      <p class="text-muted text-center mt-2">
        A clean BI workspace structured for non-technical employees.
      </p>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
        <div v-for="f in features" :key="f.title" class="card p-6">
          <div
            class="h-10 w-10 rounded-xl bg-brand-light text-brand-deep flex
                   items-center justify-center font-bold mb-3"
          >
            ✦
          </div>
          <h3 class="font-semibold text-ink">{{ f.title }}</h3>
          <p class="text-sm text-muted mt-1.5">{{ f.text }}</p>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="bg-white border-y border-cardborder">
      <div class="max-w-6xl mx-auto px-6 py-16">
        <h2 class="text-2xl font-bold text-ink text-center">
          Dashboard categories
        </h2>
        <div class="flex flex-wrap justify-center gap-3 mt-8">
          <span
            v-for="c in categories"
            :key="c"
            class="rounded-full bg-brand-light text-brand-deep px-4 py-2 text-sm
                   font-medium"
          >
            {{ c }}
          </span>
        </div>
      </div>
    </section>

    <!-- Enterprise -->
    <section class="max-w-6xl mx-auto px-6 py-20 text-center">
      <h2 class="text-3xl font-bold text-ink">Ready for enterprise deployment</h2>
      <p class="text-muted mt-3 max-w-2xl mx-auto">
        Start with demo data today, then deploy inside an internal company network
        with VPN-only access, SSO, and private infrastructure when you are ready.
      </p>
      <NuxtLink to="/login" class="btn-primary mt-8">Open Platform</NuxtLink>
    </section>

    <footer class="bg-ink text-white/70 py-8 text-center text-sm">
      Analytics &amp; Learning Platform — demo prototype with fake data only.
    </footer>
  </div>
</template>
