<template>
  <AppLayout>
    <!-- Header -->
    <div class="page-header">
      <div class="container">
        <p class="page-label">À propos</p>
        <h1 class="page-title">POWER NG TECHNOLOGIE</h1>
        <p class="page-desc">
          Votre partenaire technologique basé à Ngaoundéré, Cameroun.
          Formation professionnelle et équipements de qualité depuis 2019.
        </p>
      </div>
    </div>

    <!-- Mission & Vision -->
    <section class="section">
      <div class="container">
        <div class="two-col">
          <div>
            <h2 class="h2">Notre mission</h2>
            <p class="text">
              Contribuer au développement technologique du Cameroun en formant
              des professionnels qualifiés et en fournissant des équipements
              de qualité adaptés aux réalités locales.
            </p>
            <p class="text">
              Face à l'essor des énergies renouvelables et à la demande croissante
              de compétences spécialisées, nous avons décidé d'agir concrètement
              en ouvrant notre centre de formation à Ngaoundéré.
            </p>
          </div>
          <div>
            <h2 class="h2">Notre vision</h2>
            <p class="text">
              Devenir le centre de référence en formation technologique en Afrique
              centrale, en démocratisant l'accès aux compétences en énergie
              renouvelable et en électronique industrielle.
            </p>
            <p class="text">
              Nous croyons que chaque technicien formé est un pas vers
              l'autonomie énergétique du Cameroun.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="h2" style="margin-bottom: 2rem">Notre parcours</h2>
        <div class="timeline">
          <div v-for="event in timeline" :key="event.year" class="timeline-item">
            <span class="timeline-year">{{ event.year }}</span>
            <p class="timeline-text">{{ event.event }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Valeurs -->
    <section class="section">
      <div class="container">
        <h2 class="h2" style="margin-bottom: 2rem">Nos valeurs</h2>
        <div class="values-grid">
          <div v-for="val in values" :key="val.title" class="value-item">
            <h4>{{ val.title }}</h4>
            <p>{{ val.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Domaines -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="h2" style="margin-bottom: 2rem">Nos domaines d'intervention</h2>
        <div class="domains-grid">
          <div v-for="domain in domains" :key="domain" class="domain-item">
            {{ domain }}
          </div>
        </div>
      </div>
    </section>

    <!-- Contact rapide -->
    <section class="section">
      <div class="container">
        <div class="contact-box">
          <div>
            <h2 class="h2">Contactez-nous</h2>
            <p class="text" style="margin-bottom: 1rem">
              Basés à Ngaoundéré, quartier Bali, nous sommes disponibles
              du lundi au samedi.
            </p>
            <div class="contact-info">
              <a href="tel:+237691242788">+237 691 242 788</a>
              <a href="mailto:christinoo120@gmail.com">christinoo120@gmail.com</a>
            </div>
          </div>
          <RouterLink to="/contact" class="btn btn-primary">
            Nous écrire
          </RouterLink>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import AppLayout from "@/components/common/AppLayout.vue";

const timeline = [
  { year: "2019", event: "Création de l'entreprise à Ngaoundéré." },
  { year: "2020", event: "Lancement des premières formations en énergie solaire." },
  { year: "2021", event: "Immatriculation officielle POWER.NG TECHNOLOGY SARL. Ouverture de la boutique." },
  { year: "2022", event: "Extension aux formations en électrotechnique et climatisation." },
  { year: "2024", event: "Lancement de la plateforme de formation en ligne." },
];

const values = [
  { title: "Excellence", desc: "Qualité de service et de formation irréprochable." },
  { title: "Confiance", desc: "Relations durables et transparentes avec nos clients." },
  { title: "Innovation", desc: "Solutions adaptées aux réalités et besoins africains." },
  { title: "Développement", desc: "Engagement pour la montée en compétences locales." },
];

const domains = [
  "Énergie solaire",
  "Électrotechnique",
  "Électronique",
  "Climatisation & Froid",
  "Maintenance industrielle",
  "Formation professionnelle",
];
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
  max-width: 520px;
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
  margin-bottom: 1rem;
}

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
}

/* Timeline */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
  border-left: 2px solid var(--color-neutral-200);
  padding-left: 2rem;
}
.timeline-item {
  position: relative;
  padding-bottom: 1.75rem;
}
.timeline-item::before {
  content: '';
  position: absolute;
  left: -2.35rem;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-primary);
}
.timeline-year {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-primary);
}
.timeline-text {
  font-size: 0.875rem;
  color: var(--color-neutral-700);
  margin-top: 0.2rem;
}

/* Values */
.values-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.value-item {
  padding: 1.25rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  background: #fff;
}
.value-item h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin-bottom: 0.35rem;
}
.value-item p {
  font-size: 0.82rem;
  color: var(--color-neutral-600);
  line-height: 1.6;
}

/* Domains */
.domains-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.domain-item {
  padding: 0.5rem 1.1rem;
  border: 1px solid var(--color-neutral-300);
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-neutral-700);
  background: #fff;
}

/* Contact box */
.contact-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 3rem;
  padding: 2rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
}
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.contact-info a {
  font-size: 0.875rem;
  color: var(--color-primary);
  text-decoration: none;
}
.contact-info a:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .two-col { grid-template-columns: 1fr; gap: 2rem; }
  .values-grid { grid-template-columns: 1fr 1fr; }
  .contact-box { flex-direction: column; text-align: center; }
}
@media (max-width: 480px) {
  .values-grid { grid-template-columns: 1fr; }
}
</style>
