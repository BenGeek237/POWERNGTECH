<template>
  <div class="service-card card">
    <div class="service-icon-wrap">
      <div class="service-icon">
        <img v-if="service.image" :src="service.image" :alt="service.title" />
        <component v-else :is="iconComponent" :size="32" stroke-width="1.5" class="service-icon-svg" />
      </div>
    </div>
    <h3 class="service-title">{{ service.title }}</h3>
    <p class="service-desc">{{ service.description }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Sun, Zap, Wrench, Hammer, Snowflake, Settings, Monitor, Battery, BarChart } from 'lucide-vue-next';

const props = defineProps({ service: { type: Object, required: true } });

const iconMap = {
  "Sun": Sun, "solar-panel": Sun,
  "bolt": Zap, "zap": Zap, "Zap": Zap,
  "wrench": Wrench, "Wrench": Wrench,
  "tool": Hammer,
  "ac": Snowflake,
  "gear": Settings,
  "cpu": Monitor,
  "battery": Battery,
  "ChartBar": BarChart
};

const iconComponent = computed(() => {
  return iconMap[props.service.icon] || Settings;
});
</script>

<style scoped>
.service-card {
  padding: 2rem 1.5rem;
  text-align: center;
  border: none;
  background: #fff;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);
}
.service-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}
.service-icon-wrap { display: flex; justify-content: center; margin-bottom: 1.25rem; }
.service-icon {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100));
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.75rem;
  transition: transform var(--transition-normal), background var(--transition-normal);
}
.service-card:hover .service-icon {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-500));
  transform: scale(1.1) rotate(-3deg);
}
.service-icon img { width: 36px; height: 36px; object-fit: contain; }
.service-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-primary-dark);
  margin-bottom: 0.6rem;
}
.service-desc {
  font-size: 0.875rem;
  color: var(--color-neutral-600);
  line-height: 1.65;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
