<template>
  <AppLayout>
    <div v-if="loading" class="page-loading"><div class="spinner" style="width:3rem;height:3rem;border-width:3px"></div></div>
    <template v-else-if="product">
      <div class="product-hero">
        <div class="container product-hero-inner">
          <div class="product-gallery">
            <div class="main-image">
              <img v-if="selectedImage" :src="selectedImage.image" :alt="product.name" />
              <div v-else class="no-image">📦</div>
            </div>
            <div v-if="product.images?.length > 1" class="thumbnails">
              <button v-for="img in product.images" :key="img.id" class="thumb" :class="{active:selectedImage?.id===img.id}" @click="selectedImage=img">
                <img :src="img.image" :alt="img.alt_text || product.name" />
              </button>
            </div>
          </div>
          <div class="product-info">
            <p class="product-category">{{ product.category?.name }}</p>
            <h1 class="product-name">{{ product.name }}</h1>
            <div class="product-price-row">
              <span class="product-price">{{ formatPrice(product.price) }} FCFA</span>
              <span class="availability" :class="product.is_available?'available':'unavailable'">
                {{ product.is_available ? '✅ En stock' : '❌ Épuisé' }}
              </span>
            </div>
            <p class="product-desc">{{ product.description }}</p>
            <div v-if="product.specs?.length" class="specs-table">
              <h3>Caractéristiques</h3>
              <table>
                <tr v-for="spec in product.specs" :key="spec.key">
                  <td class="spec-key">{{ spec.key }}</td>
                  <td class="spec-val">{{ spec.value }}</td>
                </tr>
              </table>
            </div>
            <button v-if="product.is_available" @click="addToOrder" class="btn btn-primary btn-lg" style="width:100%">
              Acheter ce produit
            </button>
          </div>
        </div>
      </div>
    </template>
    <div v-else class="container" style="text-align:center;padding:5rem 0">
      <span style="font-size:4rem">😕</span><h1>Produit introuvable</h1>
      <RouterLink to="/boutique" class="btn btn-primary" style="margin-top:1rem">Retour à la boutique</RouterLink>
    </div>
  </AppLayout>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppLayout from "@/components/common/AppLayout.vue";
import { boutiqueApi } from "@/services/api";
import { useAuthStore } from "@/stores/auth";
const route = useRoute(); const router = useRouter(); const authStore = useAuthStore();
const product = ref(null); const loading = ref(true); const selectedImage = ref(null);
function formatPrice(p) { return new Intl.NumberFormat("fr-FR").format(p); }
function addToOrder() {
  if (!authStore.isAuthenticated) { router.push({ name:"login", query:{redirect:route.fullPath} }); return; }
  alert("Fonctionnalité commande à venir — contactez-nous directement pour acheter.");
}
onMounted(async () => {
  try {
    const { data } = await boutiqueApi.getProduct(route.params.slug);
    product.value = data;
    selectedImage.value = data.images?.find(i=>i.is_primary) || data.images?.[0] || null;
  } finally { loading.value = false; }
});
</script>
<style scoped>
.page-loading{min-height:60vh;display:flex;align-items:center;justify-content:center}
.product-hero{padding:3rem 0}
.product-hero-inner{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}
.main-image{border-radius:var(--radius-lg);overflow:hidden;aspect-ratio:4/3;background:var(--color-neutral-50);display:flex;align-items:center;justify-content:center}
.main-image img{width:100%;height:100%;object-fit:contain}
.no-image{font-size:5rem}
.thumbnails{display:flex;gap:.5rem;margin-top:.75rem;flex-wrap:wrap}
.thumb{width:70px;height:70px;border-radius:var(--radius-md);overflow:hidden;border:2px solid transparent;cursor:pointer;transition:border-color var(--transition-fast)}
.thumb.active{border-color:var(--color-primary)}
.thumb img{width:100%;height:100%;object-fit:cover}
.product-category{font-size:.72rem;font-weight:700;color:var(--color-secondary);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem}
.product-name{font-size:clamp(1.4rem,2.5vw,2rem);font-weight:800;color:var(--color-primary-dark);margin-bottom:1rem}
.product-price-row{display:flex;align-items:center;gap:1.25rem;margin-bottom:1.25rem;flex-wrap:wrap}
.product-price{font-family:var(--font-heading);font-size:1.75rem;font-weight:800;color:var(--color-primary)}
.availability{font-size:.875rem;font-weight:600}
.available{color:#15803d}.unavailable{color:#991b1b}
.product-desc{color:var(--color-neutral-600);line-height:1.7;margin-bottom:1.5rem}
.specs-table{margin-bottom:1.5rem}
.specs-table h3{font-size:.9rem;font-weight:700;margin-bottom:.75rem;color:var(--color-primary-dark)}
.specs-table table{width:100%;border-collapse:collapse}
.specs-table tr:nth-child(even){background:var(--color-neutral-50)}
.spec-key,.spec-val{padding:.6rem .75rem;font-size:.875rem;border-bottom:1px solid var(--color-neutral-100)}
.spec-key{font-weight:600;color:var(--color-neutral-700);width:40%}
.spec-val{color:var(--color-neutral-800)}
@media(max-width:768px){.product-hero-inner{grid-template-columns:1fr}}
</style>
