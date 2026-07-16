<template>
  <AppLayout>
    <div class="account-page">
      <div class="container account-layout">
        <AccountSidebar />
        <div class="account-content">
          <div class="content-header">
            <div>
              <h1 class="content-title">Mes Commandes</h1>
              <p class="content-subtitle">Suivez vos commandes et leur statut</p>
            </div>
            <RouterLink to="/boutique" class="btn btn-primary btn-sm">
              <ShoppingBag :size="16" />
              Boutique
            </RouterLink>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="spinner" style="width:2.5rem;height:2.5rem"></div>
            <p>Chargement de vos commandes...</p>
          </div>

          <div v-else-if="orders.length === 0" class="empty-state card">
            <div class="empty-icon-wrap">
              <Package :size="48" stroke-width="1" />
            </div>
            <h3>Aucune commande pour l'instant</h3>
            <p>Vous n'avez encore passé aucune commande. Explorez notre boutique !</p>
            <RouterLink to="/boutique" class="btn btn-primary">
              Voir la boutique
              <ArrowRight :size="16" />
            </RouterLink>
          </div>

          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-card card">
              <!-- Order header -->
              <div class="order-header">
                <div class="order-id">
                  <Hash :size="15" stroke-width="2" />
                  Commande {{ order.id }}
                </div>
                <span class="badge" :class="statusBadge(order.status)">{{ statusLabel(order.status) }}</span>
                <span class="order-date">
                  <Calendar :size="13" />
                  {{ formatDate(order.created_at) }}
                </span>
              </div>
              <!-- Items -->
              <div class="order-items">
                <div v-for="item in order.items" :key="item.id" class="order-item">
                  <div class="item-name">{{ item.product_name }}</div>
                  <div class="item-qty">× {{ item.quantity }}</div>
                  <div class="item-price">{{ formatPrice(item.unit_price) }} FCFA</div>
                </div>
              </div>
              <!-- Footer -->
              <div class="order-footer">
                <div class="order-total">
                  <span>Total</span>
                  <strong>{{ formatPrice(order.total_amount) }} FCFA</strong>
                </div>
                <div class="order-status-track">
                  <div
                    v-for="(step, idx) in statusSteps"
                    :key="step.key"
                    class="track-step"
                    :class="{ active: isStepActive(order.status, idx), done: isStepDone(order.status, idx) }"
                  >
                    <component :is="step.icon" :size="14" />
                    <span>{{ step.label }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import AccountSidebar from "@/components/compte/AccountSidebar.vue";
import { boutiqueApi } from "@/services/api";
import { Package, ShoppingBag, ArrowRight, Hash, Calendar, Clock, CreditCard, Truck, CheckCircle, XCircle } from "lucide-vue-next";

const orders  = ref([]);
const loading = ref(true);

const statusLabels   = { PENDING: "En attente", PAID: "Payée", SHIPPED: "Expédiée", DELIVERED: "Livrée", CANCELLED: "Annulée" };
const statusBadgeMap = { PENDING: "badge-warning", PAID: "badge-success", SHIPPED: "badge-primary", DELIVERED: "badge-secondary", CANCELLED: "badge-danger" };
const statusOrder    = ["PENDING", "PAID", "SHIPPED", "DELIVERED"];

const statusSteps = [
  { key: "PENDING",   label: "Reçue",     icon: Clock },
  { key: "PAID",      label: "Payée",     icon: CreditCard },
  { key: "SHIPPED",   label: "Expédiée",  icon: Truck },
  { key: "DELIVERED", label: "Livrée",    icon: CheckCircle },
];

function statusLabel(s) { return statusLabels[s] || s; }
function statusBadge(s) { return statusBadgeMap[s] || "badge-neutral"; }
function formatPrice(p) { return new Intl.NumberFormat("fr-FR").format(p); }
function formatDate(d)  { return new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }); }
function isStepActive(status, idx) { return statusOrder[idx] === status; }
function isStepDone(status, idx)   { return statusOrder.indexOf(status) > idx; }

onMounted(async () => {
  try {
    const { data } = await boutiqueApi.getMyOrders();
    orders.value = data;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.account-page { padding: 2.5rem 0; min-height: 70vh; background: var(--color-neutral-50); }
.account-layout { display: grid; grid-template-columns: 260px 1fr; gap: 1.75rem; align-items: start; }

.content-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem;
}
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
.empty-state p { font-size: .875rem; color: var(--color-neutral-500); max-width: 300px; }

.orders-list { display: flex; flex-direction: column; gap: 1.25rem; }
.order-card { overflow: hidden; }

.order-header {
  display: flex; align-items: center; gap: 1rem; padding: 1rem 1.25rem;
  background: var(--color-neutral-50); border-bottom: 1px solid var(--color-neutral-100);
  flex-wrap: wrap;
}
.order-id {
  display: flex; align-items: center; gap: .35rem;
  font-weight: 700; font-size: .9rem; color: var(--color-primary-dark); flex: 1;
}
.order-date {
  display: flex; align-items: center; gap: .35rem;
  font-size: .78rem; color: var(--color-neutral-500); margin-left: auto;
}

.order-items { padding: .5rem 1.25rem; }
.order-item {
  display: flex; align-items: center; gap: 1rem; padding: .6rem 0;
  font-size: .875rem; border-bottom: 1px solid var(--color-neutral-50);
}
.order-item:last-child { border: none; }
.item-name { flex: 1; color: var(--color-neutral-800); }
.item-qty  { color: var(--color-neutral-500); font-size: .8rem; }
.item-price { font-weight: 600; color: var(--color-primary); white-space: nowrap; }

.order-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: .85rem 1.25rem; border-top: 1px solid var(--color-neutral-100);
  flex-wrap: wrap; gap: 1rem;
}
.order-total { display: flex; align-items: center; gap: .75rem; font-size: .9rem; color: var(--color-neutral-600); }
.order-total strong { font-family: var(--font-heading); font-size: 1rem; color: var(--color-primary-dark); }

/* Status tracker */
.order-status-track { display: flex; gap: .5rem; align-items: center; }
.track-step {
  display: flex; flex-direction: column; align-items: center; gap: .2rem;
  font-size: .62rem; color: var(--color-neutral-400); font-weight: 500;
  position: relative;
}
.track-step::after {
  content: ''; position: absolute; left: 100%; top: 7px;
  width: 12px; height: 1px; background: var(--color-neutral-200);
}
.track-step:last-child::after { display: none; }
.track-step.done   { color: var(--color-secondary); }
.track-step.active { color: var(--color-primary); }

@media (max-width: 768px) {
  .account-layout { grid-template-columns: 1fr; }
  .order-status-track { display: none; }
}
</style>
