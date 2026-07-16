<template>
  <AppLayout>
    <!-- ── Hero ─────────────────────────────────────────── -->
    <div class="about-hero">
      <div class="about-hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
      </div>
      <div class="container about-hero-content">
        <div class="about-hero-text fade-in">
          <span class="hero-badge">
            <MapPin :size="14" />
            Ngaoundéré, Cameroun
          </span>
          <h1 class="about-hero-title">
            Votre partenaire technologique
            <span class="accent">en Afrique centrale</span>
          </h1>
          <p class="about-hero-sub">
            Depuis 5 ans, POWER NG TECHNOLOGIE forme des techniciens qualifiés et fournit
            des équipements professionnels dans les domaines de l'énergie solaire,
            de l'électronique et de l'électrotechnique.
          </p>
        </div>
        <!-- Stats banner -->
        <div class="about-stats fade-in" style="animation-delay:.2s">
          <div class="about-stat-item" v-for="stat in heroStats" :key="stat.label">
            <component :is="stat.icon" :size="24" stroke-width="1.5" class="stat-icon" />
            <span class="stat-val">{{ stat.value }}</span>
            <span class="stat-lbl">{{ stat.label }}</span>
          </div>
        </div>
      </div>
      <div class="hero-wave">
        <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
          <path d="M0,64L80,58.7C160,53,320,43,480,48C640,53,800,75,960,74.7C1120,75,1280,53,1360,42.7L1440,32L1440,80L1360,80C1280,80,1120,80,960,80C800,80,640,80,480,80C320,80,160,80,80,80L0,80Z" fill="white"/>
        </svg>
      </div>
    </div>

    <!-- ── Mission & Vision ───────────────────────────────── -->
    <section class="section">
      <div class="container">
        <div class="mission-grid">
          <div class="mission-card">
            <div class="mission-icon">
              <Target :size="32" stroke-width="1.5" />
            </div>
            <h3>Notre Mission</h3>
            <p>
              Contribuer au développement technologique du Cameroun en formant des
              professionnels qualifiés et en fournissant des équipements de qualité
              adaptés aux réalités locales.
            </p>
          </div>
          <div class="mission-card mission-card--accent">
            <div class="mission-icon">
              <Eye :size="32" stroke-width="1.5" />
            </div>
            <h3>Notre Vision</h3>
            <p>
              Devenir le centre de référence en formation technologique en Afrique
              centrale, en démocratisant l'accès aux compétences en énergie renouvelable
              et en électronique industrielle.
            </p>
          </div>
          <div class="mission-card">
            <div class="mission-icon">
              <Heart :size="32" stroke-width="1.5" />
            </div>
            <h3>Nos Valeurs</h3>
            <p>
              Excellence, confiance, innovation et engagement sont les piliers qui
              guident chacune de nos actions au service de nos étudiants et partenaires.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Notre Histoire ─────────────────────────────────── -->
    <section class="section section--alt">
      <div class="container story-layout">
        <div class="story-text">
          <p class="section-label">Notre histoire</p>
          <h2 class="section-title">Une aventure née d'une passion pour la technologie</h2>
          <p class="story-p">
            POWER NG TECHNOLOGIE est née de la volonté de combler un manque criant :
            le déficit de techniciens qualifiés dans les métiers de l'énergie au Cameroun.
            Face à l'essor des énergies renouvelables et à la demande croissante de
            compétences spécialisées, notre fondatrice a décidé d'agir.
          </p>
          <p class="story-p">
            Basée à Ngaoundéré, au cœur de la région de l'Adamaoua, notre entreprise
            rayonne dans tout le nord Cameroun. Nous proposons des formations intensives
            ancrées dans la réalité du terrain, avec du matériel professionnel et des
            formateurs expérimentés.
          </p>
          <!-- Timeline -->
          <div class="timeline">
            <div class="timeline-item" v-for="event in timeline" :key="event.year">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <span class="timeline-year">{{ event.year }}</span>
                <p class="timeline-event">{{ event.event }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="story-visual">
          <!-- Map card -->
          <div class="location-card card">
            <div class="location-map">
              <MapPin :size="48" stroke-width="1" class="map-pin-icon" />
              <div class="map-rings">
                <div class="ring ring-1"></div>
                <div class="ring ring-2"></div>
                <div class="ring ring-3"></div>
              </div>
            </div>
            <div class="location-info">
              <h4>Notre localisation</h4>
              <p>Ngaoundéré, Région de l'Adamaoua, Cameroun</p>
              <div class="location-tags">
                <span class="tag">Cameroun</span>
                <span class="tag">Afrique centrale</span>
              </div>
            </div>
          </div>
          <!-- Contact quick card -->
          <div class="contact-quick card">
            <h4>Contactez-nous</h4>
            <a href="tel:+237691242788" class="contact-q-item">
              <Phone :size="18" stroke-width="1.75" />
              +237 691 242 788
            </a>
            <a href="mailto:christinoo120@gmail.com" class="contact-q-item">
              <Mail :size="18" stroke-width="1.75" />
              christinoo120@gmail.com
            </a>
            <RouterLink to="/contact" class="btn btn-primary" style="width:100%;margin-top:.75rem">
              Nous écrire
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Valeurs ─────────────────────────────────────────── -->
    <section class="section">
      <div class="container">
        <div class="section-header" style="text-align:center;margin-bottom:3rem">
          <p class="section-label">Ce qui nous définit</p>
          <h2 class="section-title">Nos valeurs fondamentales</h2>
          <p class="section-subtitle" style="margin-inline:auto">
            Ces principes guident chaque décision et chaque interaction avec nos étudiants.
          </p>
        </div>
        <div class="values-grid">
          <div v-for="val in values" :key="val.title" class="value-card">
            <div class="value-icon-wrap" :style="`background:${val.color}1a`">
              <component :is="val.icon" :size="28" stroke-width="1.5" :style="`color:${val.color}`" />
            </div>
            <h4 class="value-title">{{ val.title }}</h4>
            <p class="value-desc">{{ val.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Domaines d'expertise ───────────────────────────── -->
    <section class="section section--alt">
      <div class="container">
        <div class="section-header" style="text-align:center;margin-bottom:3rem">
          <p class="section-label">Expertise</p>
          <h2 class="section-title">Nos domaines d'intervention</h2>
        </div>
        <div class="domains-grid">
          <div v-for="domain in domains" :key="domain.name" class="domain-card">
            <div class="domain-icon">
              <component :is="domain.icon" :size="36" stroke-width="1.25" />
            </div>
            <h4>{{ domain.name }}</h4>
            <p>{{ domain.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────────── -->
    <section class="section about-cta-section">
      <div class="container">
        <div class="about-cta">
          <div class="about-cta-text">
            <h2>Prêt à rejoindre notre communauté ?</h2>
            <p>Inscrivez-vous dès aujourd'hui et commencez votre parcours technologique.</p>
          </div>
          <div class="about-cta-actions">
            <RouterLink to="/formations" class="btn btn-lg" style="background:#fff;color:var(--color-primary)">
              Voir les formations
            </RouterLink>
            <RouterLink to="/contact" class="btn btn-lg btn-outline-white">
              Nous contacter
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import AppLayout from "@/components/common/AppLayout.vue";
import {
  Trophy, Handshake, FlaskConical, TrendingUp, Zap,
  MapPin, Target, Eye, Heart, Phone, Mail,
  Sun, Snowflake, Wrench, Radio, Battery, Factory
} from 'lucide-vue-next';

const heroStats = [
  { icon: Trophy, value: "5", label: "Ans d'expérience" },
  { icon: Zap, value: "5", label: "Étudiants formés" },
  { icon: FlaskConical, value: "20+", label: "Formations" },
  { icon: TrendingUp, value: "100%", label: "Pratique garantie" },
];

const timeline = [
  { year: "2019", event: "Création de POWER NG TECHNOLOGIE à Ngaoundéré." },
  { year: "2020", event: "Lancement des premières formations en énergie solaire." },
  { year: "2021", event: "Ouverture de la boutique d'équipements professionnels." },
  { year: "2022", event: "Extension aux formations en électrotechnique et climatisation." },
  { year: "2024", event: "Lancement de la plateforme de formation en ligne." },
];

const values = [
  { icon: Trophy,      title: "Excellence",    desc: "Qualité de service et de formation irréprochable dans chacune de nos interventions.", color: "#f59e0b" },
  { icon: Handshake,   title: "Confiance",     desc: "Relations durables et transparentes avec nos étudiants, clients et partenaires.", color: "#3b82f6" },
  { icon: FlaskConical, title: "Innovation",   desc: "Solutions technologiques modernes, adaptées aux réalités et besoins africains.", color: "#8b5cf6" },
  { icon: TrendingUp,  title: "Développement", desc: "Engagement fort pour la montée en compétences et l'essor des talents locaux.", color: "#22c55e" },
];

const domains = [
  { icon: Sun,      name: "Énergie Solaire",        desc: "Installation, dimensionnement et maintenance de systèmes photovoltaïques." },
  { icon: Zap,      name: "Électrotechnique",        desc: "Câblage, automatismes, moteurs électriques et tableaux de distribution." },
  { icon: Snowflake, name: "Climatisation",          desc: "Installation et entretien de systèmes de climatisation et de froid." },
  { icon: Wrench,   name: "Maintenance Industrielle", desc: "Diagnostic, réparation et maintenance préventive d'équipements industriels." },
  { icon: Radio,    name: "Électronique",            desc: "Circuits électroniques, microcontrôleurs et systèmes embarqués." },
  { icon: Factory,  name: "Industrie",               desc: "Automatisation industrielle, domotique et gestion de l'énergie." },
];
</script>

<style scoped>
/* ── Hero ─────────────────────────────────────────────── */
.about-hero {
  position: relative;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 50%, #1a4a7a 100%);
  color: #fff;
  padding: 5rem 0 7rem;
  overflow: hidden;
}
.about-hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-gradient {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(46,125,50,.15) 0%, transparent 60%);
}
.hero-pattern {
  position: absolute; inset: 0;
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,.04) 1px, transparent 0);
  background-size: 32px 32px;
}
.about-hero-content { position: relative; z-index: 1; }
.hero-badge {
  display: inline-flex; align-items: center; gap: .5rem;
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
  border-radius: 999px; padding: .35rem 1rem; font-size: .8rem; font-weight: 500;
  color: rgba(255,255,255,.9); margin-bottom: 1.5rem; backdrop-filter: blur(8px);
}
.about-hero-title {
  font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; line-height: 1.2;
  color: #fff; margin-bottom: 1rem;
}
.about-hero-title .accent { color: var(--color-secondary-500); display: block; }
.about-hero-sub {
  font-size: 1.05rem; color: rgba(255,255,255,.8); line-height: 1.7; max-width: 640px;
}

/* Stats */
.about-stats {
  display: flex; gap: 0; flex-wrap: wrap;
  background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.15);
  border-radius: var(--radius-xl); backdrop-filter: blur(12px);
  margin-top: 3rem; overflow: hidden;
}
.about-stat-item {
  flex: 1; min-width: 120px;
  display: flex; flex-direction: column; align-items: center;
  gap: .3rem; padding: 1.5rem 1rem; text-align: center;
  border-right: 1px solid rgba(255,255,255,.1);
}
.about-stat-item:last-child { border-right: none; }
.stat-icon { color: var(--color-secondary-500); margin-bottom: .2rem; }
.stat-val {
  font-family: var(--font-heading); font-size: 1.6rem; font-weight: 800;
  color: #fff; line-height: 1;
}
.stat-lbl { font-size: .72rem; color: rgba(255,255,255,.65); font-weight: 500; }

/* Wave */
.hero-wave { position: absolute; bottom: 0; left: 0; right: 0; height: 80px; z-index: 2; }
.hero-wave svg { width: 100%; height: 100%; display: block; }

/* ── Mission ─────────────────────────────────────────── */
.mission-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}
.mission-card {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 2rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.mission-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-4px); }
.mission-card--accent {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #fff; border-color: transparent;
}
.mission-card--accent h3, .mission-card--accent p { color: #fff !important; }
.mission-icon {
  width: 56px; height: 56px; border-radius: var(--radius-lg);
  background: var(--color-primary-50); display: flex; align-items: center;
  justify-content: center; color: var(--color-primary); margin-bottom: 1.25rem;
}
.mission-card--accent .mission-icon {
  background: rgba(255,255,255,.15); color: #fff;
}
.mission-card h3 {
  font-size: 1.1rem; font-weight: 700; color: var(--color-primary-dark);
  margin-bottom: .6rem;
}
.mission-card p { font-size: .875rem; color: var(--color-neutral-600); line-height: 1.7; }

/* ── Story ─────────────────────────────────────────────── */
.story-layout {
  display: grid; grid-template-columns: 1fr 340px; gap: 4rem; align-items: start;
}
.story-p { color: var(--color-neutral-600); line-height: 1.8; margin-bottom: 1.25rem; font-size: .95rem; }

/* Timeline */
.timeline { margin-top: 2rem; display: flex; flex-direction: column; gap: 0; }
.timeline-item {
  display: flex; gap: 1.25rem; position: relative;
  padding-bottom: 1.5rem;
}
.timeline-item:last-child { padding-bottom: 0; }
.timeline-item::before {
  content: ''; position: absolute; left: 7px; top: 16px;
  width: 2px; bottom: 0;
  background: linear-gradient(to bottom, var(--color-primary-200), transparent);
}
.timeline-item:last-child::before { display: none; }
.timeline-dot {
  width: 16px; height: 16px; border-radius: 50%;
  background: var(--color-primary); border: 3px solid var(--color-primary-100);
  flex-shrink: 0; margin-top: 4px;
}
.timeline-content { flex: 1; }
.timeline-year {
  font-family: var(--font-heading); font-size: .8rem; font-weight: 700;
  color: var(--color-primary); display: block; margin-bottom: .2rem;
}
.timeline-event { font-size: .875rem; color: var(--color-neutral-700); line-height: 1.6; }

/* Location & Contact cards */
.location-card {
  padding: 0; overflow: hidden; margin-bottom: 1.25rem;
}
.location-map {
  background: linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100));
  height: 150px; position: relative;
  display: flex; align-items: center; justify-content: center;
}
.map-pin-icon { color: var(--color-primary); position: relative; z-index: 2; }
.map-rings { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
.ring {
  position: absolute; border-radius: 50%;
  border: 1px solid var(--color-primary); opacity: .25;
  animation: ring-pulse 3s ease-in-out infinite;
}
.ring-1 { width: 80px; height: 80px; }
.ring-2 { width: 130px; height: 130px; animation-delay: .5s; }
.ring-3 { width: 180px; height: 180px; animation-delay: 1s; }
@keyframes ring-pulse {
  0%, 100% { opacity: .15; transform: scale(1); }
  50%       { opacity: .35; transform: scale(1.05); }
}
.location-info { padding: 1.25rem; }
.location-info h4 { font-size: .95rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .35rem; }
.location-info p { font-size: .8rem; color: var(--color-neutral-600); margin-bottom: .75rem; }
.location-tags { display: flex; gap: .4rem; flex-wrap: wrap; }
.tag {
  font-size: .7rem; font-weight: 600; padding: .2rem .6rem;
  background: var(--color-primary-50); color: var(--color-primary);
  border-radius: 999px;
}
.contact-quick {
  padding: 1.5rem;
}
.contact-quick h4 { font-size: .95rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: 1rem; }
.contact-q-item {
  display: flex; align-items: center; gap: .6rem;
  font-size: .875rem; color: var(--color-neutral-700); text-decoration: none;
  padding: .6rem .75rem; border-radius: var(--radius-sm);
  transition: background var(--transition-fast), color var(--transition-fast);
  margin-bottom: .35rem;
}
.contact-q-item:hover { background: var(--color-primary-50); color: var(--color-primary); }

/* ── Values ───────────────────────────────────────────── */
.values-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;
}
.value-card {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 1.75rem 1.5rem;
  text-align: center; box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.value-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-4px); }
.value-icon-wrap {
  width: 60px; height: 60px; border-radius: var(--radius-lg);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.1rem;
}
.value-title { font-size: .95rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .5rem; }
.value-desc { font-size: .82rem; color: var(--color-neutral-600); line-height: 1.65; }

/* ── Domains ───────────────────────────────────────────── */
.domains-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}
.domain-card {
  background: #fff; border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-xl); padding: 2rem;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.domain-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-4px); }
.domain-icon {
  width: 64px; height: 64px; border-radius: 16px;
  background: var(--color-primary-50); color: var(--color-primary);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.1rem;
}
.domain-card h4 { font-size: .95rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .5rem; }
.domain-card p { font-size: .825rem; color: var(--color-neutral-600); line-height: 1.65; }

/* ── CTA ───────────────────────────────────────────────── */
.about-cta-section {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 60%, var(--color-primary-500) 100%);
}
.about-cta {
  display: flex; align-items: center; justify-content: space-between; gap: 3rem; flex-wrap: wrap;
}
.about-cta-text h2 {
  font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 800; color: #fff; margin-bottom: .5rem;
}
.about-cta-text p { color: rgba(255,255,255,.75); font-size: .95rem; }
.about-cta-actions { display: flex; gap: 1rem; flex-wrap: wrap; flex-shrink: 0; }

/* Responsive */
@media (max-width: 1024px) {
  .values-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 900px) {
  .mission-grid { grid-template-columns: 1fr; }
  .story-layout { grid-template-columns: 1fr; }
  .domains-grid { grid-template-columns: repeat(2, 1fr); }
  .about-hero { padding: 4rem 0 6rem; }
}
@media (max-width: 640px) {
  .about-stats { flex-direction: column; }
  .about-stat-item { border-right: none; border-bottom: 1px solid rgba(255,255,255,.1); }
  .about-stat-item:last-child { border-bottom: none; }
  .domains-grid { grid-template-columns: 1fr; }
  .values-grid { grid-template-columns: 1fr; }
  .about-cta { flex-direction: column; text-align: center; }
  .about-cta-actions { justify-content: center; }
}
</style>
