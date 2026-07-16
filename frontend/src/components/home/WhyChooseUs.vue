<template>
  <section class="section">
    <div class="container">
      <div class="why-grid">
        <div class="why-text">
          <p class="section-label">Notre différence</p>
          <h2 class="section-title">Pourquoi nous choisir ?</h2>
          <p class="why-intro">
            POWER NG TECHNOLOGIE est votre partenaire de confiance pour la formation
            professionnelle et l'acquisition d'équipements de qualité au Cameroun.
          </p>
        </div>
        <div class="advantages-list">
          <div v-for="adv in advantages" :key="adv.title" class="advantage-item">
            <div class="advantage-number">{{ adv.num }}</div>
            <div>
              <h4 class="advantage-title">{{ adv.title }}</h4>
              <p class="advantage-desc">{{ adv.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const advantages = [
  {
    num: "01",
    title: "Formateurs expérimentés",
    desc: "Des professionnels du terrain avec une vraie expérience pratique, pas que de la théorie."
  },
  {
    num: "02",
    title: "100% pratique",
    desc: "Vous travaillez sur du vrai matériel dès le premier jour de formation."
  },
  {
    num: "03",
    title: "Programme personnalisé",
    desc: "Chaque formation est adaptée à votre niveau et vos objectifs professionnels."
  },
  {
    num: "04",
    title: "Équipements de qualité",
    desc: "Nous fournissons et vendons uniquement du matériel professionnel testé et certifié."
  },
  {
    num: "05",
    title: "Suivi après formation",
    desc: "Un accompagnement technique continu pour vous aider à réussir sur le terrain."
  },
  {
    num: "06",
    title: "Paiement flexible",
    desc: "Plusieurs modes de paiement acceptés : MTN MoMo, Orange Money, virement bancaire."
  },
];
</script>

<style scoped>
.why-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 4rem;
  align-items: start;
}

.why-intro {
  font-size: 0.95rem;
  color: var(--color-neutral-600);
  line-height: 1.75;
  margin-top: 1rem;
}

.advantages-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.advantage-item {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
}

.advantage-number {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-primary-50);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.advantage-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin-bottom: 0.25rem;
}

.advantage-desc {
  font-size: 0.82rem;
  color: var(--color-neutral-600);
  line-height: 1.6;
}

@media (max-width: 900px) {
  .why-grid { grid-template-columns: 1fr; gap: 2rem; }
  .advantages-list { grid-template-columns: 1fr; }
}
</style>
