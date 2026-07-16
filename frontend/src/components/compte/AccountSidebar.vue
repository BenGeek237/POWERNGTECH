<template>
  <aside class="account-sidebar card">
    <!-- User info -->
    <div class="account-user">
      <div class="account-avatar">{{ userInitials }}</div>
      <div class="user-details">
        <strong>{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</strong>
        <small>{{ authStore.user?.email }}</small>
      </div>
    </div>
    <!-- Navigation -->
    <nav class="account-nav">
      <RouterLink to="/compte/profil" class="account-nav-link" active-class="is-active">
        <UserCircle :size="17" stroke-width="1.75" />
        Mon profil
      </RouterLink>
      <RouterLink to="/compte/formations" class="account-nav-link" active-class="is-active">
        <GraduationCap :size="17" stroke-width="1.75" />
        Mes formations
      </RouterLink>
      <RouterLink to="/compte/commandes" class="account-nav-link" active-class="is-active">
        <Package :size="17" stroke-width="1.75" />
        Mes commandes
      </RouterLink>
      <RouterLink to="/compte/paiements" class="account-nav-link" active-class="is-active">
        <CreditCard :size="17" stroke-width="1.75" />
        Paiements
      </RouterLink>
    </nav>
    <!-- Logout -->
    <div class="sidebar-footer">
      <button class="logout-btn" @click="handleLogout">
        <LogOut :size="16" stroke-width="1.75" />
        Déconnexion
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { UserCircle, GraduationCap, Package, CreditCard, LogOut } from "lucide-vue-next";

const authStore = useAuthStore();
const uiStore   = useUiStore();
const router    = useRouter();

const userInitials = computed(() => {
  const u = authStore.user;
  return u ? `${u.first_name?.[0] || ""}${u.last_name?.[0] || ""}`.toUpperCase() : "U";
});

async function handleLogout() {
  await authStore.logout();
  uiStore.showSuccess("À bientôt !");
  router.push("/auth/connexion");
}
</script>

<style scoped>
.account-sidebar { padding: 1.5rem; }

.account-user {
  display: flex; align-items: center; gap: .85rem;
  margin-bottom: 1.5rem; padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-neutral-100);
}
.account-avatar {
  width: 46px; height: 46px; border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: .9rem; flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(30,58,95,.3);
}
.user-details strong {
  display: block; font-size: .875rem; font-weight: 700;
  color: var(--color-primary-dark); line-height: 1.3;
}
.user-details small { font-size: .72rem; color: var(--color-neutral-500); }

.account-nav { display: flex; flex-direction: column; gap: .2rem; }
.account-nav-link {
  display: flex; align-items: center; gap: .65rem;
  padding: .65rem .85rem; border-radius: var(--radius-md);
  font-size: .875rem; color: var(--color-neutral-700);
  text-decoration: none; font-weight: 500;
  transition: background var(--transition-fast), color var(--transition-fast);
}
.account-nav-link:hover { background: var(--color-neutral-50); color: var(--color-primary); }
.account-nav-link.is-active {
  background: var(--color-primary-50); color: var(--color-primary); font-weight: 600;
}

.sidebar-footer {
  margin-top: 1.25rem; padding-top: 1.25rem;
  border-top: 1px solid var(--color-neutral-100);
}
.logout-btn {
  display: flex; align-items: center; gap: .6rem; width: 100%;
  padding: .6rem .85rem; border-radius: var(--radius-md);
  background: none; border: none; cursor: pointer;
  font-size: .875rem; color: var(--color-neutral-500); font-weight: 500;
  transition: background var(--transition-fast), color var(--transition-fast);
}
.logout-btn:hover { background: #fee2e2; color: #dc2626; }
</style>
