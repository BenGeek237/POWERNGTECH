<template>
  <section class="hero" aria-label="Section principale">
    <div class="hero-bg" aria-hidden="true">
      <div class="hero-gradient"></div>
      <div class="hero-pattern"></div>
    </div>
    <div class="container hero-content">
      <div class="hero-text fade-in">
        <div class="hero-badge">
          <Zap :size="14" class="text-secondary-dark" />
          <span>Formation &amp; Innovation Technologique au Cameroun</span>
        </div>
        <h1 class="hero-title">
          Maîtrisez les
          <span class="hero-title-accent">technologies de demain</span>
          dès aujourd'hui
        </h1>
        <p class="hero-subtitle">
          POWER NG TECHNOLOGIE vous propose des formations pratiques en énergie solaire,
          électronique et électrotechnique, ainsi que des équipements professionnels de qualité.
        </p>
        <div class="hero-actions">
          <RouterLink to="/formations" class="btn btn-lg hero-btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            Voir les formations
          </RouterLink>
          <RouterLink to="/boutique" class="btn btn-lg btn-outline-white">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4zM3 6h18"/><path d="M16 10a4 4 0 01-8 0"/></svg>
            Voir les produits
          </RouterLink>
        </div>
        <!-- Stats -->
        <div class="hero-stats">
          <div class="stat-item" v-for="stat in stats" :key="stat.label">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
      <!-- Hero visual -->
      <div class="hero-visual fade-in" style="animation-delay:0.2s">
        <div class="hero-card-main">
          <div class="hero-card-icon"><Sun :size="32" class="text-warning" /></div>
          <div class="hero-card-text">
            <strong>Formation Solaire</strong>
            <span>Installation &amp; Maintenance</span>
          </div>
          <div class="hero-card-badge">Populaire</div>
        </div>
        <div class="hero-floating-cards">
          <div class="floating-card fc-1">
            <Zap :size="16" class="text-warning" />
            <span>Électrotechnique</span>
          </div>
          <div class="floating-card fc-2">
            <Wrench :size="16" class="text-neutral-400" />
            <span>Maintenance</span>
          </div>
          <div class="floating-card fc-3">
            <Snowflake :size="16" class="text-info" />
            <span>Climatisation</span>
          </div>
        </div>
        <div class="hero-decoration" aria-hidden="true">
          <div class="deco-circle deco-1"></div>
          <div class="deco-circle deco-2"></div>
        </div>
      </div>
    </div>
    <!-- Wave separator -->
    <div class="hero-wave" aria-hidden="true">
      <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
        <path d="M0,64L80,58.7C160,53,320,43,480,48C640,53,800,75,960,74.7C1120,75,1280,53,1360,42.7L1440,32L1440,80L1360,80C1280,80,1120,80,960,80C800,80,640,80,480,80C320,80,160,80,80,80L0,80Z" fill="white"/>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { Zap, Sun, Wrench, Snowflake } from 'lucide-vue-next';

const stats = [
  { value: "5", label: "Étudiants formés" },
  { value: "20+", label: "Formations disponibles" },
  { value: "5", label: "Années d'expérience" },
  { value: "100%", label: "Pratique garantie" },
];
</script>

<style scoped>
.hero {
  position: relative;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 50%, #1a4a7a 100%);
  color: #fff;
  padding: 5rem 0 7rem;
  overflow: hidden;
  min-height: 85vh;
  display: flex;
  align-items: center;
}

.hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-gradient {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(46,125,50,0.15) 0%, transparent 60%);
}
.hero-pattern {
  position: absolute; inset: 0;
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.04) 1px, transparent 0);
  background-size: 32px 32px;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
}

/* Text */
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 999px;
  padding: 0.35rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: rgba(255,255,255,0.9);
  margin-bottom: 1.5rem;
  backdrop-filter: blur(8px);
}

.hero-title {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 800;
  line-height: 1.2;
  color: #fff;
  margin-bottom: 1.25rem;
}
.hero-title-accent {
  color: var(--color-secondary-500);
  display: block;
}

.hero-subtitle {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.8);
  line-height: 1.7;
  margin-bottom: 2rem;
  max-width: 500px;
}

.hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 3rem; }
.hero-btn-primary {
  background: var(--color-secondary);
  color: #fff;
  border-color: var(--color-secondary);
}
.hero-btn-primary:hover {
  background: var(--color-secondary-dark);
  border-color: var(--color-secondary-dark);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(46,125,50,0.4);
}

/* Stats */
.hero-stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.15);
}
.stat-item { display: flex; flex-direction: column; gap: 0.2rem; }
.stat-value {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-secondary-500);
  line-height: 1;
}
.stat-label { font-size: 0.75rem; color: rgba(255,255,255,0.6); }

/* Visual */
.hero-visual { position: relative; display: flex; align-items: center; justify-content: center; }

.hero-card-main {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 1.75rem 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  z-index: 2;
  width: 280px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.hero-card-icon { font-size: 2.5rem; }
.hero-card-text { display: flex; flex-direction: column; gap: 0.2rem; }
.hero-card-text strong { font-size: 0.95rem; font-weight: 700; color: #fff; }
.hero-card-text span { font-size: 0.8rem; color: rgba(255,255,255,0.65); }
.hero-card-badge {
  position: absolute; top: -10px; right: 1rem;
  background: var(--color-secondary);
  color: #fff; font-size: 0.7rem; font-weight: 700;
  padding: 0.2rem 0.6rem; border-radius: 999px;
}

.hero-floating-cards {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
}
.floating-card {
  display: flex; align-items: center; gap: 0.5rem;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(255,255,255,0.9);
  white-space: nowrap;
  animation: float 3s ease-in-out infinite;
}
.fc-1 { animation-delay: 0s; }
.fc-2 { animation-delay: 0.5s; }
.fc-3 { animation-delay: 1s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.1);
}
.deco-1 { width: 300px; height: 300px; top: -50px; left: -80px; }
.deco-2 { width: 200px; height: 200px; bottom: -20px; right: -40px; }

/* Wave */
.hero-wave {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 80px;
  z-index: 2;
}
.hero-wave svg { width: 100%; height: 100%; display: block; }

@media (max-width: 900px) {
  .hero { padding: 4rem 0 6rem; min-height: auto; }
  .hero-content { grid-template-columns: 1fr; gap: 2.5rem; }
  .hero-visual { display: none; }
  .hero-title { font-size: clamp(1.8rem, 6vw, 2.5rem); }
}
@media (max-width: 480px) {
  .hero-stats { gap: 1.25rem; }
  .hero-actions { flex-direction: column; }
}
</style>
