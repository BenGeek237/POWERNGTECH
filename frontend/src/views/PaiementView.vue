<template>
  <AppLayout>
    <div class="checkout-page">
      <div class="container">
        <!-- Breadcrumb -->
        <nav class="checkout-breadcrumb" aria-label="Breadcrumb">
          <RouterLink to="/" class="breadcrumb-link">Accueil</RouterLink>
          <ChevronRight :size="14" class="breadcrumb-sep" />
          <span class="breadcrumb-current">Paiement</span>
        </nav>

        <!-- Loading -->
        <div v-if="loading" class="checkout-skeleton">
          <div class="skeleton-card">
            <div class="skeleton-line w60"></div>
            <div class="skeleton-line w80"></div>
            <div class="skeleton-line w40"></div>
            <div class="skeleton-block"></div>
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="checkout-error">
          <div class="error-card">
            <div class="error-icon-wrap">
              <AlertCircle :size="40" stroke-width="1.5" />
            </div>
            <h2>Une erreur est survenue</h2>
            <p>{{ error }}</p>
            <button class="btn btn-outline" @click="$router.back()">
              <ArrowLeft :size="16" /> Retour
            </button>
          </div>
        </div>

        <!-- Checkout -->
        <div v-else class="checkout-layout">
          <!-- Main Card -->
          <div class="checkout-card">
            <!-- Security Badge -->
            <div class="security-header">
              <div class="shield-icon">
                <ShieldCheck :size="28" stroke-width="1.8" />
              </div>
              <div>
                <h1 class="checkout-title">Finaliser votre achat</h1>
                <p class="checkout-subtitle">Transaction sécurisée et chiffrée</p>
              </div>
            </div>

            <!-- Divider -->
            <div class="divider"></div>

            <!-- Order Summary -->
            <div class="order-summary">
              <div class="summary-label">
                <Package :size="16" />
                <span>Résumé de la commande</span>
              </div>
              <div class="summary-item">
                <div class="summary-item-info">
                  <span class="item-type-badge" :class="itemType === 'formation' ? 'badge-formation' : 'badge-order'">
                    {{ itemType === 'formation' ? 'Formation' : 'Commande' }}
                  </span>
                  <span class="item-title">{{ itemTitle }}</span>
                </div>
                <span class="item-price">{{ formatPrice(itemPrice) }} <small>FCFA</small></span>
              </div>
            </div>

            <!-- Divider -->
            <div class="divider"></div>

            <!-- Total -->
            <div class="order-total">
              <span class="total-label">Total à payer</span>
              <span class="total-amount">{{ formatPrice(itemPrice) }} <small>FCFA</small></span>
            </div>

            <form @submit.prevent="handlePayment">
              <!-- Phone Input -->
              <div class="form-group mb-4">
                <label for="phone" class="form-label">Numéro Mobile Money (MTN/Orange)</label>
                <div class="input-with-icon">
                  <span class="input-icon">📞</span>
                  <input
                    type="tel"
                    id="phone"
                    v-model="form.phone"
                    class="form-control"
                    placeholder="Ex: 6XXXXXXXX"
                    required
                  />
                </div>
                <small class="form-hint">Le numéro sur lequel le prélèvement sera effectué.</small>
              </div>

              <!-- Pay Button -->
              <button
                type="submit"
                class="pay-button"
                :disabled="processing"
                :class="{ 'is-processing': processing }"
              >
                <span v-if="processing" class="pay-spinner"></span>
                <Lock v-else :size="18" />
                <span>{{ processing ? "Traitement en cours..." : `Payer ${formatPrice(itemPrice)} FCFA` }}</span>
              </button>
            </form>

            <!-- Trust Indicators -->
            <div class="trust-section">
              <div class="trust-icons">
                <span class="trust-badge" title="Visa">
                  <svg viewBox="0 0 48 32" width="38" height="24"><rect width="48" height="32" rx="4" fill="#1A1F71"/><text x="24" y="21" text-anchor="middle" fill="#fff" font-size="13" font-weight="700" font-family="Arial">VISA</text></svg>
                </span>
                <span class="trust-badge" title="Mastercard">
                  <svg viewBox="0 0 48 32" width="38" height="24"><rect width="48" height="32" rx="4" fill="#2D2D2D"/><circle cx="19" cy="16" r="9" fill="#EB001B"/><circle cx="29" cy="16" r="9" fill="#F79E1B"/><path d="M24 9.3a9 9 0 010 13.4 9 9 0 010-13.4z" fill="#FF5F00"/></svg>
                </span>
                <span class="trust-badge" title="Mobile Money">
                  <svg viewBox="0 0 48 32" width="38" height="24"><rect width="48" height="32" rx="4" fill="#FFCC00"/><text x="24" y="18" text-anchor="middle" fill="#333" font-size="8" font-weight="700" font-family="Arial">MoMo</text><text x="24" y="26" text-anchor="middle" fill="#666" font-size="5" font-family="Arial">Money</text></svg>
                </span>
                <span class="trust-badge" title="Orange Money">
                  <svg viewBox="0 0 48 32" width="38" height="24"><rect width="48" height="32" rx="4" fill="#FF6600"/><text x="24" y="18" text-anchor="middle" fill="#fff" font-size="7" font-weight="700" font-family="Arial">Orange</text><text x="24" y="26" text-anchor="middle" fill="rgba(255,255,255,.8)" font-size="5" font-family="Arial">Money</text></svg>
                </span>
              </div>
              <p class="trust-text">
                <ShieldCheck :size="13" /> Paiement 100% sécurisé&ensp;•&ensp;Accès immédiat après paiement
              </p>
            </div>
          </div>

          <!-- Help Card -->
          <div class="help-card">
            <div class="help-item">
              <div class="help-icon"><Lock :size="18" /></div>
              <div>
                <strong>Paiement sécurisé</strong>
                <p>Vos données sont chiffrées et protégées.</p>
              </div>
            </div>
            <div class="help-item">
              <div class="help-icon"><Zap :size="18" /></div>
              <div>
                <strong>Accès instantané</strong>
                <p>Accédez à votre contenu dès la confirmation.</p>
              </div>
            </div>
            <div class="help-item">
              <div class="help-icon"><Headphones :size="18" /></div>
              <div>
                <strong>Support réactif</strong>
                <p>Notre équipe est disponible pour vous aider.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppLayout from "@/components/common/AppLayout.vue";
import { formationsApi, boutiqueApi, paiementsApi } from "@/services/api";
import { useUiStore } from "@/stores/ui";
import { useAuthStore } from "@/stores/auth";
import {
  ShieldCheck, Lock, Package, ChevronRight,
  AlertCircle, ArrowLeft, Zap, Headphones,
} from "lucide-vue-next";

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
  method: "PAWAPAY",
  phone: ""
});

function formatPrice(p) {
  return new Intl.NumberFormat("fr-FR").format(p);
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }

  // Pre-fill phone if available in profile
  if (authStore.user?.phone) {
    form.phone = authStore.user.phone;
  }

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
  } else if (route.query.type === 'commande' && route.query.id) {
    itemType.value = "order";
    itemId.value = route.query.id;
    try {
      const { data } = await boutiqueApi.getOrder(route.query.id);
      itemTitle.value = `Commande #${data.id}`;
      itemPrice.value = data.total_amount;
    } catch (err) {
      error.value = "Impossible de récupérer les informations de la commande.";
    } finally {
      loading.value = false;
    }
  } else {
    error.value = "Aucun article sélectionné valide.";
    loading.value = false;
  }
});

async function handlePayment() {
  processing.value = true;
  try {
    const payload = {
      provider: form.method,
      phone: form.phone,
    };
    if (itemType.value === "formation") {
      payload.formation_id = Number(itemId.value);
    } else {
      payload.order_id = Number(itemId.value);
    }

    const { data } = await paiementsApi.initiate(payload);

    if (data.payment_url) {
      window.location.href = data.payment_url;
    } else if (data.reference) {
      uiStore.showSuccess(data.message || "Paiement initié. Redirection...");
      router.push({ name: "payment-return", params: { reference: data.reference } });
    } else {
      uiStore.showError("Erreur lors de l'initiation du paiement.");
    }
  } catch (err) {
    uiStore.showError(err.response?.data?.error || "Une erreur est survenue lors de l'initialisation du paiement.");
  } finally {
    processing.value = false;
  }
}
</script>

<style scoped>
/* ── Page ────────────────────────────────────────── */
.checkout-page {
  padding: 2rem 0 5rem;
  min-height: 80vh;
  background:
    radial-gradient(ellipse at 20% 0%, rgba(22,163,74,.04) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 100%, rgba(217,119,6,.03) 0%, transparent 60%),
    var(--color-neutral-50);
}

/* ── Breadcrumb ──────────────────────────────────── */
.checkout-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: var(--color-neutral-500);
  margin-bottom: 2rem;
}
.breadcrumb-link {
  color: var(--color-neutral-500);
  transition: color var(--transition-fast);
}
.breadcrumb-link:hover { color: var(--color-primary); }
.breadcrumb-sep { color: var(--color-neutral-300); flex-shrink: 0; }
.breadcrumb-current { color: var(--color-primary-dark); font-weight: 600; }

/* ── Layout ──────────────────────────────────────── */
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  align-items: start;
  max-width: 820px;
  margin: 0 auto;
}

/* ── Main Card ───────────────────────────────────── */
.checkout-card {
  background: #fff;
  border-radius: var(--radius-xl);
  box-shadow:
    0 1px 3px rgba(0,0,0,.04),
    0 8px 32px rgba(0,0,0,.06);
  padding: 2.5rem;
  animation: fadeSlideUp 0.5s ease both;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Security Header ─────────────────────────────── */
.security-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.shield-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100));
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.checkout-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--color-primary-dark);
  margin: 0;
  line-height: 1.2;
}
.checkout-subtitle {
  font-size: 0.82rem;
  color: var(--color-neutral-500);
  margin: 0.15rem 0 0;
}

/* ── Divider ─────────────────────────────────────── */
.divider {
  height: 1px;
  background: var(--color-neutral-100);
  margin: 1.5rem 0;
}

/* ── Order Summary ───────────────────────────────── */
.summary-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-neutral-500);
  margin-bottom: 1rem;
}
.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg);
  background: var(--color-neutral-50);
  border: 1px solid var(--color-neutral-100);
}
.summary-item-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}
.item-type-badge {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  flex-shrink: 0;
}
.badge-formation {
  background: var(--color-primary-50);
  color: var(--color-primary);
}
.badge-order {
  background: var(--color-secondary-50);
  color: var(--color-secondary);
}
.item-title {
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--color-neutral-800);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.item-price {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--color-primary-dark);
  white-space: nowrap;
  margin-left: 1rem;
}
.item-price small {
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--color-neutral-500);
}

/* ── Total ───────────────────────────────────────── */
.order-total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.75rem;
}
.total-label {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-neutral-700);
}
.total-amount {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--color-primary-dark);
}
.total-amount small {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-neutral-500);
}

/* ── Form Inputs ─────────────────────────────────── */
.form-group {
  margin-bottom: 1.5rem;
}
.form-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-neutral-700);
  margin-bottom: 0.4rem;
}
.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 1.1rem;
  color: var(--color-neutral-400);
  pointer-events: none;
}
.form-control {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.5rem;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: var(--font-body);
  color: var(--color-neutral-800);
  background: var(--color-neutral-50);
  transition: all var(--transition-fast);
}
.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}
.form-hint {
  display: block;
  font-size: 0.75rem;
  color: var(--color-neutral-500);
  margin-top: 0.3rem;
}

/* ── Pay Button ──────────────────────────────────── */
.pay-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  width: 100%;
  padding: 1rem 2rem;
  font-family: var(--font-body);
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, var(--color-primary) 0%, #15803d 100%);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all var(--transition-normal);
  box-shadow:
    0 4px 14px rgba(22,163,74,.25),
    0 1px 3px rgba(22,163,74,.15);
}
.pay-button::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.15) 0%, transparent 50%);
  opacity: 0;
  transition: opacity var(--transition-normal);
}
.pay-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow:
    0 8px 24px rgba(22,163,74,.3),
    0 2px 6px rgba(22,163,74,.2);
}
.pay-button:hover:not(:disabled)::before { opacity: 1; }
.pay-button:active:not(:disabled) {
  transform: translateY(0);
}
.pay-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* ── Processing spinner ──────────────────────────── */
.pay-spinner {
  width: 20px;
  height: 20px;
  border: 2.5px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Trust Section ───────────────────────────────── */
.trust-section {
  margin-top: 1.75rem;
  text-align: center;
}
.trust-icons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.trust-badge {
  display: flex;
  opacity: 0.55;
  transition: opacity var(--transition-fast);
}
.trust-badge:hover { opacity: 0.85; }
.trust-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  font-size: 0.72rem;
  color: var(--color-neutral-400);
  font-weight: 500;
}

/* ── Help Card ───────────────────────────────────── */
.help-card {
  background: #fff;
  border-radius: var(--radius-xl);
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  animation: fadeSlideUp 0.5s ease 0.15s both;
}
.help-item {
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
}
.help-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--color-primary-50);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.help-item strong {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--color-neutral-800);
  display: block;
}
.help-item p {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
  margin: 0.15rem 0 0;
  line-height: 1.45;
}

/* ── Skeleton ────────────────────────────────────── */
.checkout-skeleton {
  max-width: 520px;
  margin: 0 auto;
}
.skeleton-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 2.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.skeleton-line {
  height: 14px;
  border-radius: 8px;
  background: linear-gradient(90deg, var(--color-neutral-100) 25%, var(--color-neutral-50) 50%, var(--color-neutral-100) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.skeleton-block {
  height: 52px;
  border-radius: var(--radius-lg);
  background: linear-gradient(90deg, var(--color-neutral-100) 25%, var(--color-neutral-50) 50%, var(--color-neutral-100) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  margin-top: 0.5rem;
}
.w40 { width: 40%; }
.w60 { width: 60%; }
.w80 { width: 80%; }
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── Error Card ──────────────────────────────────── */
.checkout-error {
  max-width: 440px;
  margin: 0 auto;
}
.error-card {
  background: #fff;
  border-radius: var(--radius-xl);
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  padding: 3rem 2.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
.error-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #FEF2F2;
  color: #DC2626;
  display: flex;
  align-items: center;
  justify-content: center;
}
.error-card h2 {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-neutral-800);
  margin: 0;
}
.error-card p {
  font-size: 0.875rem;
  color: var(--color-neutral-500);
  margin: 0;
}

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 768px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
  .checkout-card {
    padding: 1.75rem;
  }
  .help-card {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .help-item {
    flex: 1;
    min-width: 140px;
  }
  .checkout-title {
    font-size: 1.2rem;
  }
  .total-amount {
    font-size: 1.35rem;
  }
}

@media (max-width: 480px) {
  .checkout-page {
    padding: 1.25rem 0 3rem;
  }
  .checkout-card {
    padding: 1.5rem;
    border-radius: var(--radius-lg);
  }
  .security-header {
    flex-direction: column;
    text-align: center;
  }
  .summary-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  .item-price {
    margin-left: 0;
  }
  .help-card {
    flex-direction: column;
  }
  .help-item {
    min-width: 100%;
  }
}
</style>
