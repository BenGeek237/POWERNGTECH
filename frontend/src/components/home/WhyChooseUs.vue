<template>
  <section class="section why-section">
    <div class="container">
      <div class="why-grid">
        <!-- Left: text -->
        <div class="why-text">
          <p class="section-label">Notre différence</p>
          <h2 class="section-title">Pourquoi nous choisir ?</h2>
          <p class="section-subtitle">
            POWER NG TECHNOLOGIE est votre partenaire de confiance pour la formation
            professionnelle et l'acquisition d'équipements de qualité au Cameroun.
          </p>
          <div class="advantages-list">
            <div v-for="adv in advantages" :key="adv.title" class="advantage-item">
              <div class="advantage-icon"><component :is="adv.icon" :size="20" stroke-width="2" class="text-primary-dark" /></div>
              <div>
                <h4 class="advantage-title">{{ adv.title }}</h4>
                <p class="advantage-desc">{{ adv.desc }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Right: visual stats -->
        <div class="why-visual">
          <div class="stats-card" v-for="stat in stats" :key="stat.label">
            <span class="stat-emoji"><component :is="stat.icon" :size="32" stroke-width="1.5" class="text-primary" /></span>
            <span class="stat-val">{{ stat.value }}</span>
            <span class="stat-lbl">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { UserCheck, Hammer, Lock, Target, PhoneCall, Zap, GraduationCap, BookOpen, Star, Trophy } from 'lucide-vue-next';

const advantages = [
  {
    icon: UserCheck,
    title: "Formateurs experts",
    desc: "Des professionnels qualifiés avec une expérience terrain reconnue."
  },
  {
    icon: Hammer,
    title: "Formation 100% pratique",
    desc: "Nos formations sont orientées terrain pour une mise en application immédiate."
  },
  {
    icon: Lock,
    title: "Paiement sécurisé",
    desc: "Transactions sécurisées via MTN MoMo, Orange Money et PayPal."
  },
  {
    icon: Target,
    title: "Programme personnalisé",
    desc: "Des formations sur mesure adaptées à vos besoins spécifiques."
  },
  {
    icon: PhoneCall,
    title: "Support continu",
    desc: "Un accompagnement technique après la formation pour assurer votre succès."
  },
  {
    icon: Zap,
    title: "Équipements certifiés",
    desc: "Nous vendons uniquement des équipements de qualité professionnelle testés."
  },
];

const stats = [
  { icon: GraduationCap, value: "5", label: "Diplômés" },
  { icon: BookOpen, value: "20+", label: "Formations" },
  { icon: Star, value: "4.8/5", label: "Satisfaction" },
  { icon: Trophy, value: "5", label: "Années" },
];
</script>

<style scoped>
.why-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  align-items: center;
}
.advantages-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 2rem;
}
.advantage-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}
.advantage-icon {
  width: 42px; height: 42px;
  background: var(--color-primary-50);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.advantage-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-primary-dark);
  margin-bottom: 0.2rem;
}
.advantage-desc {
  font-size: 0.83rem;
  color: var(--color-neutral-600);
  line-height: 1.55;
}

/* Visual stats */
.why-visual {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.stats-card {
  background: #fff;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl);
  padding: 1.75rem 1.25rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.stats-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.stat-emoji { font-size: 2rem; }
.stat-val {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--color-primary);
  line-height: 1;
}
.stat-lbl { font-size: 0.78rem; color: var(--color-neutral-600); font-weight: 500; }

@media (max-width: 900px) {
  .why-grid { grid-template-columns: 1fr; gap: 3rem; }
  .why-visual { order: -1; }
}
</style>
