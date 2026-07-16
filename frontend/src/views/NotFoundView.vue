<template>
  <AppLayout>
    <div class="not-found-page">
      <div class="container not-found-inner">
        <div class="not-found-visual">
          <span class="not-found-code">404</span>
          <span class="not-found-icon">🔍</span>
        </div>
        <h1 class="not-found-title">Page introuvable</h1>
        <p class="not-found-desc">
          La page que vous cherchez n'existe pas ou a été déplacée.
        </p>
        <div class="not-found-actions">
          <RouterLink to="/" class="btn btn-primary btn-lg">Retour à l'accueil</RouterLink>
          <RouterLink to="/contact" class="btn btn-outline btn-lg">Nous contacter</RouterLink>
        </div>
        <div class="not-found-links">
          <strong>Vous cherchiez peut-être :</strong>
          <div class="quick-links">
            <RouterLink to="/formations" class="quick-link">🎓 Formations</RouterLink>
            <RouterLink to="/boutique" class="quick-link">🛒 Boutique</RouterLink>
            <RouterLink to="/services" class="quick-link">⚙️ Services</RouterLink>
            <RouterLink to="/a-propos" class="quick-link">🏢 À Propos</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
<script setup>
import AppLayout from "@/components/common/AppLayout.vue";
</script>
<style scoped>
.not-found-page{min-height:70vh;display:flex;align-items:center;padding:4rem 0}
.not-found-inner{text-align:center;max-width:600px;margin:auto}
.not-found-visual{position:relative;display:inline-block;margin-bottom:2rem}
.not-found-code{font-family:var(--font-heading);font-size:8rem;font-weight:900;color:var(--color-primary-50);line-height:1;display:block}
.not-found-icon{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:3.5rem}
.not-found-title{font-size:2rem;font-weight:800;color:var(--color-primary-dark);margin-bottom:.75rem}
.not-found-desc{color:var(--color-neutral-600);margin-bottom:2rem;font-size:1.05rem}
.not-found-actions{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:3rem}
.not-found-links strong{display:block;font-size:.875rem;color:var(--color-neutral-600);margin-bottom:1rem}
.quick-links{display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap}
.quick-link{display:flex;align-items:center;gap:.4rem;padding:.5rem 1rem;background:var(--color-neutral-50);border:1px solid var(--color-neutral-200);border-radius:999px;font-size:.875rem;color:var(--color-neutral-700);text-decoration:none;transition:all var(--transition-fast)}
.quick-link:hover{background:var(--color-primary-50);border-color:var(--color-primary-100);color:var(--color-primary)}
</style>
