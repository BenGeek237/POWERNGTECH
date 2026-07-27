<template>
  <AppLayout>
    <!-- Loading -->
    <div v-if="loading" class="page-loading">
      <div class="spinner" style="width:3rem;height:3rem;border-width:3px"></div>
    </div>

    <!-- Error -->
    <div v-else-if="!formation" class="error-page">
      <div class="container" style="text-align:center;padding:5rem 0">
        <Frown :size="64" stroke-width="1.5" class="text-neutral-400 mx-auto mb-4" />
        <h1>Formation introuvable</h1>
        <RouterLink to="/formations" class="btn btn-primary" style="margin-top:1rem">
          Voir toutes les formations
        </RouterLink>
      </div>
    </div>

    <template v-else>
      <!-- Header -->
      <div class="formation-header">
        <div class="container formation-header-inner">
          <div class="formation-header-text">
            <div class="header-badges">
              <span class="badge badge-neutral">{{ levelLabel }}</span>
              <span v-if="formation.is_free" class="badge badge-success">Gratuit</span>
              <span class="badge badge-primary">{{ formation.category?.name }}</span>
            </div>
            <h1 class="formation-title">{{ formation.title }}</h1>
            <p class="formation-description">{{ formation.description }}</p>
            <div class="formation-meta-row">
              <span style="display:flex;align-items:center;gap:4px;"><Clock :size="16" /> {{ formation.duration_hours }}h estimées</span>
              <span style="display:flex;align-items:center;gap:4px;"><Folder :size="16" /> Formation téléchargeable</span>
            </div>
          </div>
          <div class="formation-purchase-card card">
            <img v-if="formation.image" :src="formation.image" :alt="formation.title" class="purchase-card-img" />
            <div class="purchase-card-body">
              <div class="purchase-price">
                <template v-if="formation.is_free">
                  <span class="price-main free">Gratuit</span>
                </template>
                <template v-else>
                  <span class="price-main">{{ formatPrice(formation.price) }} FCFA</span>
                </template>
              </div>
              <template v-if="formation.is_enrolled || (formation.is_free && authStore.isAuthenticated)">
                <a v-if="formation.zip_file_url" :href="formation.zip_file_url" class="btn btn-secondary btn-lg" style="width:100%;display:flex;align-items:center;justify-content:center;gap:8px;" download>
                  <Download :size="18" fill="none" /> Télécharger la formation (ZIP)
                </a>
                <p v-else class="purchase-login-hint">Le fichier de formation n'est pas encore disponible.</p>
              </template>
              <template v-else-if="formation.is_free && !authStore.isAuthenticated">
                <RouterLink :to="{ name: 'login', query: { redirect: route.fullPath } }" class="btn btn-primary btn-lg" style="width:100%">
                  Connectez-vous pour télécharger
                </RouterLink>
              </template>
              <template v-else>
                <RouterLink :to="{ name: 'paiement', query: { type: 'formation', id: formation.id, slug: formation.slug } }" class="btn btn-primary btn-lg" style="width:100%" v-if="authStore.isAuthenticated">
                  Acheter cette formation
                </RouterLink>
                <RouterLink :to="{ name: 'login', query: { redirect: route.fullPath } }" class="btn btn-primary btn-lg" style="width:100%" v-else>
                  Connectez-vous pour acheter
                </RouterLink>
              </template>
              <ul class="purchase-features">
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Accès à vie aux fichiers</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Téléchargement immédiat</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Apprentissage hors-ligne</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Support technique inclus</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Tabs -->
      <section class="section">
        <div class="container formation-content-grid">
          <div class="formation-main">
            <!-- Intro Video -->
            <div v-if="formation.has_intro_video" class="content-block">
              <h2 class="content-block-title" style="display:flex;align-items:center;gap:8px;"><Video :size="24" class="text-primary" /> Présentation</h2>
              <div class="intro-video-wrapper">
                <video v-if="formation.intro_video" :src="formation.intro_video" controls class="intro-video-player"></video>
                <iframe v-else-if="formation.intro_video_url" :src="formation.intro_video_url" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen class="intro-video-player"></iframe>
              </div>
            </div>

            <!-- Objectives -->
            <div v-if="formation.objectives" class="content-block">
              <h2 class="content-block-title" style="display:flex;align-items:center;gap:8px;"><Target :size="24" class="text-primary" /> Objectifs</h2>
              <ul class="objectives-list">
                <li v-for="obj in objectivesList" :key="obj">{{ obj }}</li>
              </ul>
            </div>

            <!-- Prerequisites -->
            <div v-if="formation.prerequisites" class="content-block">
              <h2 class="content-block-title" style="display:flex;align-items:center;gap:8px;"><ClipboardList :size="24" class="text-primary" /> Prérequis</h2>
              <ul class="objectives-list">
                <li v-for="req in prerequisitesList" :key="req">{{ req }}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </template>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppLayout from "@/components/common/AppLayout.vue";
import { formationsApi } from "@/services/api";
import { useAuthStore } from "@/stores/auth";
import { Frown, Clock, Video, Folder, Download, CheckCircle2, Target, ClipboardList } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const formation = ref(null);
const loading = ref(true);

const levelLabels = { DEBUTANT: "Débutant", INTERMEDIAIRE: "Intermédiaire", AVANCE: "Avancé" };
const levelLabel = computed(() => levelLabels[formation.value?.level] || "");
const objectivesList = computed(() => formation.value?.objectives?.split("\n").filter(l => l.trim()) || []);
const prerequisitesList = computed(() => formation.value?.prerequisites?.split("\n").filter(l => l.trim()) || []);

function formatPrice(price) { return new Intl.NumberFormat("fr-FR").format(price); }

onMounted(async () => {
  try {
    const { data } = await formationsApi.getDetail(route.params.slug);
    formation.value = data;
  } catch { formation.value = null; }
  finally { loading.value = false; }
});
</script>

<style scoped>
.page-loading { min-height: 60vh; display: flex; align-items: center; justify-content: center; }
.formation-header { background: var(--color-primary-dark); color: #fff; padding: 3rem 0 5rem; }
.formation-header-inner { display: grid; grid-template-columns: 1fr 360px; gap: 3rem; align-items: start; }
.header-badges { display: flex; gap: .5rem; margin-bottom: 1rem; flex-wrap: wrap; }
.formation-title { font-size: clamp(1.5rem, 3vw, 2.2rem); font-weight: 800; color: #fff; margin-bottom: 1rem; }
.formation-description { color: rgba(255,255,255,.8); line-height: 1.7; margin-bottom: 1.25rem; }
.formation-meta-row { display: flex; gap: 1.5rem; flex-wrap: wrap; color: rgba(255,255,255,.8); font-size: .875rem; }
.formation-purchase-card { overflow: hidden; }
.purchase-card-img { width: 100%; height: 200px; object-fit: cover; }
.purchase-card-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.purchase-price { text-align: center; }
.price-main { font-family: var(--font-heading); font-size: 2rem; font-weight: 800; color: var(--color-primary-dark); }
.price-main.free { color: var(--color-secondary-dark); }
.purchase-login-hint { text-align: center; font-size: .8rem; color: var(--color-neutral-600); }
.purchase-features { list-style: none; display: flex; flex-direction: column; gap: .5rem; font-size: .875rem; color: var(--color-neutral-700); padding-top: .5rem; border-top: 1px solid var(--color-neutral-100); }
.content-block { margin-bottom: 2.5rem; padding-bottom: 2.5rem; border-bottom: 1px solid var(--color-neutral-100); }
.content-block-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; color: var(--color-primary-dark); }
.objectives-list { list-style: none; display: flex; flex-direction: column; gap: .6rem; }
.objectives-list li { display: flex; align-items: flex-start; gap: .5rem; font-size: .9rem; line-height: 1.55; }
.objectives-list li::before { content: "✓"; color: var(--color-secondary-dark); font-weight: 700; flex-shrink: 0; }
.intro-video-wrapper { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: var(--radius-lg); background: #000; }
.intro-video-player { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
@media (max-width: 900px) { .formation-header-inner { grid-template-columns: 1fr; } .formation-purchase-card { order: -1; } }
</style>
