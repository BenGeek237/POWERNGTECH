/**
 * POWER NG TECHNOLOGIE — Vue Router Configuration
 * All routes with lazy loading and navigation guards.
 */
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) return { el: to.hash, behavior: "smooth" };
    return { top: 0, behavior: "smooth" };
  },
  routes: [
    // ---------------------------------------------------------------------------
    // Public routes
    // ---------------------------------------------------------------------------
    {
      path: "/",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
      meta: { title: "Accueil — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/formations",
      name: "formations",
      component: () => import("@/views/FormationsView.vue"),
      meta: { title: "Formations — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/formations/:slug",
      name: "formation-detail",
      component: () => import("@/views/FormationDetailView.vue"),
      meta: { title: "Détail Formation — POWER NG TECHNOLOGIE" },
    },

    {
      path: "/formation-personnalisee",
      name: "custom-training",
      component: () => import("@/views/CustomTrainingView.vue"),
      meta: { title: "Formation Personnalisée — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/boutique",
      name: "boutique",
      component: () => import("@/views/BoutiqueView.vue"),
      meta: { title: "Boutique — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/boutique/:slug",
      name: "product-detail",
      component: () => import("@/views/ProductDetailView.vue"),
      meta: { title: "Produit — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/services",
      name: "services",
      component: () => import("@/views/ServicesView.vue"),
      meta: { title: "Services — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/a-propos",
      name: "about",
      component: () => import("@/views/AboutView.vue"),
      meta: { title: "À Propos — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/contact",
      name: "contact",
      component: () => import("@/views/ContactView.vue"),
      meta: { title: "Contact — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/mentions-legales",
      name: "mentions-legales",
      component: () => import("@/views/MentionsLegalesView.vue"),
      meta: { title: "Mentions Légales — POWER.NG TECHNOLOGY SARL" },
    },

    // ---------------------------------------------------------------------------
    // Auth routes (guest only)
    // ---------------------------------------------------------------------------
    {
      path: "/auth/connexion",
      name: "login",
      component: () => import("@/views/auth/LoginView.vue"),
      meta: { title: "Connexion — POWER NG TECHNOLOGIE", guestOnly: true },
    },
    {
      path: "/auth/inscription",
      name: "register",
      component: () => import("@/views/auth/RegisterView.vue"),
      meta: { title: "Inscription — POWER NG TECHNOLOGIE", guestOnly: true },
    },
    {
      path: "/auth/mot-de-passe-oublie",
      name: "forgot-password",
      component: () => import("@/views/auth/ForgotPasswordView.vue"),
      meta: { title: "Mot de passe oublié — POWER NG TECHNOLOGIE", guestOnly: true },
    },
    {
      path: "/auth/reinitialisation/:uid/:token",
      name: "reset-password",
      component: () => import("@/views/auth/ResetPasswordView.vue"),
      meta: { title: "Nouveau mot de passe — POWER NG TECHNOLOGIE", guestOnly: true },
    },

    // ---------------------------------------------------------------------------
    // Protected user account routes
    // ---------------------------------------------------------------------------
    {
      path: "/compte",
      meta: { requiresAuth: true },
      children: [
        {
          path: "profil",
          name: "profile",
          component: () => import("@/views/compte/ProfileView.vue"),
          meta: { title: "Mon Profil — POWER NG TECHNOLOGIE" },
        },
        {
          path: "formations",
          name: "my-courses",
          component: () => import("@/views/compte/MyCoursesView.vue"),
          meta: { title: "Mes Formations — POWER NG TECHNOLOGIE" },
        },
        {
          path: "commandes",
          name: "my-orders",
          component: () => import("@/views/compte/MyOrdersView.vue"),
          meta: { title: "Mes Commandes — POWER NG TECHNOLOGIE" },
        },
        {
          path: "paiements",
          name: "payment-history",
          component: () => import("@/views/compte/PaymentHistoryView.vue"),
          meta: { title: "Historique des paiements — POWER NG TECHNOLOGIE" },
        },
      ],
    },

    // ---------------------------------------------------------------------------
    // Payment callback & checkout
    // ---------------------------------------------------------------------------
    {
      path: "/paiement",
      name: "paiement",
      component: () => import("@/views/PaiementView.vue"),
      meta: { requiresAuth: true, title: "Paiement — POWER NG TECHNOLOGIE" },
    },
    {
      path: "/paiement/retour/:reference",
      name: "payment-return",
      component: () => import("@/views/PaymentReturnView.vue"),
      meta: { requiresAuth: true, title: "Confirmation de paiement" },
    },

    // ---------------------------------------------------------------------------
    // 404
    // ---------------------------------------------------------------------------
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/views/NotFoundView.vue"),
      meta: { title: "Page introuvable — POWER NG TECHNOLOGIE" },
    },
  ],
});

// ---------------------------------------------------------------------------
// Global navigation guards
// ---------------------------------------------------------------------------

router.beforeEach(async (to) => {
  // Update page title
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  const authStore = useAuthStore();

  // Restore session on first load
  if (!authStore.user && authStore.accessToken) {
    await authStore.fetchProfile();
  }

  // Redirect authenticated users away from guest-only pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: "home" };
  }

  // Require authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }

  return true;
});

export default router;
