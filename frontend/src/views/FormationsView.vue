<template>
  <AppLayout>
    <!-- Page Banner -->
    <div class="page-banner">
      <div class="container">
        <p class="page-banner-label">Notre catalogue</p>
        <h1 class="page-banner-title">Toutes les formations</h1>
        <p class="page-banner-desc">
          Développez vos compétences avec nos formations pratiques en énergie, électronique et électrotechnique.
        </p>
      </div>
    </div>

    <section class="section">
      <div class="container formations-layout">
        <!-- Filters sidebar -->
        <aside class="filters-sidebar">
          <h3 class="filters-title">Filtres</h3>

          <!-- Categories -->
          <div class="filter-group">
            <h4 class="filter-group-title">Catégorie</h4>
            <div class="filter-options">
              <label class="filter-option" :class="{ active: !filters.category }">
                <input type="radio" v-model="filters.category" :value="null" @change="applyFilters" />
                Toutes les catégories
              </label>
              <label
                v-for="cat in categories"
                :key="cat.id"
                class="filter-option"
                :class="{ active: filters.category === cat.slug }"
              >
                <input type="radio" v-model="filters.category" :value="cat.slug" @change="applyFilters" />
                {{ cat.name }}
                <span class="filter-count">{{ cat.formation_count }}</span>
              </label>
            </div>
          </div>

          <!-- Level -->
          <div class="filter-group">
            <h4 class="filter-group-title">Niveau</h4>
            <div class="filter-options">
              <label class="filter-option" :class="{ active: !filters.level }">
                <input type="radio" v-model="filters.level" :value="null" @change="applyFilters" />
                Tous les niveaux
              </label>
              <label v-for="level in levels" :key="level.value" class="filter-option">
                <input type="radio" v-model="filters.level" :value="level.value" @change="applyFilters" />
                {{ level.label }}
              </label>
            </div>
          </div>

          <!-- Type -->
          <div class="filter-group">
            <h4 class="filter-group-title">Type</h4>
            <div class="filter-options">
              <label class="filter-option"><input type="radio" v-model="filters.is_free" :value="null" @change="applyFilters" />Toutes</label>
              <label class="filter-option"><input type="radio" v-model="filters.is_free" :value="true" @change="applyFilters" />Gratuites</label>
              <label class="filter-option"><input type="radio" v-model="filters.is_free" :value="false" @change="applyFilters" />Payantes</label>
            </div>
          </div>

          <button class="btn btn-outline" style="width:100%" @click="resetFilters">
            Réinitialiser
          </button>
        </aside>

        <!-- Main content -->
        <div class="formations-main">
          <!-- Search + Sort bar -->
          <div class="content-toolbar">
            <div class="search-wrap">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
              <input
                v-model="filters.search"
                @input="debouncedSearch"
                type="text"
                class="form-input"
                placeholder="Rechercher une formation..."
                style="padding-left:2.5rem"
              />
            </div>
            <div class="sort-wrap">
              <select v-model="filters.ordering" @change="applyFilters" class="form-select">
                <option value="-created_at">Plus récentes</option>
                <option value="price">Prix croissant</option>
                <option value="-price">Prix décroissant</option>
                <option value="title">Alphabétique</option>
              </select>
            </div>
          </div>

          <!-- Results count -->
          <p v-if="!loading" class="results-count">
            {{ pagination.count }} formation{{ pagination.count !== 1 ? 's' : '' }} trouvée{{ pagination.count !== 1 ? 's' : '' }}
          </p>

          <!-- Grid -->
          <div v-if="loading" class="cards-grid">
            <div v-for="i in 6" :key="i" class="card skeleton-card">
              <div class="skeleton" style="height:180px"></div>
              <div style="padding:1rem"><div class="skeleton" style="height:14px;margin-bottom:8px"></div><div class="skeleton" style="height:14px;width:60%"></div></div>
            </div>
          </div>

                    <div v-else-if="formations.length === 0" class="empty-state">
            <Search :size="48" stroke-width="1" class="empty-icon-svg" />
            <h3>Aucune formation trouvée</h3>
            <p>Essayez de modifier vos filtres ou votre recherche.</p>
            <button class="btn btn-outline" @click="resetFilters">Effacer les filtres</button>
          </div>

          <div v-else class="cards-grid">
            <CourseCard v-for="f in formations" :key="f.id" :formation="f" />
          </div>

          <!-- Pagination -->
          <div v-if="pagination.total_pages > 1" class="pagination">
            <button
              class="btn btn-outline btn-sm"
              :disabled="!pagination.previous"
              @click="changePage(pagination.current_page - 1)"
            >← Précédent</button>
            <span class="page-info">Page {{ pagination.current_page }} / {{ pagination.total_pages }}</span>
            <button
              class="btn btn-outline btn-sm"
              :disabled="!pagination.next"
              @click="changePage(pagination.current_page + 1)"
            >Suivant →</button>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import CourseCard from "@/components/formations/CourseCard.vue";
import { formationsApi } from "@/services/api";
import { Search } from "lucide-vue-next";

const formations = ref([]);
const categories = ref([]);
const loading = ref(true);
const pagination = reactive({ count: 0, total_pages: 1, current_page: 1, next: null, previous: null });

const filters = reactive({ category: null, level: null, is_free: null, search: "", ordering: "-created_at", page: 1 });
const levels = [
  { value: "DEBUTANT", label: "Débutant" },
  { value: "INTERMEDIAIRE", label: "Intermédiaire" },
  { value: "AVANCE", label: "Avancé" },
];

let searchTimer = null;
function debouncedSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { filters.page = 1; loadFormations(); }, 400);
}

async function loadFormations() {
  loading.value = true;
  try {
    const params = { ordering: filters.ordering, page: filters.page };
    if (filters.category) params.category = filters.category;
    if (filters.level)    params.level = filters.level;
    if (filters.is_free !== null) params.is_free = filters.is_free;
    if (filters.search)   params.search = filters.search;

    const { data } = await formationsApi.getList(params);
    formations.value = data.results;
    Object.assign(pagination, data);
  } finally {
    loading.value = false;
  }
}

function applyFilters() { filters.page = 1; loadFormations(); }
function resetFilters() { Object.assign(filters, { category: null, level: null, is_free: null, search: "", ordering: "-created_at", page: 1 }); loadFormations(); }
function changePage(page) { filters.page = page; loadFormations(); window.scrollTo({ top: 0, behavior: "smooth" }); }

onMounted(async () => {
  const [_, catRes] = await Promise.allSettled([loadFormations(), formationsApi.getCategories()]);
  if (catRes.status === "fulfilled") categories.value = catRes.value.data;
});
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
  color: #fff; padding: 3.5rem 0 2.5rem;
}
.page-title { font-size: clamp(1.75rem, 3vw, 2.5rem); font-weight: 800; color: #fff; margin: 0.5rem 0; }
.page-subtitle { color: rgba(255,255,255,.75); max-width: 600px; }

.formations-layout { display: grid; grid-template-columns: 260px 1fr; gap: 2.5rem; align-items: start; }

/* Sidebar */
.filters-sidebar { position: sticky; top: 90px; background: #fff; border: 1px solid var(--color-neutral-200); border-radius: var(--radius-lg); padding: 1.5rem; }
.filters-title { font-size: 1rem; font-weight: 700; margin-bottom: 1.25rem; color: var(--color-primary-dark); }
.filter-group { margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--color-neutral-100); }
.filter-group:last-of-type { border-bottom: none; padding-bottom: 0; }
.filter-group-title { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: var(--color-neutral-600); margin-bottom: .75rem; }
.filter-options { display: flex; flex-direction: column; gap: .4rem; }
.filter-option { display: flex; align-items: center; gap: .5rem; font-size: .875rem; color: var(--color-neutral-700); cursor: pointer; padding: .35rem .5rem; border-radius: var(--radius-sm); transition: background var(--transition-fast); }
.filter-option:hover { background: var(--color-neutral-50); }
.filter-option.active { color: var(--color-primary); font-weight: 600; }
.filter-option input { accent-color: var(--color-primary); }
.filter-count { margin-left: auto; font-size: .72rem; color: var(--color-neutral-500); background: var(--color-neutral-100); padding: .1rem .45rem; border-radius: 999px; }

/* Toolbar */
.content-toolbar { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.search-wrap { flex: 1; position: relative; }
.search-icon { position: absolute; left: .8rem; top: 50%; transform: translateY(-50%); opacity: .5; }
.sort-wrap { flex-shrink: 0; }
.results-count { font-size: .875rem; color: var(--color-neutral-600); margin-bottom: 1.25rem; }

/* Grid */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.5rem; }
.skeleton-card { min-height: 260px; }
.empty-state { text-align: center; padding: 4rem 2rem; color: var(--color-neutral-500); }
.empty-icon-svg { margin: 0 auto 1rem; opacity: 0.4; }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-top: 2.5rem; }
.page-info { font-size: .875rem; color: var(--color-neutral-600); }

@media (max-width: 900px) {
  .formations-layout { grid-template-columns: 1fr; }
  .filters-sidebar { position: static; }
}
</style>
