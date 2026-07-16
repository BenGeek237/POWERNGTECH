<template>
  <AppLayout>
    <!-- ── Hero ─────────────────────────────────────────── -->
    <div class="services-hero">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
      </div>
      <div class="container services-hero-content fade-in">
        <span class="hero-badge">
          <Wrench :size="14" />
          Solutions professionnelles
        </span>
        <h1 class="services-hero-title">
          Des services experts pour
          <span class="accent">votre réussite technologique</span>
        </h1>
        <p class="services-hero-sub">
          POWER NG TECHNOLOGIE intervient dans plusieurs domaines d'expertise pour
          accompagner particuliers, entreprises et institutions dans leur développement.
        </p>
        <div class="hero-actions">
          <RouterLink to="/contact" class="btn btn-lg hero-btn-primary">
            Demander un devis
            <ArrowRight :size="18" />
          </RouterLink>
          <RouterLink to="/formation-personnalisee" class="btn btn-lg btn-outline-white">
            Formation personnalisée
          </RouterLink>
        </div>
      </div>
      <div class="hero-wave">
        <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
          <path d="M0,64L80,58.7C160,53,320,43,480,48C640,53,800,75,960,74.7C1120,75,1280,53,1360,42.7L1440,32L1440,80L1360,80C1280,80,1120,80,960,80C800,80,640,80,480,80C320,80,160,80,80,80L0,80Z" fill="white"/>
        </svg>
      </div>
    </div>

    <!-- ── Services Grid ─────────────────────────────────── -->
    <section class="section">
      <div class="container">
        <div class="section-header" style="text-align:center;margin-bottom:3rem">
          <p class="section-label">Ce que nous proposons</p>
          <h2 class="section-title">Nos domaines d'expertise</h2>
          <p class="section-subtitle" style="margin-inline:auto">
            Des prestations professionnelles adaptées à vos besoins spécifiques, avec un accompagnement de qualité.
          </p>
        </div>

        <!-- Loading skeleton -->
        <div v-if="loading" class="services-main-grid">
          <div v-for="i in 6" :key="i" class="skeleton-service">
            <div class="skeleton" style="height:72px;width:72px;border-radius:16px;margin-bottom:1.25rem"></div>
            <div class="skeleton" style="height:18px;width:60%;margin-bottom:.75rem"></div>
            <div class="skeleton" style="height:12px;margin-bottom:.4rem"></div>
            <div class="skeleton" style="height:12px;width:80%"></div>
          </div>
        </div>

        <div v-else-if="services.length === 0" class="empty-state">
          <Settings :size="48" stroke-width="1" class="empty-icon-svg" />
          <h3>Aucun service disponible</h3>
          <p>Revenez bientôt pour découvrir nos services.</p>
        </div>

        <div v-else class="services-main-grid">
          <div
            v-for="(service, idx) in services"
            :key="service.id"
            class="service-main-card"
            :class="{ 'service-main-card--featured': idx === 0 }"
          >
            <div class="service-main-icon">
              <component :is="getIconComponent(service.icon)" :size="36" stroke-width="1.25" />
            </div>
            <h3 class="service-main-title">{{ service.title }}</h3>
            <p class="service-main-desc">{{ service.description }}</p>
            <RouterLink to="/contact" class="service-main-cta">
              Demander ce service
              <ArrowRight :size="16" />
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Process Section ──────────────────────────────── -->
    <section class="section section--alt">
      <div class="container">
        <div class="section-header" style="text-align:center;margin-bottom:3rem">
          <p class="section-label">Notre approche</p>
          <h2 class="section-title">Comment nous travaillons</h2>
          <p class="section-subtitle" style="margin-inline:auto">
            Un processus simple et transparent pour vous garantir les meilleurs résultats.
          </p>
        </div>
        <div class="process-grid">
          <div v-for="step in process" :key="step.step" class="process-step">
            <div class="process-number">{{ step.step }}</div>
            <div class="process-icon">
              <component :is="step.icon" :size="28" stroke-width="1.5" />
            </div>
            <h4>{{ step.title }}</h4>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Guarantees ──────────────────────────────────── -->
    <section class="section">
      <div class="container">
        <div class="guarantees-grid">
          <div class="guarantees-text">
            <p class="section-label">Nos engagements</p>
            <h2 class="section-title">Pourquoi faire confiance à POWER NG TECHNOLOGIE ?</h2>
            <p style="color:var(--color-neutral-600);line-height:1.75;margin-top:.75rem">
              Notre réputation repose sur la qualité de nos prestations et la satisfaction
              de nos clients. Chaque intervention est réalisée par des techniciens certifiés.
            </p>
            <div class="guarantees-list">
              <div v-for="g in guarantees" :key="g" class="guarantee-item">
                <CheckCircle :size="20" stroke-width="2" class="g-check" />
                <span>{{ g }}</span>
              </div>
            </div>
            <RouterLink to="/contact" class="btn btn-primary" style="margin-top:2rem">
              Prendre contact maintenant
              <ArrowRight :size="16" />
            </RouterLink>
          </div>
          <div class="guarantees-visual">
            <div class="guarantee-stat-grid">
              <div v-for="stat in qualityStats" :key="stat.label" class="guarantee-stat-card">
                <component :is="stat.icon" :size="32" stroke-width="1.25" class="gs-icon" />
                <span class="gs-val">{{ stat.value }}</span>
                <span class="gs-lbl">{{ stat.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────────── -->
    <section class="section services-cta-section">
      <div class="container">
        <div class="services-cta">
          <div class="services-cta-text">
            <h2>Besoin d'une intervention rapide ?</h2>
            <p>Notre équipe est disponible du lundi au samedi, de 8h à 18h.</p>
            <div class="cta-contacts">
              <a href="tel:+237691242788" class="cta-contact-item">
                <Phone :size="18" />
                +237 691 242 788
              </a>
              <a href="https://wa.me/237691242788" target="_blank" rel="noopener" class="cta-contact-item cta-whatsapp">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.464 3.488"/></svg>
                WhatsApp
              </a>
            </div>
          </div>
          <RouterLink to="/contact" class="cta-big-btn">
            <Mail :size="24" />
            <span>Envoyer un message</span>
          </RouterLink>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import { servicesApi } from "@/services/api";
import {
  Sun, Zap, Wrench, Hammer, Snowflake, Settings,
  Monitor, Battery, BarChart, ArrowRight, CheckCircle,
  Phone, Mail, MessageSquare, ClipboardList, Handshake, Star, Trophy, Clock
} from 'lucide-vue-next';

const services = ref([]);
const loading = ref(true);

const iconMap = {
  "Sun": Sun, "solar-panel": Sun,
  "bolt": Zap, "zap": Zap, "Zap": Zap,
  "wrench": Wrench, "Wrench": Wrench,
  "tool": Hammer,
  "ac": Snowflake, "Snowflake": Snowflake,
  "gear": Settings,
  "cpu": Monitor,
  "battery": Battery,
  "ChartBar": BarChart
};
function getIconComponent(icon) { return iconMap[icon] || Settings; }

const process = [
  { step: "01", icon: MessageSquare, title: "Contact & Analyse", desc: "Vous nous contactez et nous analysons ensemble vos besoins spécifiques." },
  { step: "02", icon: ClipboardList, title: "Proposition", desc: "Nous élaborons une proposition technique et financière adaptée à votre situation." },
  { step: "03", icon: Wrench, title: "Intervention", desc: "Notre équipe de techniciens certifiés réalise la prestation dans les délais convenus." },
  { step: "04", icon: Handshake, title: "Suivi", desc: "Nous assurons un suivi post-intervention pour garantir votre satisfaction." },
];

const guarantees = [
  "Techniciens certifiés et expérimentés",
  "Équipements professionnels de qualité",
  "Interventions rapides et dans les délais",
  "Devis gratuit et sans engagement",
  "Service après-vente et maintenance",
  "Support technique disponible 6j/7",
];

const qualityStats = [
  { icon: Star,    value: "4.9/5", label: "Note de satisfaction" },
  { icon: Trophy,  value: "5",     label: "Ans d'expérience" },
  { icon: Clock,   value: "< 48h", label: "Délai de réponse" },
  { icon: CheckCircle, value: "100%", label: "Clients satisfaits" },
];

onMounted(async () => {
  try {
    const { data } = await servicesApi.getServices();
    services.value = data;
  } catch {
    services.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* ── Hero ─────────────────────────────────────────────── */
.services-hero {
  position: relative;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 50%, #1a4a7a 100%);
  color: #fff; padding: 5rem 0 7rem; overflow: hidden;
}
.hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-gradient {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(46,125,50,.15) 0%, transparent 60%);
}
.hero-pattern {
  position: absolute; inset: 0;
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,.04) 1px, transparent 0);
  background-size: 32px 32px;
}
.services-hero-content { position: relative; z-index: 1; max-width: 700px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: .5rem;
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
  border-radius: 999px; padding: .35rem 1rem; font-size: .8rem; font-weight: 500;
  color: rgba(255,255,255,.9); margin-bottom: 1.5rem; backdrop-filter: blur(8px);
}
.services-hero-title {
  font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; line-height: 1.2;
  color: #fff; margin-bottom: 1rem;
}
.services-hero-title .accent { color: var(--color-secondary-500); }
.services-hero-sub {
  font-size: 1.05rem; color: rgba(255,255,255,.8); line-height: 1.7; margin-bottom: 2rem;
}
.hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.hero-btn-primary {
  background: var(--color-secondary); color: #fff; border-color: var(--color-secondary);
}
.hero-btn-primary:hover {
  background: var(--color-secondary-dark); border-color: var(--color-secondary-dark); color: #fff;
}
.hero-wave { position: absolute; bottom: 0; left: 0; right: 0; height: 80px; z-index: 2; }
.hero-wave svg { width: 100%; height: 100%; display: block; }

/* ── Services Grid ─────────────────────────────────────── */
.services-main-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}
.service-main-card {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 2rem;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
  display: flex; flex-direction: column;
}
.service-main-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-5px); }
.service-main-card--featured {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-color: transparent; color: #fff;
}
.service-main-card--featured .service-main-title,
.service-main-card--featured .service-main-desc { color: rgba(255,255,255,.9); }
.service-main-card--featured .service-main-icon {
  background: rgba(255,255,255,.15); color: #fff;
}
.service-main-card--featured .service-main-cta { color: rgba(255,255,255,.85); }
.service-main-card--featured .service-main-cta:hover { color: #fff; }

.service-main-icon {
  width: 72px; height: 72px; border-radius: 18px;
  background: var(--color-primary-50); color: var(--color-primary);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.25rem; flex-shrink: 0;
}
.service-main-title { font-size: 1.05rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .6rem; }
.service-main-desc { font-size: .875rem; color: var(--color-neutral-600); line-height: 1.7; flex: 1; }
.service-main-cta {
  display: inline-flex; align-items: center; gap: .4rem;
  font-size: .8rem; font-weight: 600; color: var(--color-primary);
  text-decoration: none; margin-top: 1.25rem;
  transition: gap var(--transition-fast), color var(--transition-fast);
}
.service-main-cta:hover { gap: .7rem; color: var(--color-primary-dark); }

/* Skeleton */
.skeleton-service {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 2rem;
}
.empty-state {
  text-align: center; padding: 4rem 2rem; color: var(--color-neutral-500);
}
.empty-icon-svg { margin: 0 auto 1rem; opacity: .4; }

/* ── Process ──────────────────────────────────────────── */
.process-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; position: relative; }
.process-grid::before {
  content: ''; position: absolute;
  top: 28px; left: calc(12.5% + 20px); right: calc(12.5% + 20px);
  height: 2px; background: var(--color-primary-100); z-index: 0;
}
.process-step { text-align: center; position: relative; z-index: 1; }
.process-number {
  font-family: var(--font-heading); font-size: .7rem; font-weight: 700;
  color: var(--color-primary); background: var(--color-primary-50);
  width: 28px; height: 28px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto .75rem; border: 2px solid var(--color-primary-100);
}
.process-icon {
  width: 56px; height: 56px; border-radius: var(--radius-lg);
  background: #fff; border: 1.5px solid var(--color-neutral-200);
  color: var(--color-primary); display: flex; align-items: center;
  justify-content: center; margin: 0 auto 1rem;
  box-shadow: var(--shadow-sm);
}
.process-step h4 { font-size: .9rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .4rem; }
.process-step p { font-size: .8rem; color: var(--color-neutral-600); line-height: 1.6; }

/* ── Guarantees ────────────────────────────────────────── */
.guarantees-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center; }
.guarantees-list { display: flex; flex-direction: column; gap: .85rem; margin-top: 1.75rem; }
.guarantee-item { display: flex; align-items: center; gap: .75rem; font-size: .875rem; color: var(--color-neutral-700); }
.g-check { color: var(--color-secondary); flex-shrink: 0; }

.guarantee-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.guarantee-stat-card {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 2rem 1.5rem; text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: .4rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.guarantee-stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.gs-icon { color: var(--color-primary); margin-bottom: .3rem; }
.gs-val { font-family: var(--font-heading); font-size: 1.6rem; font-weight: 800; color: var(--color-primary); line-height: 1; }
.gs-lbl { font-size: .72rem; color: var(--color-neutral-600); font-weight: 500; }

/* ── CTA ──────────────────────────────────────────────── */
.services-cta-section {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 60%, var(--color-primary-500) 100%);
}
.services-cta { display: flex; align-items: center; justify-content: space-between; gap: 3rem; flex-wrap: wrap; }
.services-cta-text h2 { font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 800; color: #fff; margin-bottom: .5rem; }
.services-cta-text p { color: rgba(255,255,255,.75); font-size: .95rem; }
.cta-contacts { display: flex; gap: 1.25rem; flex-wrap: wrap; margin-top: 1.25rem; }
.cta-contact-item {
  display: flex; align-items: center; gap: .5rem;
  color: rgba(255,255,255,.85); font-size: .9rem; text-decoration: none;
  transition: color var(--transition-fast);
}
.cta-contact-item:hover { color: #fff; }
.cta-whatsapp { color: #25D366; font-weight: 600; }
.cta-whatsapp:hover { color: #1ebe5d; }
.cta-big-btn {
  display: flex; flex-direction: column; align-items: center; gap: .6rem;
  background: rgba(255,255,255,.12); border: 1.5px solid rgba(255,255,255,.3);
  border-radius: var(--radius-xl); padding: 2rem 2.5rem;
  color: #fff; text-decoration: none; text-align: center;
  backdrop-filter: blur(8px); font-weight: 700; font-size: .9rem;
  transition: background var(--transition-normal), transform var(--transition-normal);
  flex-shrink: 0;
}
.cta-big-btn:hover { background: rgba(255,255,255,.22); color: #fff; transform: translateY(-3px); }

/* Responsive */
@media (max-width: 1024px) {
  .services-main-grid { grid-template-columns: repeat(2, 1fr); }
  .process-grid { grid-template-columns: repeat(2, 1fr); }
  .process-grid::before { display: none; }
}
@media (max-width: 768px) {
  .guarantees-grid { grid-template-columns: 1fr; gap: 2.5rem; }
}
@media (max-width: 640px) {
  .services-main-grid { grid-template-columns: 1fr; }
  .services-cta { flex-direction: column; text-align: center; }
  .cta-contacts { justify-content: center; }
  .hero-actions { flex-direction: column; }
}
</style>
