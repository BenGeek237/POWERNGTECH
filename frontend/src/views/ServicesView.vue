<template>
  <AppLayout>
    <!-- Header -->
    <div class="page-header">
      <div class="container">
        <p class="page-label">Services</p>
        <h1 class="page-title">Ce que nous proposons</h1>
        <p class="page-desc">
          Des prestations professionnelles en énergie, électronique et maintenance,
          avec un accompagnement de A à Z.
        </p>
      </div>
    </div>

    <!-- Services grid -->
    <section class="section">
      <div class="container">
        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Chargement des services...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="services.length === 0" class="empty-state">
          <h3>Aucun service disponible</h3>
          <p>Revenez bientôt pour découvrir nos services.</p>
        </div>

        <!-- Services -->
        <div v-else class="services-grid">
          <div v-for="service in services" :key="service.id" class="service-card">
            <h3>{{ service.title }}</h3>
            <p>{{ service.description }}</p>
            <RouterLink to="/contact" class="service-link">
              Demander ce service →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Process -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="h2" style="margin-bottom: 2rem">Comment ça se passe</h2>
        <div class="process-list">
          <div v-for="step in process" :key="step.num" class="process-step">
            <span class="process-num">{{ step.num }}</span>
            <div>
              <h4>{{ step.title }}</h4>
              <p>{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Guarantees -->
    <section class="section">
      <div class="container">
        <div class="guarantees-layout">
          <div>
            <h2 class="h2">Nos engagements</h2>
            <p class="text" style="margin-top: 0.5rem">
              Chaque intervention est réalisée par des techniciens expérimentés.
            </p>
            <ul class="guarantees-list">
              <li v-for="g in guarantees" :key="g">✓ {{ g }}</li>
            </ul>
            <RouterLink to="/contact" class="btn btn-primary" style="margin-top: 1.5rem">
              Demander un devis gratuit
            </RouterLink>
          </div>
          <div class="contact-aside">
            <h4>Contact direct</h4>
            <a href="tel:+237691242788">+237 691 242 788</a>
            <a href="mailto:christinoo120@gmail.com">christinoo120@gmail.com</a>
            <p class="hours">Lun – Sam, 8h – 18h</p>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import { servicesApi } from "@/services/api";

const services = ref([]);
const loading  = ref(true);

const process = [
  { num: "1", title: "Contactez-nous", desc: "Expliquez votre besoin par téléphone, WhatsApp ou via le formulaire." },
  { num: "2", title: "Devis gratuit", desc: "On vous envoie une proposition claire avec un délai et un prix." },
  { num: "3", title: "Intervention", desc: "Notre équipe intervient sur site ou en atelier selon le besoin." },
  { num: "4", title: "Suivi", desc: "On assure le suivi technique après l'intervention." },
];

const guarantees = [
  "Techniciens expérimentés",
  "Équipements professionnels",
  "Devis gratuit et sans engagement",
  "Interventions dans les délais",
  "Service après-vente inclus",
  "Support technique 6j/7",
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
.page-header {
  background: var(--color-primary-dark);
  color: #fff;
  padding: 4rem 0 3rem;
}
.page-label {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.5);
  margin-bottom: 0.5rem;
}
.page-title {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.75rem;
}
.page-desc {
  color: rgba(255,255,255,0.65);
  max-width: 480px;
  line-height: 1.7;
}
.h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--color-neutral-900);
}
.text {
  font-size: 0.9rem;
  color: var(--color-neutral-600);
  line-height: 1.75;
}

.loading-state {
  text-align: center;
  padding: 4rem;
  color: var(--color-neutral-500);
}
.empty-state {
  text-align: center;
  padding: 4rem;
  color: var(--color-neutral-500);
}

/* Services grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.service-card {
  padding: 1.5rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  background: #fff;
}
.service-card h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin-bottom: 0.5rem;
}
.service-card p {
  font-size: 0.85rem;
  color: var(--color-neutral-600);
  line-height: 1.65;
  margin-bottom: 1rem;
}
.service-link {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}
.service-link:hover {
  text-decoration: underline;
}

/* Process */
.process-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.process-step {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}
.process-num {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-primary-50);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.process-step h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin-bottom: 0.2rem;
}
.process-step p {
  font-size: 0.82rem;
  color: var(--color-neutral-600);
  line-height: 1.6;
}

/* Guarantees */
.guarantees-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 4rem;
  align-items: start;
}
.guarantees-list {
  list-style: none;
  padding: 0;
  margin-top: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}
.guarantees-list li {
  font-size: 0.875rem;
  color: var(--color-neutral-700);
}

.contact-aside {
  padding: 1.5rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  background: var(--color-neutral-50);
}
.contact-aside h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin-bottom: 0.75rem;
}
.contact-aside a {
  display: block;
  font-size: 0.85rem;
  color: var(--color-primary);
  text-decoration: none;
  margin-bottom: 0.35rem;
}
.contact-aside a:hover { text-decoration: underline; }
.hours {
  font-size: 0.78rem;
  color: var(--color-neutral-500);
  margin-top: 0.75rem;
}

@media (max-width: 768px) {
  .process-list { grid-template-columns: 1fr 1fr; }
  .guarantees-layout { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .process-list { grid-template-columns: 1fr; }
}
</style>
