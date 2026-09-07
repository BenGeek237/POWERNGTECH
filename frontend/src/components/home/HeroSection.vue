<template>
  <section class="hero" aria-label="Section principale">
    <!-- Animated background shapes -->
    <div class="hero-bg">
      <div class="hero-orb hero-orb-1"></div>
      <div class="hero-orb hero-orb-2"></div>
      <div class="hero-orb hero-orb-3"></div>
      <div class="hero-grid-pattern"></div>
    </div>

    <div class="container hero-content">
      <div class="hero-text">
        <div class="hero-badge">
          <Zap :size="14" />
          <span>Leader en formation technologique au Cameroun</span>
        </div>
        <h1 class="hero-title">
          Formations professionnelles en
          <span class="hero-title-accent">énergie &amp; technologie</span>
        </h1>
        <p class="hero-subtitle">
          POWER NG TECHNOLOGIE vous forme aux métiers de l'énergie renouvelable,
          de l'électronique, l'électronique de puissance, l'électrotechnique et l'informatique industrielle. Des formations pratiques
          encadrées par des professionnels.
        </p>
        <div class="hero-actions">
          <RouterLink to="/formations" class="hero-btn hero-btn-primary">
            <span>Voir les formations</span>
            <ArrowRight :size="18" />
          </RouterLink>
          <RouterLink to="/boutique" class="hero-btn hero-btn-outline">
            <ShoppingBag :size="18" />
            <span>Boutique</span>
          </RouterLink>
        </div>
        <div class="hero-stats">
          <div class="stat-item" v-for="stat in stats" :key="stat.label">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="hero-visual-card">
          <img src="@/assets/hero.png" alt="Formation en énergie solaire" class="hero-image" />
          <!-- Floating badge -->
          <div class="float-badge float-badge-1">
            <Sun :size="20" />
            <div>
              <strong>Énergie Solaire</strong>
              <small>Formation pratique</small>
            </div>
          </div>
          <div class="float-badge float-badge-2">
            <Award :size="20" />
            <div>
              <strong>Certifié</strong>
              <small>Formation reconnue</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ArrowRight, ShoppingBag, Zap, Sun, Award } from "lucide-vue-next";

const stats = [
  { value: "15 ans", label: "d'expérience" },
  { value: "500+", label: "étudiants formés" },
  { value: "20+", label: "formations" },
];
</script>

<style scoped>
/* ── Hero Base ───────────────────────────────────── */
.hero {
  background: linear-gradient(160deg, var(--color-primary-dark) 0%, #0c3b1e 40%, #0f172a 100%);
  color: #fff;
  padding: 6rem 0 5rem;
  overflow: hidden;
  position: relative;
}

/* ── Animated Background ─────────────────────────── */
.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}
.hero-orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);
  top: -20%; left: -5%;
  animation: float 8s ease-in-out infinite;
}
.hero-orb-2 {
  width: 350px; height: 350px;
  background: radial-gradient(circle, var(--color-secondary) 0%, transparent 70%);
  bottom: -10%; right: 10%;
  animation: float 10s ease-in-out infinite reverse;
  opacity: 0.25;
}
.hero-orb-3 {
  width: 200px; height: 200px;
  background: radial-gradient(circle, #22d3ee 0%, transparent 70%);
  top: 30%; right: 30%;
  animation: float 7s ease-in-out infinite 2s;
  opacity: 0.15;
}

.hero-grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* ── Content Grid ────────────────────────────────── */
.hero-content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
}

/* ── Badge ───────────────────────────────────────── */
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 999px;
  padding: 0.35rem 1rem 0.35rem 0.65rem;
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--color-secondary-500);
  margin-bottom: 1.5rem;
  animation: slideUp 0.6s ease both;
  backdrop-filter: blur(8px);
}

/* ── Title ───────────────────────────────────────── */
.hero-title {
  font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 800;
  line-height: 1.15;
  color: #fff;
  margin-bottom: 1.25rem;
  animation: slideUp 0.6s ease 0.1s both;
}
.hero-title-accent {
  background: linear-gradient(135deg, var(--color-secondary-500) 0%, var(--color-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── Subtitle ────────────────────────────────────── */
.hero-subtitle {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.6);
  line-height: 1.75;
  margin-bottom: 2rem;
  max-width: 480px;
  animation: slideUp 0.6s ease 0.2s both;
}

/* ── Buttons ─────────────────────────────────────── */
.hero-actions {
  display: flex;
  gap: 0.85rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
  animation: slideUp 0.6s ease 0.3s both;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.75rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: var(--radius-lg);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(.22,1,.36,1);
  cursor: pointer;
  border: 2px solid transparent;
}
.hero-btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, #15803d 100%);
  color: #fff;
  box-shadow: 0 4px 20px rgba(22,163,74,.3);
}
.hero-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(22,163,74,.4);
  color: #fff;
}
.hero-btn-outline {
  background: rgba(255,255,255,0.06);
  color: #fff;
  border-color: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
}
.hero-btn-outline:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.35);
  transform: translateY(-2px);
  color: #fff;
}

/* ── Stats ───────────────────────────────────────── */
.hero-stats {
  display: flex;
  gap: 2.5rem;
  padding-top: 1.75rem;
  border-top: 1px solid rgba(255,255,255,0.08);
  animation: slideUp 0.6s ease 0.4s both;
}
.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.stat-value {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  line-height: 1;
}
.stat-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.45);
  font-weight: 500;
}

/* ── Visual / Image ──────────────────────────────── */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  animation: scaleIn 0.7s ease 0.3s both;
}
.hero-visual-card {
  position: relative;
  border-radius: 20px;
  overflow: visible;
}
.hero-image {
  width: 100%;
  max-width: 460px;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,.3);
}

/* ── Floating Badges ─────────────────────────────── */
.float-badge {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(12px);
  border-radius: 14px;
  padding: 0.65rem 1rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.12);
  color: var(--color-primary-dark);
  white-space: nowrap;
}
.float-badge strong {
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
}
.float-badge small {
  display: block;
  font-size: 0.65rem;
  color: var(--color-neutral-500);
}
.float-badge svg {
  color: var(--color-secondary);
  flex-shrink: 0;
}
.float-badge-1 {
  top: 12%;
  right: -20px;
  animation: float 4s ease-in-out infinite, slideInRight 0.6s ease 0.6s both;
}
.float-badge-2 {
  bottom: 15%;
  left: -24px;
  animation: float 5s ease-in-out infinite 1.5s, slideInLeft 0.6s ease 0.8s both;
}

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 900px) {
  .hero { padding: 4rem 0 3rem; }
  .hero-content { grid-template-columns: 1fr; gap: 2.5rem; }
  .hero-visual { display: none; }
  .hero-title { font-size: clamp(1.8rem, 5vw, 2.4rem); }
}
@media (max-width: 480px) {
  .hero { padding: 3rem 0 2.5rem; }
  .hero-stats { gap: 1.5rem; }
  .hero-actions { flex-direction: column; }
  .hero-btn { width: 100%; justify-content: center; }
  .hero-badge { font-size: 0.7rem; }
}
</style>
