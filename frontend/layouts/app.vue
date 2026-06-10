<template>
  <div class="flex min-h-screen bg-brand-light">
    <AppSidebar />
    <div class="flex-1 flex flex-col min-w-0">
      <AppTopbar />
      <main class="flex-1 px-4 md:px-8 py-6 md:py-8">
        <slot />
      </main>
    </div>
  </div>
</template>
