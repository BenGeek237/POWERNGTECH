<template>
  <header class="site-header" :class="{ 'is-scrolled': isScrolled, 'menu-open': menuOpen }">
    <div class="container header-inner">
      <!-- Logo -->
      <RouterLink to="/" class="header-logo" @click="closeMenu">
        <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" />
      </RouterLink>

      <!-- Desktop Navigation -->
      <nav class="header-nav" aria-label="Navigation principale">
        <RouterLink to="/" class="nav-link" exact-active-class="is-active">Accueil</RouterLink>
        <RouterLink to="/formations" class="nav-link" active-class="is-active">Formations</RouterLink>
        <RouterLink to="/formation-personnalisee" class="nav-link" active-class="is-active">Formation personnalisée</RouterLink>
        <RouterLink to="/boutique" class="nav-link" active-class="is-active">Boutique</RouterLink>
        <RouterLink to="/services" class="nav-link" active-class="is-active">Services</RouterLink>
        <RouterLink to="/a-propos" class="nav-link" active-class="is-active">À Propos</RouterLink>
        <RouterLink to="/contact" class="nav-link" active-class="is-active">Contact</RouterLink>
      </nav>

      <!-- CTA Area -->
      <div class="header-cta">
        <template v-if="authStore.isAuthenticated">
          <div class="user-menu" @click.stop="toggleUserMenu" ref="userMenuRef">
                        <button class="user-menu-trigger" :aria-expanded="userMenuOpen">
              <div class="user-avatar">
                <img
                  v-if="authStore.user?.avatar"
                  :src="authStore.user.avatar"
                  :alt="authStore.user.first_name"
                />
                <span v-else>{{ userInitials }}</span>
              </div>
              <span class="user-name">{{ authStore.user?.first_name }}</span>
              <ChevronDown :size="16" class="chevron" :class="{ open: userMenuOpen }" />
            </button>
                      <Transition name="dropdown">
              <div v-if="userMenuOpen" class="user-dropdown">
                <RouterLink to="/compte/profil" class="dropdown-item" @click="closeUserMenu">
                  <User :size="16" stroke-width="1.75" /> Mon profil
                </RouterLink>
                <RouterLink to="/compte/formations" class="dropdown-item" @click="closeUserMenu">
                  <GraduationCap :size="16" stroke-width="1.75" /> Mes formations
                </RouterLink>
                <RouterLink to="/compte/commandes" class="dropdown-item" @click="closeUserMenu">
                  <Package :size="16" stroke-width="1.75" /> Mes commandes
                </RouterLink>
                <RouterLink to="/compte/paiements" class="dropdown-item" @click="closeUserMenu">
                  <CreditCard :size="16" stroke-width="1.75" /> Paiements
                </RouterLink>
                <hr class="dropdown-divider" />
                <button class="dropdown-item danger" @click="handleLogout">
                  <LogOut :size="16" stroke-width="1.75" /> Déconnexion
                </button>
              </div>
            </Transition>
          </div>
        </template>
        <template v-else>
          <RouterLink to="/auth/connexion" class="btn btn-outline btn-sm">Connexion</RouterLink>
          <RouterLink to="/auth/inscription" class="btn btn-primary btn-sm">S'inscrire</RouterLink>
        </template>
      </div>

      <!-- Mobile hamburger -->
      <button
        class="hamburger"
        :class="{ open: menuOpen }"
        @click="toggleMenu"
        aria-label="Menu"
        :aria-expanded="menuOpen"
      >
        <span></span><span></span><span></span>
      </button>
    </div>

    <!-- Mobile Menu -->
    <Transition name="mobile-menu">
      <div v-if="menuOpen" class="mobile-menu">
        <nav class="mobile-nav-list" aria-label="Navigation mobile">
          <RouterLink to="/" class="mobile-nav-link" exact-active-class="is-active" @click="closeMenu">Accueil</RouterLink>
          <RouterLink to="/formations" class="mobile-nav-link" active-class="is-active" @click="closeMenu">Formations</RouterLink>
          <RouterLink to="/formation-personnalisee" class="mobile-nav-link" active-class="is-active" @click="closeMenu">Formation personnalisée</RouterLink>
          <RouterLink to="/boutique" class="mobile-nav-link" active-class="is-active" @click="closeMenu">Boutique</RouterLink>
          <RouterLink to="/services" class="mobile-nav-link" active-class="is-active" @click="closeMenu">Services</RouterLink>
          <RouterLink to="/a-propos" class="mobile-nav-link" active-class="is-active" @click="closeMenu">À Propos</RouterLink>
          <RouterLink to="/contact" class="mobile-nav-link" active-class="is-active" @click="closeMenu">Contact</RouterLink>
        </nav>
        <div class="mobile-auth">
          <template v-if="authStore.isAuthenticated">
            <RouterLink to="/compte/profil" class="btn btn-outline" style="width:100%" @click="closeMenu">
              Mon compte
            </RouterLink>
            <button class="btn btn-primary" style="width:100%" @click="handleLogout">Déconnexion</button>
          </template>
          <template v-else>
            <RouterLink to="/auth/connexion" class="btn btn-outline" style="width:100%" @click="closeMenu">Connexion</RouterLink>
            <RouterLink to="/auth/inscription" class="btn btn-primary" style="width:100%" @click="closeMenu">S'inscrire</RouterLink>
          </template>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { User, GraduationCap, Package, CreditCard, LogOut, ChevronDown } from "lucide-vue-next";

const authStore = useAuthStore();
const uiStore = useUiStore();
const router = useRouter();

const isScrolled = ref(false);
const menuOpen = ref(false);
const userMenuOpen = ref(false);
const userMenuRef = ref(null);

const userInitials = computed(() => {
  const u = authStore.user;
  if (!u) return "U";
  return `${u.first_name?.[0] || ""}${u.last_name?.[0] || ""}`.toUpperCase();
});

function toggleMenu() { menuOpen.value = !menuOpen.value; }
function closeMenu() { menuOpen.value = false; }
function toggleUserMenu() { userMenuOpen.value = !userMenuOpen.value; }
function closeUserMenu() { userMenuOpen.value = false; }

async function handleLogout() {
  closeMenu();
  closeUserMenu();
  await authStore.logout();
  uiStore.showSuccess("Vous avez été déconnecté.");
  router.push("/");
}

function handleScroll() { isScrolled.value = window.scrollY > 20; }

function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    userMenuOpen.value = false;
  }
}

onMounted(() => {
  window.addEventListener("scroll", handleScroll, { passive: true });
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
/* ---- Header base ---- */
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.97);
  border-bottom: 1px solid var(--color-neutral-200);
  transition: box-shadow var(--transition-normal), background var(--transition-normal);
  backdrop-filter: blur(8px);
}
.site-header.is-scrolled {
  box-shadow: var(--shadow-md);
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  gap: 1rem;
}

/* ---- Logo ---- */
.header-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  flex-shrink: 0;
}
.logo-image {
  height: 48px;
  width: auto;
  object-fit: contain;
}

/* ---- Desktop Nav ---- */
.header-nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
  justify-content: center;
}
.nav-link {
  padding: 0.4rem 0.8rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-neutral-700);
  border-radius: var(--radius-sm);
  transition: color var(--transition-fast), background var(--transition-fast);
  white-space: nowrap;
  text-decoration: none;
}
.nav-link:hover,
.nav-link.is-active {
  color: var(--color-primary);
  background: var(--color-primary-50);
}

/* ---- CTA ---- */
.header-cta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* ---- User Menu ---- */
.user-menu { position: relative; }
.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1.5px solid var(--color-neutral-200);
  border-radius: var(--radius-xl);
  padding: 0.3rem 0.8rem 0.3rem 0.3rem;
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}
.user-menu-trigger:hover { border-color: var(--color-primary-500); }
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  overflow: hidden;
  flex-shrink: 0;
}
.user-avatar img { width: 100%; height: 100%; object-fit: cover; }
.user-name { font-size: 0.85rem; font-weight: 500; color: var(--color-neutral-800); }
.chevron { transition: transform var(--transition-fast); }
.chevron.open { transform: rotate(180deg); }

.user-dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 200px;
  background: #fff;
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 0.4rem;
  z-index: 200;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: var(--color-neutral-700);
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: background var(--transition-fast), color var(--transition-fast);
}
.dropdown-item:hover { background: var(--color-neutral-50); color: var(--color-primary); }
.dropdown-item.danger:hover { background: #fef2f2; color: #dc2626; }
.dropdown-divider { border: none; border-top: 1px solid var(--color-neutral-200); margin: 0.3rem 0; }

/* ---- Dropdown transition ---- */
.dropdown-enter-active, .dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0; transform: translateY(-6px);
}

/* ---- Hamburger ---- */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}
.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-neutral-800);
  border-radius: 2px;
  transition: all var(--transition-normal);
  transform-origin: center;
}
.hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.hamburger.open span:nth-child(2) { opacity: 0; }
.hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* ---- Mobile Menu ---- */
.mobile-menu {
  position: absolute;
  top: 70px;
  left: 0;
  right: 0;
  background: #fff;
  border-bottom: 1px solid var(--color-neutral-200);
  box-shadow: var(--shadow-lg);
  padding: 1rem;
}
.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.mobile-nav-link {
  display: block;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--color-neutral-800);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background var(--transition-fast), color var(--transition-fast);
}
.mobile-nav-link:hover { background: var(--color-primary-50); color: var(--color-primary); }
.mobile-auth {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-neutral-200);
}
.mobile-menu-enter-active, .mobile-menu-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.mobile-menu-enter-from, .mobile-menu-leave-to {
  opacity: 0; transform: translateY(-10px);
}

/* ---- Responsive ---- */
@media (max-width: 900px) {
  .header-nav { display: none; }
  .header-cta { display: none; }
  .hamburger { display: flex; }
}
</style>
