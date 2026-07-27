<template>
  <section class="hero" aria-label="Section principale">
    <div class="container hero-content">
      <div class="hero-text">
        <h1 class="hero-title">
          Formations professionnelles en
          <span class="hero-title-accent">énergie & technologie</span>
        </h1>
        <p class="hero-subtitle">
          POWER NG TECHNOLOGIE vous forme aux métiers de l'énergie solaire,
          de l'électronique et de l'électrotechnique. Des formations pratiques
          encadrées par des professionnels.
        </p>
        <div class="hero-actions">
          <RouterLink to="/formations" class="btn btn-lg btn-primary">
            Voir les formations
          </RouterLink>
          <RouterLink to="/boutique" class="btn btn-lg btn-outline-white">
            Boutique
          </RouterLink>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">5 ans</span>
            <span class="stat-label">d'expérience</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">5</span>
            <span class="stat-label">étudiants formés</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">20+</span>
            <span class="stat-label">formations</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <img src="@/assets/hero.png" alt="Formation en énergie solaire" class="hero-image" />
      </div>
    </div>
  </section>
</template>

<script setup>
// No complex imports needed — clean hero
</script>

<style scoped>
.hero {
  background: var(--color-primary-dark);
  color: #fff;
  padding: 6rem 0 5rem;
  overflow: hidden;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
}

.hero-title {
  font-size: clamp(1.9rem, 3.5vw, 2.8rem);
  font-weight: 700;
  line-height: 1.25;
  color: #fff;
  margin-bottom: 1.25rem;
}
.hero-title-accent {
  color: var(--color-secondary);
}

.hero-subtitle {
  font-size: 1rem;
  color: rgba(255,255,255,0.7);
  line-height: 1.75;
  margin-bottom: 2rem;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}


.hero-stats {
  display: flex;
  gap: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.12);
}
.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.stat-value {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}
.stat-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.5);
}

.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-image {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
}

@media (max-width: 900px) {
  .hero { padding: 4rem 0 3rem; }
  .hero-content { grid-template-columns: 1fr; gap: 2rem; }
  .hero-visual { display: none; }
}
@media (max-width: 480px) {
  .hero-stats { gap: 1.5rem; }
  .hero-actions { flex-direction: column; }
}
</style>
