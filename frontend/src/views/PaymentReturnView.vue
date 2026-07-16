<template>
  <AppLayout>
    <div class="payment-return">
      <div class="container payment-return-inner">
        <div v-if="loading" class="pr-loading">
          <div class="spinner" style="width:3rem;height:3rem;border-width:3px"></div>
          <p>Vérification du paiement en cours...</p>
        </div>
        <div v-else-if="payment" class="pr-result" :class="payment.status">
          <span class="pr-icon">{{ statusIcons[payment.status] || '❓' }}</span>
          <h1>{{ statusTitles[payment.status] || 'Statut inconnu' }}</h1>
          <p class="pr-desc">{{ statusDescs[payment.status] }}</p>
          <div class="pr-details">
            <div class="pr-detail"><span>Référence</span><strong><code>{{ payment.camerpay_reference }}</code></strong></div>
            <div class="pr-detail"><span>Montant</span><strong>{{ formatPrice(payment.amount) }} FCFA</strong></div>
          </div>
          <div class="pr-actions">
            <RouterLink to="/" class="btn btn-primary">Retour à l'accueil</RouterLink>
            <RouterLink v-if="payment.status === 'SUCCESS'" to="/compte/formations" class="btn btn-secondary">Mes formations</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import AppLayout from "@/components/common/AppLayout.vue";
import { paiementsApi } from "@/services/api";
const route = useRoute();
const payment = ref(null); const loading = ref(true);
const statusIcons = { SUCCESS:"✅", FAILED:"❌", CANCELLED:"🚫", PENDING:"⏳" };
const statusTitles = { SUCCESS:"Paiement réussi !", FAILED:"Paiement échoué", CANCELLED:"Paiement annulé", PENDING:"En attente de confirmation" };
const statusDescs = { SUCCESS:"Votre paiement a été traité avec succès. Vous avez maintenant accès à votre formation ou commande.", FAILED:"Le paiement n'a pas pu être traité. Veuillez réessayer ou contacter le support.", CANCELLED:"Le paiement a été annulé. Aucune somme n'a été débitée.", PENDING:"Votre paiement est en cours de traitement. Vous serez notifié dès la confirmation." };
function formatPrice(p) { return new Intl.NumberFormat("fr-FR").format(p); }
onMounted(async () => {
  try {
    const { data } = await paiementsApi.getStatus(route.params.reference);
    payment.value = data;
  } finally { loading.value = false; }
});
</script>
<style scoped>
.payment-return{min-height:70vh;display:flex;align-items:center;padding:3rem 0}
.payment-return-inner{max-width:560px;margin:auto;text-align:center}
.pr-loading{display:flex;flex-direction:column;align-items:center;gap:1rem;color:var(--color-neutral-600)}
.pr-result{display:flex;flex-direction:column;align-items:center;gap:1.25rem}
.pr-icon{font-size:4rem;line-height:1}
.pr-result h1{font-size:1.75rem;font-weight:800;color:var(--color-primary-dark)}
.pr-result.SUCCESS h1{color:var(--color-secondary-dark)}
.pr-result.FAILED h1{color:#991b1b}
.pr-desc{color:var(--color-neutral-600);line-height:1.65;font-size:.95rem}
.pr-details{background:var(--color-neutral-50);border-radius:var(--radius-md);padding:1rem 1.5rem;width:100%;display:flex;flex-direction:column;gap:.5rem}
.pr-detail{display:flex;justify-content:space-between;font-size:.875rem}
.pr-detail span{color:var(--color-neutral-600)}
.pr-actions{display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;margin-top:.5rem}
</style>
