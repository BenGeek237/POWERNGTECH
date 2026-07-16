<template>
  <AppLayout>
    <div class="account-page">
      <div class="container account-layout">
        <AccountSidebar />
        <div class="account-content">
          <div class="content-header">
            <div>
              <h1 class="content-title">Mes Formations</h1>
              <p class="content-subtitle">Vos formations achetées et en cours</p>
            </div>
            <RouterLink to="/formations" class="btn btn-primary btn-sm">
              <Plus :size="16" />
              Voir le catalogue
            </RouterLink>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="loading-state">
            <div class="spinner" style="width:2.5rem;height:2.5rem"></div>
            <p>Chargement de vos formations...</p>
          </div>

          <!-- Empty -->
          <div v-else-if="formations.length === 0" class="empty-state card">
            <div class="empty-icon-wrap">
              <GraduationCap :size="48" stroke-width="1" />
            </div>
            <h3>Aucune formation pour l'instant</h3>
            <p>Vous n'êtes encore inscrit à aucune formation. Explorez notre catalogue !</p>
            <RouterLink to="/formations" class="btn btn-primary">
              Découvrir les formations
              <ArrowRight :size="16" />
            </RouterLink>
          </div>

          <!-- Formations grid -->
          <div v-else class="formations-list">
            <RouterLink
              v-for="f in formations"
              :key="f.id"
              :to="`/formations/${f.formation.slug}/apprendre`"
              class="formation-item card"
            >
              <div class="fi-thumb">
                <img v-if="f.formation.image" :src="f.formation.image" :alt="f.formation.title" />
                <div v-else class="fi-thumb-placeholder">
                  <GraduationCap :size="32" stroke-width="1" />
                </div>
              </div>
              <div class="fi-body">
                <p class="fi-category">{{ f.formation.category?.name }}</p>
                <h4 class="fi-title">{{ f.formation.title }}</h4>
                <div class="fi-meta">
                  <span class="badge badge-success">
                    <CheckCircle :size="12" /> Inscrit
                  </span>
                  <span class="fi-enrolled-date" v-if="f.enrolled_at">
                    Depuis {{ formatDate(f.enrolled_at) }}
                  </span>
                </div>
              </div>
              <div class="fi-action">
                <span class="fi-cta">
                  Continuer
                  <ArrowRight :size="15" />
                </span>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import AccountSidebar from "@/components/compte/AccountSidebar.vue";
import { formationsApi } from "@/services/api";
import { GraduationCap, CheckCircle, ArrowRight, Plus } from "lucide-vue-next";

const formations = ref([]);
const loading    = ref(true);

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString("fr-FR", { month: "long", year: "numeric" });
}

onMounted(async () => {
  try {
    const { data } = await formationsApi.getMyFormations();
    formations.value = data;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.account-page { padding: 2.5rem 0; min-height: 70vh; background: var(--color-neutral-50); }
.account-layout { display: grid; grid-template-columns: 260px 1fr; gap: 1.75rem; align-items: start; }

.content-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;
}
.content-title { font-size: 1.4rem; font-weight: 800; color: var(--color-primary-dark); margin: 0; }
.content-subtitle { font-size: .875rem; color: var(--color-neutral-500); margin-top: .2rem; }

.loading-state {
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
  padding: 4rem; color: var(--color-neutral-500);
}
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 1rem; text-align: center; padding: 4rem 2rem;
}
.empty-icon-wrap {
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--color-primary-50); color: var(--color-primary);
  display: flex; align-items: center; justify-content: center;
}
.empty-state h3 { font-size: 1.1rem; font-weight: 700; color: var(--color-primary-dark); }
.empty-state p { font-size: .875rem; color: var(--color-neutral-500); max-width: 300px; }

.formations-list { display: flex; flex-direction: column; gap: 1rem; }
.formation-item {
  display: flex; align-items: center; gap: 1.25rem;
  text-decoration: none; color: inherit; padding: 1rem;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.formation-item:hover { box-shadow: var(--shadow-md); transform: translateX(4px); }

.fi-thumb {
  width: 110px; height: 75px; border-radius: var(--radius-md);
  overflow: hidden; flex-shrink: 0; background: var(--color-primary-50);
  display: flex; align-items: center; justify-content: center; color: var(--color-primary);
}
.fi-thumb img { width: 100%; height: 100%; object-fit: cover; }
.fi-thumb-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }

.fi-body { flex: 1; min-width: 0; }
.fi-category {
  font-size: .68rem; font-weight: 700; color: var(--color-secondary);
  text-transform: uppercase; letter-spacing: .06em; margin-bottom: .25rem;
}
.fi-title {
  font-size: .925rem; font-weight: 700; color: var(--color-primary-dark);
  margin-bottom: .6rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.fi-meta { display: flex; align-items: center; gap: .75rem; flex-wrap: wrap; }
.fi-enrolled-date { font-size: .72rem; color: var(--color-neutral-500); }

.fi-action { flex-shrink: 0; }
.fi-cta {
  display: flex; align-items: center; gap: .35rem;
  font-size: .8rem; font-weight: 600; color: var(--color-primary);
  transition: gap var(--transition-fast);
}
.formation-item:hover .fi-cta { gap: .6rem; }

@media (max-width: 768px) {
  .account-layout { grid-template-columns: 1fr; }
  .fi-thumb { width: 80px; height: 60px; }
}
</style>
