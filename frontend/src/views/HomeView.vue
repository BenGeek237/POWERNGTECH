<template>
  <AppLayout>
    <!-- HERO -->
    <HeroSection />

    <!-- DERNIÈRES FORMATIONS -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <p class="section-label">Notre catalogue</p>
          <h2 class="section-title">Dernières formations</h2>
          <p class="section-subtitle">
            Des formations pratiques dispensées par des professionnels certifiés
            dans les domaines de l'énergie et de l'électronique.
          </p>
        </div>
        <div v-if="formationsLoading" class="cards-grid">
          <div v-for="i in 6" :key="i" class="card skeleton-card">
            <div class="skeleton" style="height:180px"></div>
            <div style="padding:1rem">
              <div class="skeleton" style="height:14px;margin-bottom:8px"></div>
              <div class="skeleton" style="height:14px;width:60%"></div>
            </div>
          </div>
        </div>
        <div v-else class="cards-grid">
          <CourseCard
            v-for="formation in latestFormations"
            :key="formation.id"
            :formation="formation"
          />
        </div>
        <div class="section-cta">
          <RouterLink to="/formations" class="btn btn-primary btn-lg">
            Voir toutes les formations
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- PRODUITS RÉCENTS -->
    <section class="section section--alt">
      <div class="container">
        <div class="section-header">
          <p class="section-label">Notre boutique</p>
          <h2 class="section-title">Produits récents</h2>
          <p class="section-subtitle">
            Équipements électroniques et solutions énergétiques de qualité professionnelle.
          </p>
        </div>
        <div v-if="productsLoading" class="cards-grid">
          <div v-for="i in 6" :key="i" class="card skeleton-card">
            <div class="skeleton" style="height:200px"></div>
            <div style="padding:1rem">
              <div class="skeleton" style="height:14px;margin-bottom:8px"></div>
              <div class="skeleton" style="height:14px;width:40%"></div>
            </div>
          </div>
        </div>
        <div v-else class="cards-grid">
          <ProductCard
            v-for="product in latestProducts"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="section-cta">
          <RouterLink to="/boutique" class="btn btn-outline btn-lg">
            Voir la boutique complète
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- SERVICES -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <p class="section-label">Ce que nous faisons</p>
          <h2 class="section-title">Nos services</h2>
          <p class="section-subtitle">
            POWER NG TECHNOLOGIE intervient dans plusieurs domaines d'expertise
            pour accompagner votre développement.
          </p>
        </div>
        <div v-if="servicesLoading" class="services-grid">
          <div v-for="i in 6" :key="i" class="card skeleton-card" style="padding:1.5rem">
            <div class="skeleton" style="height:48px;width:48px;border-radius:12px;margin-bottom:1rem"></div>
            <div class="skeleton" style="height:16px;margin-bottom:8px"></div>
            <div class="skeleton" style="height:14px"></div>
          </div>
        </div>
        <div v-else class="services-grid">
          <ServiceCard
            v-for="service in services"
            :key="service.id"
            :service="service"
          />
        </div>
        <div class="section-cta">
          <RouterLink to="/services" class="btn btn-outline btn-lg">Tous nos services</RouterLink>
        </div>
      </div>
    </section>

    <!-- FORMATION PERSONNALISÉE CTA -->
    <section class="section custom-training-section">
      <div class="container">
        <div class="custom-training-inner">
          <div class="custom-training-content">
            <span class="section-label" style="color:rgba(255,255,255,0.7)">Formation sur mesure</span>
            <h2 class="custom-training-title">Besoin d'une formation personnalisée ?</h2>
            <p class="custom-training-desc">
              Nous élaborons des programmes de formation adaptés à vos besoins spécifiques,
              votre niveau et votre secteur d'activité. Groupes ou individuels.
            </p>
            <RouterLink to="/formation-personnalisee" class="btn btn-lg" style="background:#fff;color:var(--color-primary);border-color:#fff">
              Faire une demande gratuitement
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </RouterLink>
          </div>
          <div class="custom-training-visual">
            <div class="training-icon-grid">
              <div class="training-icon" v-for="item in trainingIcons" :key="item.label">
                <component :is="item.icon" :size="28" stroke-width="1.5" />
                <small>{{ item.label }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- POURQUOI NOUS CHOISIR -->
    <WhyChooseUs />

    <!-- TÉMOIGNAGES -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="section-title" style="margin-bottom: 2rem">Ce que disent nos apprenants</h2>
        <div class="testimonials-grid">
          <div v-for="t in testimonials" :key="t.name" class="testimonial-card">
            <blockquote class="testi-quote">« {{ t.quote }} »</blockquote>
            <div class="testi-author">
              <strong>{{ t.name }}</strong>
              <span>{{ t.role }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTACT RAPIDE -->
    <section class="section section--alt">
      <div class="container">
        <div class="contact-banner">
          <div>
            <h2 class="section-title" style="margin:0">Prêt à commencer ?</h2>
            <p class="section-subtitle" style="margin-top:0.5rem">
              Contactez-nous dès aujourd'hui pour en savoir plus sur nos services et formations.
            </p>
          </div>
          <div class="contact-banner-actions">
            <RouterLink to="/contact" class="btn btn-primary btn-lg">Nous contacter</RouterLink>
                        <a href="tel:+237691242788" class="btn btn-outline btn-lg">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 10.8a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>
              Appeler directement
            </a>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import HeroSection from "@/components/home/HeroSection.vue";
import CourseCard from "@/components/formations/CourseCard.vue";
import ProductCard from "@/components/boutique/ProductCard.vue";
import ServiceCard from "@/components/home/ServiceCard.vue";
import WhyChooseUs from "@/components/home/WhyChooseUs.vue";
import { formationsApi, boutiqueApi, servicesApi } from "@/services/api";
import { Sun, Zap, Wrench, Snowflake, Radio, Factory } from "lucide-vue-next";

const latestFormations = ref([]);
const latestProducts = ref([]);
const services = ref([]);
const formationsLoading = ref(true);
const productsLoading = ref(true);
const servicesLoading = ref(true);

const trainingIcons = [
  { icon: Sun, label: "Solaire" },
  { icon: Zap, label: "Électrotechnique" },
  { icon: Wrench, label: "Maintenance" },
  { icon: Snowflake, label: "Climatisation" },
  { icon: Radio, label: "Électronique" },
  { icon: Factory, label: "Industriel" },
];

const testimonials = [
  {
    name: "Moussa Hamidou",
    role: "Technicien solaire, Ngaoundéré",
    initials: "MH",
    quote: "Grâce à POWER NG TECHNOLOGIE, j'ai pu créer ma propre entreprise d'installation solaire. La formation était très pratique et bien structurée.",
  },
  {
    name: "Aïssatou Bello",
    role: "Étudiante en électrotechnique",
    initials: "AB",
    quote: "Les formateurs sont vraiment compétents et disponibles. J'ai appris en quelques semaines ce que je n'aurais pas appris en plusieurs mois ailleurs.",
  },
  {
    name: "Jean-Pierre Nkolo",
    role: "Chef d'atelier de maintenance",
    initials: "JN",
    quote: "Le matériel est professionnel et les conditions de formation sont excellentes. Je recommande vivement à tous ceux qui veulent progresser dans ces métiers.",
  },
];

onMounted(async () => {
  // Load all data in parallel
  const [formationsRes, productsRes, servicesRes] = await Promise.allSettled([
    formationsApi.getLatest(),
    boutiqueApi.getLatestProducts(),
    servicesApi.getServices(),
  ]);

  if (formationsRes.status === "fulfilled") {
    latestFormations.value = formationsRes.value.data;
  }
  formationsLoading.value = false;

  if (productsRes.status === "fulfilled") {
    latestProducts.value = productsRes.value.data;
  }
  productsLoading.value = false;

  if (servicesRes.status === "fulfilled") {
    services.value = servicesRes.value.data;
  }
  servicesLoading.value = false;
});
</script>

<style scoped>
/* Section header */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}
.section-header .section-subtitle { margin-inline: auto; }

/* Cards grids */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.skeleton-card { min-height: 260px; }

/* Services grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

/* Section CTA */
.section-cta {
  text-align: center;
  margin-top: 2.5rem;
}

/* Custom Training */
.custom-training-section {
  background: var(--color-primary-dark);
  color: #fff;
}
.custom-training-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 3rem;
}
.custom-training-content { max-width: 540px; }
.custom-training-title {
  font-size: clamp(1.5rem, 2.5vw, 2.2rem);
  font-weight: 700;
  color: #fff;
  margin: 0.5rem 0 1rem;
}
.custom-training-desc {
  color: rgba(255,255,255,0.8);
  margin-bottom: 1.75rem;
  line-height: 1.7;
}

/* Training icon grid */
.training-icon-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.training-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 1rem 0.75rem;
  border: 1px solid rgba(255,255,255,0.1);
}
.training-icon span { font-size: 1.75rem; }
.training-icon small { font-size: 0.7rem; color: rgba(255,255,255,0.75); font-weight: 500; }

/* Contact banner */
.contact-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
}
.contact-banner-actions {
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
  flex-wrap: wrap;
}

/* Testimonials */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.testimonial-card {
  padding: 1.5rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  background: #fff;
}
.testi-quote {
  font-size: 0.9rem;
  color: var(--color-neutral-700);
  line-height: 1.75;
  font-style: italic;
  margin: 0 0 1rem;
}
.testi-author strong {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-neutral-900);
}
.testi-author span {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
}

@media (max-width: 768px) {
  .custom-training-inner { flex-direction: column; }
  .training-icon-grid { grid-template-columns: repeat(3, 1fr); }
  .contact-banner { flex-direction: column; text-align: center; }
  .contact-banner-actions { justify-content: center; }
}
</style>
