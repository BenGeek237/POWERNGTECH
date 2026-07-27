<template>
  <AppLayout>
    <div class="payment-page">
      <div class="container">
        <div class="payment-card card">
          <div v-if="loading" class="payment-loading">
            <div class="spinner" style="width:3rem;height:3rem;border-width:3px"></div>
            <p>Chargement des détails...</p>
          </div>
          <div v-else-if="error" class="payment-error">
            <h2 class="text-error">Erreur</h2>
            <p>{{ error }}</p>
            <button class="btn btn-outline" @click="$router.back()" style="margin-top:1rem">Retour</button>
          </div>
          <div v-else class="payment-content">
            <div class="payment-header">
              <h2>Finaliser l'achat</h2>
              <div class="item-summary">
                <span class="item-name">{{ itemTitle }}</span>
                <span class="item-price">{{ formatPrice(itemPrice) }} FCFA</span>
              </div>
            </div>

            <form @submit.prevent="handlePayment" class="payment-form">
              <!-- Payment Method Selection -->
              <div class="form-group">
                <label class="form-label">Mode de paiement</label>
                <div class="payment-methods">
                  <label class="method-label" :class="{ active: form.method === 'OM' }">
                    <input type="radio" v-model="form.method" value="OM" name="payment_method" />
                    <span class="method-content">
                      <span class="method-name">Orange Money</span>
                    </span>
                  </label>
                  <label class="method-label" :class="{ active: form.method === 'MOMO' }">
                    <input type="radio" v-model="form.method" value="MOMO" name="payment_method" />
                    <span class="method-content">
                      <span class="method-name">MTN Mobile Money</span>
                    </span>
                  </label>
                  <label class="method-label" :class="{ active: form.method === 'CARTE' }">
                    <input type="radio" v-model="form.method" value="CARTE" name="payment_method" />
                    <span class="method-content">
                      <span class="method-name">Carte Bancaire / International</span>
                    </span>
                  </label>
                </div>
              </div>

              <!-- Phone number (only for OM/MOMO) -->
              <div class="form-group" v-if="form.method === 'OM' || form.method === 'MOMO'">
                <label for="phone" class="form-label">Numéro de téléphone de paiement</label>
                <div class="phone-input-wrapper">
                  <span class="phone-prefix">{{ phonePrefix }}</span>
                  <input 
                    id="phone" 
                    v-model="rawPhone" 
                    type="tel" 
                    class="form-input phone-input" 
                    placeholder="6XX XXX XXX" 
                    required 
                  />
                </div>
                <p class="form-hint">Le numéro qui sera débité.</p>
              </div>

              <!-- General info for Carte -->
              <div class="form-group" v-if="form.method === 'CARTE'">
                <p class="form-hint">Vous allez être redirigé vers la plateforme sécurisée de notre partenaire pour effectuer le paiement par carte ou autre moyen de paiement international.</p>
              </div>

              <div class="payment-actions">
                <button type="submit" class="btn btn-primary btn-lg" style="width:100%" :disabled="processing">
                  <span v-if="processing" class="spinner" style="width:18px;height:18px;border-width:2px"></span>
                  {{ processing ? "Traitement..." : `Payer ${formatPrice(itemPrice)} FCFA` }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppLayout from "@/components/common/AppLayout.vue";
import { formationsApi, boutiqueApi, paiementsApi } from "@/services/api";
import { useUiStore } from "@/stores/ui";
import { useAuthStore } from "@/stores/auth";
import { getPrefixByCountryCode } from "@/utils/countries";

const route = useRoute();
const router = useRouter();
const uiStore = useUiStore();
const authStore = useAuthStore();

const loading = ref(true);
const processing = ref(false);
const error = ref("");

const itemType = ref("");
const itemId = ref("");
const itemTitle = ref("");
const itemPrice = ref(0);

const form = reactive({
  method: "OM",
  phone_number: ""
});

const phonePrefix = ref("+237"); // Default for Cameroon (MoMo/OM usually CM)
const rawPhone = ref("");

function formatPrice(p) { 
  return new Intl.NumberFormat("fr-FR").format(p); 
}

watch(rawPhone, () => {
  if (rawPhone.value.trim()) {
    form.phone_number = `${phonePrefix.value} ${rawPhone.value}`.trim();
  } else {
    form.phone_number = "";
  }
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  
  if (authStore.user?.country) {
    phonePrefix.value = getPrefixByCountryCode(authStore.user.country);
  }

  // Check query params
  if (route.query.type === 'formation' && route.query.id && route.query.slug) {
    itemType.value = "formation";
    itemId.value = route.query.id;
    try {
      const { data } = await formationsApi.getDetail(route.query.slug);
      itemTitle.value = data.title;
      itemPrice.value = data.price;
    } catch (err) {
      error.value = "Impossible de récupérer les informations de la formation.";
    } finally {
      loading.value = false;
    }
  } else {
    error.value = "Aucun article sélectionné valide.";
    loading.value = false;
  }
});

async function handlePayment() {
  if ((form.method === 'OM' || form.method === 'MOMO') && !form.phone_number.trim()) {
    uiStore.showError("Veuillez entrer un numéro de téléphone.");
    return;
  }

  processing.value = true;
  try {
    const payload = {
      content_type: itemType.value,
      object_id: itemId.value,
      method: form.method,
    };
    if (form.method === 'OM' || form.method === 'MOMO') {
      payload.phone_number = form.phone_number;
    }

    const { data } = await paiementsApi.initiate(payload);

    if (data.status === 'PENDING') {
      if (data.payment_url) {
        // Redirect to external gateway (e.g. CinetPay)
        window.location.href = data.payment_url;
      } else {
        // MoMo / OM pending message
        uiStore.showSuccess(data.message || "Paiement initié. Veuillez valider sur votre téléphone.");
        router.push({ name: "payment-return", params: { reference: data.reference } });
      }
    } else {
      uiStore.showError("Erreur lors de l'initiation du paiement.");
    }
  } catch (err) {
    uiStore.showError(err.response?.data?.error || "Une erreur est survenue.");
  } finally {
    processing.value = false;
  }
}
</script>

<style scoped>
.payment-page {
  padding: 4rem 0;
  min-height: 70vh;
  background: var(--color-neutral-50);
  display: flex;
  align-items: center;
  justify-content: center;
}
.payment-card {
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
  padding: 2.5rem;
}
.payment-loading, .payment-error {
  text-align: center;
  padding: 2rem 0;
}
.payment-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-neutral-200);
  padding-bottom: 1.5rem;
}
.payment-header h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-primary-dark);
  margin-bottom: 1rem;
}
.item-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-neutral-800);
}
.item-price {
  color: var(--color-primary);
}
.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.method-label {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.method-label:hover {
  border-color: var(--color-neutral-300);
  background: var(--color-neutral-50);
}
.method-label.active {
  border-color: var(--color-primary);
  background: var(--color-primary-50);
}
.method-content {
  font-weight: 600;
  color: var(--color-neutral-800);
}
.form-hint {
  font-size: 0.8rem;
  color: var(--color-neutral-500);
  margin-top: 0.5rem;
}
.payment-actions {
  margin-top: 2rem;
}
.phone-input-wrapper { display: flex; align-items: center; }
.phone-prefix {
  background: var(--color-neutral-100);
  border: 1px solid var(--color-neutral-300);
  border-right: none;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
  color: var(--color-neutral-700);
  font-size: 0.875rem;
  font-weight: 500;
  height: 42px;
  display: flex;
  align-items: center;
}
.phone-input { border-radius: 0 var(--radius-md) var(--radius-md) 0; }
</style>
