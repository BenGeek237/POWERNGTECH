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
              <span style="display:flex;align-items:center;gap:4px;"><Clock :size="16" /> {{ formation.duration_hours }}h</span>
              <span style="display:flex;align-items:center;gap:4px;"><Video :size="16" /> {{ formation.video_count }} vidéos</span>
              <span style="display:flex;align-items:center;gap:4px;"><Folder :size="16" /> {{ formation.chapter_count }} chapitres</span>
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
              <template v-if="formation.is_enrolled">
                <RouterLink :to="`/formations/${formation.slug}/apprendre`" class="btn btn-secondary btn-lg" style="width:100%;display:flex;align-items:center;justify-content:center;gap:8px;">
                  <Play :size="18" fill="currentColor" /> Continuer la formation
                </RouterLink>
              </template>
              <template v-else-if="formation.is_free">
                <RouterLink :to="`/formations/${formation.slug}/apprendre`" class="btn btn-primary btn-lg" style="width:100%">
                  Commencer gratuitement
                </RouterLink>
              </template>
              <template v-else>
                <button @click="initiatePayment" class="btn btn-primary btn-lg" style="width:100%" :disabled="!authStore.isAuthenticated">
                  Acheter cette formation
                </button>
                <p v-if="!authStore.isAuthenticated" class="purchase-login-hint">
                  <RouterLink to="/auth/connexion">Connectez-vous</RouterLink> pour acheter.
                </p>
              </template>
              <ul class="purchase-features">
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Accès à vie</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> {{ formation.video_count }} vidéos HD</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> {{ formation.pdfs?.length || 0 }} PDF téléchargeables</li>
                <li><CheckCircle2 :size="16" class="text-secondary-dark" /> Certificat de completion</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Tabs -->
      <section class="section">
        <div class="container formation-content-grid">
          <div class="formation-main">
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

            <!-- Programme -->
            <div class="content-block">
              <h2 class="content-block-title" style="display:flex;align-items:center;gap:8px;"><BookOpen :size="24" class="text-primary" /> Programme</h2>
              <div class="chapters-list">
                <div v-for="chapter in formation.chapters" :key="chapter.id" class="chapter-item">
                  <div class="chapter-header">
                    <div class="chapter-info">
                      <Folder :size="18" class="text-neutral-500" />
                      <strong>{{ chapter.title }}</strong>
                    </div>
                    <span class="chapter-count">{{ chapter.video_count }} vidéo{{ chapter.video_count !== 1 ? 's' : '' }}</span>
                  </div>
                  <ul v-if="chapter.videos?.length" class="chapter-videos">
                    <li v-for="video in chapter.videos" :key="video.id" class="chapter-video-item">
                      <Unlock v-if="video.is_preview" :size="16" class="text-secondary-dark" />
                      <Lock v-else :size="16" class="text-neutral-400" />
                      <span>{{ video.title }}</span>
                      <span class="video-duration">{{ video.duration_minutes }}min</span>
                    </li>
                  </ul>
                </div>
              </div>
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
import { Frown, Clock, Video, Folder, Play, CheckCircle2, Target, ClipboardList, BookOpen, Unlock, Lock } from 'lucide-vue-next';

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

async function initiatePayment() {
  if (!authStore.isAuthenticated) { router.push({ name: "login", query: { redirect: route.fullPath } }); return; }
  // Navigate to formation player first for free, or payment flow for paid
  router.push(`/formations/${route.params.slug}/apprendre`);
}

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
.formation-header { background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary)); color: #fff; padding: 3rem 0 5rem; }
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
.chapter-item { border: 1px solid var(--color-neutral-200); border-radius: var(--radius-md); overflow: hidden; margin-bottom: .75rem; }
.chapter-header { display: flex; justify-content: space-between; align-items: center; padding: .9rem 1.1rem; background: var(--color-neutral-50); }
.chapter-info { display: flex; align-items: center; gap: .5rem; font-weight: 600; font-size: .9rem; }
.chapter-count { font-size: .78rem; color: var(--color-neutral-600); }
.chapter-videos { list-style: none; }
.chapter-video-item { display: flex; align-items: center; gap: .5rem; padding: .6rem 1.1rem; font-size: .875rem; color: var(--color-neutral-700); border-top: 1px solid var(--color-neutral-100); }
.video-duration { margin-left: auto; font-size: .75rem; color: var(--color-neutral-500); }
@media (max-width: 900px) { .formation-header-inner { grid-template-columns: 1fr; } .formation-purchase-card { order: -1; } }
</style>
