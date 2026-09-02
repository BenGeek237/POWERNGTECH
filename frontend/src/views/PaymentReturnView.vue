<template>
  <AppLayout>
    <div class="return-page">
      <div class="container">
        <!-- Loading -->
        <div v-if="loading" class="return-loading">
          <div class="pulse-ring">
            <div class="pulse-circle"></div>
          </div>
          <p class="loading-text">Vérification du paiement en cours...</p>
          <p class="loading-hint">Veuillez patienter quelques instants</p>
        </div>

        <!-- Result -->
        <div v-else-if="payment" class="return-result" :class="`status-${payment.status}`">
          <!-- Success -->
          <div v-if="payment.status === 'SUCCESS'" class="result-card success-card">
            <div class="result-icon success-icon">
              <CheckCircle :size="48" stroke-width="1.5" />
            </div>
            <div class="confetti-burst">🎉</div>
            <h1>Paiement réussi !</h1>
            <p class="result-desc">
              Votre paiement a été traité avec succès. Vous avez maintenant accès à votre contenu.
            </p>
            <div class="result-details">
              <div class="detail-row">
                <span class="detail-label">Référence</span>
                <code class="detail-value">{{ payment.transaction_id || `PAY-${payment.id}` }}</code>
              </div>
              <div class="detail-row">
                <span class="detail-label">Montant</span>
                <span class="detail-value amount">{{ formatPrice(payment.amount) }} FCFA</span>
              </div>
            </div>
            <div class="result-actions">
              <RouterLink to="/compte/formations" class="btn btn-primary">
                <BookOpen :size="16" /> Mes formations
              </RouterLink>
              <RouterLink to="/" class="btn btn-outline">Retour à l'accueil</RouterLink>
            </div>
          </div>

          <!-- Pending -->
          <div v-else-if="payment.status === 'PENDING' || payment.status === 'INITIATED'" class="result-card pending-card">
            <div class="result-icon pending-icon">
              <Clock :size="48" stroke-width="1.5" />
            </div>
            <h1>En attente de confirmation</h1>
            <p class="result-desc">
              Votre paiement est en cours de traitement. Vous recevrez une confirmation dès que le paiement sera validé.
            </p>
            <div class="result-details">
              <div class="detail-row">
                <span class="detail-label">Référence</span>
                <code class="detail-value">{{ payment.transaction_id || `PAY-${payment.id}` }}</code>
              </div>
              <div class="detail-row">
                <span class="detail-label">Montant</span>
                <span class="detail-value">{{ formatPrice(payment.amount) }} FCFA</span>
              </div>
            </div>
            <div class="result-actions">
              <RouterLink to="/" class="btn btn-primary">Retour à l'accueil</RouterLink>
            </div>
          </div>

          <!-- Failed / Cancelled -->
          <div v-else class="result-card failed-card">
            <div class="result-icon failed-icon">
              <XCircle :size="48" stroke-width="1.5" />
            </div>
            <h1>{{ payment.status === 'CANCELLED' ? 'Paiement annulé' : 'Paiement échoué' }}</h1>
            <p class="result-desc">
              {{ payment.status === 'CANCELLED'
                ? "Le paiement a été annulé. Aucune somme n'a été débitée."
                : "Le paiement n'a pas pu être traité. Veuillez réessayer ou contacter le support."
              }}
            </p>
            <div class="result-details">
              <div class="detail-row">
                <span class="detail-label">Référence</span>
                <code class="detail-value">{{ payment.transaction_id || `PAY-${payment.id}` }}</code>
              </div>
              <div class="detail-row">
                <span class="detail-label">Montant</span>
                <span class="detail-value">{{ formatPrice(payment.amount) }} FCFA</span>
              </div>
            </div>
            <div class="result-actions">
              <button class="btn btn-primary" @click="$router.back()">
                <RotateCcw :size="16" /> Réessayer
              </button>
              <RouterLink to="/" class="btn btn-outline">Retour à l'accueil</RouterLink>
            </div>
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
import {
  CheckCircle, Clock, XCircle, BookOpen, RotateCcw
} from "lucide-vue-next";

const route = useRoute();
const payment = ref(null);
const loading = ref(true);

function formatPrice(p) {
  return new Intl.NumberFormat("fr-FR").format(p);
}

onMounted(async () => {
  try {
    const { data } = await paiementsApi.getStatus(route.params.reference);
    payment.value = data;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* ── Page ────────────────────────────────────────── */
.return-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  padding: 3rem 0;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(22,163,74,.04) 0%, transparent 60%),
    var(--color-neutral-50);
}

/* ── Loading ─────────────────────────────────────── */
.return-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}
.pulse-ring {
  position: relative;
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}
.pulse-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-primary-100);
  animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%      { transform: scale(1.15); opacity: 0.6; }
}
.loading-text {
  font-weight: 700;
  color: var(--color-neutral-800);
  font-size: 1.05rem;
}
.loading-hint {
  font-size: 0.82rem;
  color: var(--color-neutral-500);
}

/* ── Result Card ─────────────────────────────────── */
.result-card {
  max-width: 500px;
  margin: 0 auto;
  background: #fff;
  border-radius: var(--radius-xl);
  box-shadow:
    0 1px 3px rgba(0,0,0,.04),
    0 8px 32px rgba(0,0,0,.06);
  padding: 3rem 2.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  animation: fadeSlideUp 0.5s ease both;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Icons ───────────────────────────────────────── */
.result-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}
.success-icon {
  background: linear-gradient(135deg, var(--color-primary-50), var(--color-primary-100));
  color: var(--color-primary);
}
.pending-icon {
  background: linear-gradient(135deg, var(--color-secondary-50), var(--color-secondary-100));
  color: var(--color-secondary);
}
.failed-icon {
  background: linear-gradient(135deg, #FEF2F2, #FECACA);
  color: #DC2626;
}

/* ── Confetti ────────────────────────────────────── */
.confetti-burst {
  font-size: 2rem;
  animation: confettiBounce 0.6s ease 0.3s both;
}
@keyframes confettiBounce {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.3); }
  100% { transform: scale(1); opacity: 1; }
}

/* ── Text ────────────────────────────────────────── */
.result-card h1 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0;
}
.success-card h1 { color: var(--color-primary-dark); }
.pending-card h1 { color: var(--color-secondary-dark); }
.failed-card h1  { color: #991B1B; }

.result-desc {
  font-size: 0.9rem;
  color: var(--color-neutral-600);
  line-height: 1.6;
  max-width: 380px;
}

/* ── Details ─────────────────────────────────────── */
.result-details {
  width: 100%;
  background: var(--color-neutral-50);
  border-radius: var(--radius-lg);
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin-top: 0.5rem;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}
.detail-label {
  color: var(--color-neutral-500);
}
.detail-value {
  font-weight: 600;
  color: var(--color-neutral-800);
}
.detail-value.amount {
  font-family: var(--font-heading);
  color: var(--color-primary-dark);
}
code.detail-value {
  font-size: 0.75rem;
  background: var(--color-neutral-100);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-family: var(--mono, monospace);
}

/* ── Actions ─────────────────────────────────────── */
.result-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0.75rem;
}

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 480px) {
  .result-card {
    padding: 2rem 1.5rem;
  }
  .result-card h1 {
    font-size: 1.25rem;
  }
  .result-actions {
    flex-direction: column;
    width: 100%;
  }
  .result-actions .btn {
    width: 100%;
  }
}
</style>
