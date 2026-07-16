<template>
  <AppLayout>
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Boutique</h1>
        <p class="page-subtitle">Équipements solaires, électroniques et électrotechniques de qualité professionnelle.</p>
      </div>
    </div>
    <section class="section">
      <div class="container formations-layout">
        <aside class="filters-sidebar">
          <h3 class="filters-title">Catégories</h3>
          <div class="filter-options">
            <label class="filter-option" :class="{ active: !filters.category }">
              <input type="radio" v-model="filters.category" :value="null" @change="loadProducts" /> Toutes
            </label>
            <label v-for="cat in categories" :key="cat.id" class="filter-option">
              <input type="radio" v-model="filters.category" :value="cat.slug" @change="loadProducts" />
              {{ cat.name }} <span class="filter-count">{{ cat.product_count }}</span>
            </label>
          </div>
        </aside>
        <div class="formations-main">
          <div class="content-toolbar">
            <div class="search-wrap">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
              <input v-model="filters.search" @input="debouncedSearch" type="text" class="form-input" placeholder="Rechercher un produit..." style="padding-left:2.5rem" />
            </div>
          </div>
          <div v-if="loading" class="cards-grid">
            <div v-for="i in 6" :key="i" class="card skeleton-card" style="min-height:280px">
              <div class="skeleton" style="height:200px"></div>
              <div style="padding:1rem"><div class="skeleton" style="height:14px;margin-bottom:8px"></div><div class="skeleton" style="height:14px;width:50%"></div></div>
            </div>
          </div>
          <div v-else class="cards-grid">
            <ProductCard v-for="p in products" :key="p.id" :product="p" />
          </div>
          <div v-if="pagination.total_pages > 1" class="pagination">
            <button class="btn btn-outline btn-sm" :disabled="!pagination.previous" @click="changePage(pagination.current_page - 1)">← Précédent</button>
            <span class="page-info">Page {{ pagination.current_page }} / {{ pagination.total_pages }}</span>
            <button class="btn btn-outline btn-sm" :disabled="!pagination.next" @click="changePage(pagination.current_page + 1)">Suivant →</button>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import ProductCard from "@/components/boutique/ProductCard.vue";
import { boutiqueApi } from "@/services/api";
const products = ref([]); const categories = ref([]); const loading = ref(true);
const pagination = reactive({ count:0, total_pages:1, current_page:1, next:null, previous:null });
const filters = reactive({ category:null, search:"", page:1 });
let searchTimer = null;
function debouncedSearch() { clearTimeout(searchTimer); searchTimer = setTimeout(()=>{ filters.page=1; loadProducts(); }, 400); }
async function loadProducts() {
  loading.value = true;
  try {
    const params = { page: filters.page };
    if (filters.category) params.category = filters.category;
    if (filters.search) params.search = filters.search;
    const { data } = await boutiqueApi.getProducts(params);
    products.value = data.results; Object.assign(pagination, data);
  } finally { loading.value = false; }
}
function changePage(p) { filters.page = p; loadProducts(); window.scrollTo({top:0,behavior:"smooth"}); }
onMounted(async () => {
  const [_, catRes] = await Promise.allSettled([loadProducts(), boutiqueApi.getCategories()]);
  if (catRes.status==="fulfilled") categories.value = catRes.value.data;
});
</script>
<style scoped>
.page-header{background:linear-gradient(135deg,var(--color-primary-dark),var(--color-primary));color:#fff;padding:3.5rem 0 2.5rem}
.page-title{font-size:clamp(1.75rem,3vw,2.5rem);font-weight:800;color:#fff;margin:.5rem 0}
.page-subtitle{color:rgba(255,255,255,.75);max-width:600px}
.formations-layout{display:grid;grid-template-columns:220px 1fr;gap:2.5rem;align-items:start}
.filters-sidebar{position:sticky;top:90px;background:#fff;border:1px solid var(--color-neutral-200);border-radius:var(--radius-lg);padding:1.5rem}
.filters-title{font-size:1rem;font-weight:700;margin-bottom:1.25rem;color:var(--color-primary-dark)}
.filter-options{display:flex;flex-direction:column;gap:.4rem}
.filter-option{display:flex;align-items:center;gap:.5rem;font-size:.875rem;color:var(--color-neutral-700);cursor:pointer;padding:.35rem .5rem;border-radius:var(--radius-sm);transition:background var(--transition-fast)}
.filter-option:hover{background:var(--color-neutral-50)}
.filter-option.active{color:var(--color-primary);font-weight:600}
.filter-option input{accent-color:var(--color-primary)}
.filter-count{margin-left:auto;font-size:.72rem;color:var(--color-neutral-500);background:var(--color-neutral-100);padding:.1rem .45rem;border-radius:999px}
.content-toolbar{margin-bottom:1.5rem}
.search-wrap{position:relative}
.search-icon{position:absolute;left:.8rem;top:50%;transform:translateY(-50%);opacity:.5}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1.5rem}
.pagination{display:flex;align-items:center;justify-content:center;gap:1.5rem;margin-top:2.5rem}
.page-info{font-size:.875rem;color:var(--color-neutral-600)}
@media(max-width:768px){.formations-layout{grid-template-columns:1fr}.filters-sidebar{position:static}}
</style>
