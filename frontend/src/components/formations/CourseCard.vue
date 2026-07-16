<template>
  <RouterLink :to="`/formations/${formation.slug}`" class="course-card" :class="{ 'is-free': formation.is_free }">
    <!-- Thumbnail -->
    <div class="course-thumb">
      <img
        v-if="formation.image"
        :src="formation.image"
        :alt="formation.title"
        loading="lazy"
      />
            <div v-else class="course-thumb-placeholder">
        <GraduationCap :size="48" stroke-width="1" />
      </div>
      <!-- Badges -->
      <div class="course-badges">
        <span v-if="formation.is_free" class="badge badge-success">Gratuit</span>
        <span v-else class="badge badge-primary">
          {{ formatPrice(formation.price) }} FCFA
        </span>
        <span class="badge badge-neutral">{{ levelLabel }}</span>
      </div>
    </div>
    <!-- Content -->
    <div class="course-content">
      <p class="course-category">{{ formation.category?.name }}</p>
      <h3 class="course-title">{{ formation.title }}</h3>
      <!-- Meta -->
      <div class="course-meta">
        <div class="meta-item" title="Durée">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>{{ formation.duration_hours }}h</span>
        </div>
        <div class="meta-item" title="Vidéos">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
          <span>{{ formation.video_count }} vidéo{{ formation.video_count !== 1 ? 's' : '' }}</span>
        </div>
      </div>
      <!-- CTA -->
      <div class="course-footer">
        <span class="course-price">
          <template v-if="formation.is_free">Gratuit</template>
          <template v-else>{{ formatPrice(formation.price) }} FCFA</template>
        </span>
        <span class="course-cta-btn">
          Voir
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";
import { GraduationCap } from "lucide-vue-next";

const props = defineProps({
  formation: { type: Object, required: true },
});

const levelLabels = {
  DEBUTANT: "Débutant",
  INTERMEDIAIRE: "Intermédiaire",
  AVANCE: "Avancé",
};
const levelLabel = computed(() => levelLabels[props.formation.level] || props.formation.level);

function formatPrice(price) {
  return new Intl.NumberFormat("fr-FR").format(price);
}
</script>

<style scoped>
.course-card {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-neutral-200);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.course-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

/* Thumbnail */
.course-thumb {
  position: relative;
  height: 185px;
  overflow: hidden;
  background: var(--color-neutral-100);
  flex-shrink: 0;
}
.course-thumb img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}
.course-card:hover .course-thumb img { transform: scale(1.05); }
.course-thumb-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100));
  font-size: 3rem;
}
.course-badges {
  position: absolute;
  top: 0.75rem; left: 0.75rem;
  display: flex; gap: 0.4rem; flex-wrap: wrap;
}

/* Content */
.course-content {
  padding: 1.1rem 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.course-category {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.4rem;
}
.course-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-primary-dark);
  line-height: 1.4;
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.course-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: auto;
  padding-bottom: 1rem;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
  color: var(--color-neutral-600);
}
.course-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px solid var(--color-neutral-100);
}
.course-price {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-primary);
}
.is-free .course-price { color: var(--color-secondary-dark); }
.course-cta-btn {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-primary);
  transition: gap var(--transition-fast);
}
.course-card:hover .course-cta-btn { gap: 0.5rem; }
</style>
