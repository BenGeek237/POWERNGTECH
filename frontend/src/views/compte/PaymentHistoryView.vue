<template>
  <AppLayout>
    <div class="account-page">
      <div class="container account-layout">
        <AccountSidebar />
        <div class="account-content">
          <div class="content-header">
            <div>
              <h1 class="content-title">Historique des paiements</h1>
              <p class="content-subtitle">Tous vos paiements et transactions</p>
            </div>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="spinner" style="width:2.5rem;height:2.5rem"></div>
            <p>Chargement de vos paiements...</p>
          </div>

          <div v-else-if="payments.length === 0" class="empty-state card">
            <div class="empty-icon-wrap">
              <CreditCard :size="48" stroke-width="1" />
            </div>
            <h3>Aucun paiement pour l'instant</h3>
            <p>Votre historique de paiements apparaîtra ici.</p>
            <RouterLink to="/formations" class="btn btn-primary">
              Voir les formations
              <ArrowRight :size="16" />
            </RouterLink>
          </div>

          <div v-else class="card payments-card">
            <!-- Summary -->
            <div class="payments-summary">
              <div class="summary-item">
                <span class="summary-val">{{ payments.length }}</span>
                <span class="summary-lbl">Transaction{{ payments.length > 1 ? 's' : '' }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-val">{{ formatPrice(totalPaid) }}</span>
                <span class="summary-lbl">FCFA dépensés</span>
              </div>
              <div class="summary-item success">
                <span class="summary-val">{{ successCount }}</span>
                <span class="summary-lbl">Réussie{{ successCount > 1 ? 's' : '' }}</span>
              </div>
            </div>

            <!-- Table -->
            <div class="payments-table">
              <table>
                <thead>
                  <tr>
                    <th>Référence</th>
                    <th>Montant</th>
                    <th>Statut</th>
                    <th>Mode</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in payments" :key="p.id" class="payment-row">
                    <td>
                      <code class="ref-code">{{ p.camerpay_reference || `PAY-${p.id}` }}</code>
                    </td>
                    <td class="amount-cell">{{ formatPrice(p.amount) }} <span class="currency">FCFA</span></td>
                    <td>
                      <span class="badge" :class="statusBadge(p.status)">
                        <component :is="statusIcon(p.status)" :size="12" />
                        {{ statusLabel(p.status) }}
                      </span>
                    </td>
                    <td>
                      <span class="provider-tag">{{ p.provider || "—" }}</span>
                    </td>
                    <td class="date-cell">{{ formatDate(p.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import AccountSidebar from "@/components/compte/AccountSidebar.vue";
import { paiementsApi } from "@/services/api";
import { CreditCard, ArrowRight, CheckCircle, XCircle, Clock, AlertTriangle } from "lucide-vue-next";

const payments = ref([]);
const loading  = ref(true);

const statusLabels   = { INITIATED: "Initialisé", PENDING: "En attente", SUCCESS: "Réussi", FAILED: "Échoué", CANCELLED: "Annulé" };
const statusBadgeMap = { INITIATED: "badge-neutral", PENDING: "badge-warning", SUCCESS: "badge-success", FAILED: "badge-danger", CANCELLED: "badge-neutral" };
const statusIconMap  = { INITIATED: Clock, PENDING: Clock, SUCCESS: CheckCircle, FAILED: XCircle, CANCELLED: AlertTriangle };

function statusLabel(s) { return statusLabels[s] || s; }
function statusBadge(s) { return statusBadgeMap[s] || "badge-neutral"; }
function statusIcon(s)  { return statusIconMap[s] || Clock; }
function formatPrice(p) { return new Intl.NumberFormat("fr-FR").format(p); }
function formatDate(d)  { return new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" }); }

const totalPaid    = computed(() => payments.value.filter(p => p.status === "SUCCESS").reduce((acc, p) => acc + Number(p.amount), 0));
const successCount = computed(() => payments.value.filter(p => p.status === "SUCCESS").length);

onMounted(async () => {
  try {
    const { data } = await paiementsApi.getHistory();
    payments.value = data;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.account-page { padding: 2.5rem 0; min-height: 70vh; background: var(--color-neutral-50); }
.account-layout { display: grid; grid-template-columns: 260px 1fr; gap: 1.75rem; align-items: start; }

.content-header { margin-bottom: 1.25rem; }
.content-title { font-size: 1.4rem; font-weight: 800; color: var(--color-primary-dark); margin: 0; }
.content-subtitle { font-size: .875rem; color: var(--color-neutral-500); margin-top: .2rem; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem; color: var(--color-neutral-500); }
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; text-align: center; padding: 4rem 2rem; }
.empty-icon-wrap {
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--color-primary-50); color: var(--color-primary);
  display: flex; align-items: center; justify-content: center;
}
.empty-state h3 { font-size: 1.1rem; font-weight: 700; color: var(--color-primary-dark); }
.empty-state p  { font-size: .875rem; color: var(--color-neutral-500); }

.payments-card { overflow: hidden; }

/* Summary */
.payments-summary {
  display: flex; border-bottom: 1px solid var(--color-neutral-100); background: var(--color-neutral-50);
}
.summary-item {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  padding: 1.25rem; border-right: 1px solid var(--color-neutral-100); text-align: center;
}
.summary-item:last-child { border-right: none; }
.summary-val {
  font-family: var(--font-heading); font-size: 1.4rem; font-weight: 800;
  color: var(--color-primary); line-height: 1;
}
.summary-item.success .summary-val { color: var(--color-secondary-dark); }
.summary-lbl { font-size: .72rem; color: var(--color-neutral-500); margin-top: .3rem; }

/* Table */
.payments-table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th {
  text-align: left; font-size: .72rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: .05em;
  color: var(--color-neutral-500); padding: .85rem 1.25rem;
  border-bottom: 1px solid var(--color-neutral-100); white-space: nowrap;
}
.payment-row td {
  padding: .85rem 1.25rem; font-size: .875rem; color: var(--color-neutral-700);
  border-bottom: 1px solid var(--color-neutral-50);
}
.payment-row:last-child td { border-bottom: none; }
.payment-row:hover { background: var(--color-neutral-50); }

.ref-code {
  font-size: .72rem; background: var(--color-neutral-100); padding: .2rem .5rem;
  border-radius: 4px; font-family: var(--mono, monospace); color: var(--color-neutral-700);
}
.amount-cell { font-weight: 700; color: var(--color-primary-dark); }
.currency { font-size: .72rem; font-weight: 400; color: var(--color-neutral-500); }
.badge { display: inline-flex; align-items: center; gap: .3rem; }
.provider-tag {
  font-size: .78rem; background: var(--color-primary-50); color: var(--color-primary);
  padding: .2rem .6rem; border-radius: 999px; font-weight: 600;
}
.date-cell { color: var(--color-neutral-500); font-size: .82rem; white-space: nowrap; }

@media (max-width: 768px) {
  .account-layout { grid-template-columns: 1fr; }
  .payments-summary { flex-wrap: wrap; }
}
</style>
