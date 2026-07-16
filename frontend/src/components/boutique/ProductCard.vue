<template>
  <RouterLink :to="`/boutique/${product.slug}`" class="product-card">
    <div class="product-thumb">
      <img
        v-if="primaryImage"
        :src="primaryImage"
        :alt="product.name"
        loading="lazy"
      />
      <div v-else class="product-thumb-placeholder">
        <span>📦</span>
      </div>
      <div class="product-availability" :class="product.is_available ? 'available' : 'unavailable'">
        <span class="availability-dot"></span>
        {{ product.is_available ? "En stock" : "Épuisé" }}
      </div>
    </div>
    <div class="product-content">
      <p class="product-category">{{ product.category?.name }}</p>
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-footer">
        <span class="product-price">{{ formatPrice(product.price) }} <small>FCFA</small></span>
        <span class="product-cta" v-if="product.is_available">
          Voir
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  product: { type: Object, required: true },
});

const primaryImage = computed(() => {
  return props.product.primary_image || null;
});

function formatPrice(price) {
  return new Intl.NumberFormat("fr-FR").format(price);
}
</script>

<style scoped>
.product-card {
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
.product-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}
.product-thumb {
  position: relative;
  height: 200px;
  background: var(--color-neutral-50);
  overflow: hidden;
}
.product-thumb img {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform var(--transition-slow);
}
.product-card:hover .product-thumb img { transform: scale(1.05); }
.product-thumb-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 3.5rem;
  background: linear-gradient(135deg, var(--color-neutral-50), var(--color-neutral-100));
}
.product-availability {
  position: absolute;
  top: 0.6rem; right: 0.6rem;
  display: flex; align-items: center; gap: 0.3rem;
  font-size: 0.7rem; font-weight: 600;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  backdrop-filter: blur(4px);
}
.available { background: rgba(240,253,244,0.9); color: #15803d; }
.unavailable { background: rgba(254,242,242,0.9); color: #991b1b; }
.availability-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: currentColor;
}
.product-content { padding: 1rem 1.15rem; }
.product-category {
  font-size: 0.7rem; font-weight: 600;
  color: var(--color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.4rem;
}
.product-name {
  font-size: 0.9rem; font-weight: 600;
  color: var(--color-primary-dark);
  line-height: 1.4;
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.6rem;
  border-top: 1px solid var(--color-neutral-100);
}
.product-price {
  font-family: var(--font-heading);
  font-size: 1rem; font-weight: 700;
  color: var(--color-primary);
}
.product-price small { font-size: 0.7rem; font-weight: 400; }
.product-cta {
  display: flex; align-items: center; gap: 0.3rem;
  font-size: 0.8rem; font-weight: 600;
  color: var(--color-primary);
  transition: gap var(--transition-fast);
}
.product-card:hover .product-cta { gap: 0.5rem; }
</style>
