<template>
  <div class="auth-page">
    <!-- Background decoration -->
    <div class="auth-bg">
      <div class="auth-orb auth-orb-1"></div>
      <div class="auth-orb auth-orb-2"></div>
      <div class="auth-grid-pattern"></div>
    </div>

    <!-- Left panel (branding) - Desktop only -->
    <div class="auth-branding">
      <div class="branding-content">
        <RouterLink to="/" class="brand-logo">
          <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="brand-logo-image" />
        </RouterLink>
        <h2 class="brand-tagline">
          Votre partenaire en <span class="brand-accent">énergie &amp; technologie</span>
        </h2>
        <p class="brand-desc">
          Accédez à vos formations, suivez vos commandes et gérez votre parcours professionnel.
        </p>
        <div class="brand-features">
          <div class="brand-feature" v-for="f in features" :key="f.text">
            <component :is="f.icon" :size="18" />
            <span>{{ f.text }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right panel (form) -->
    <div class="auth-form-panel">
      <div class="auth-card">
        <!-- Mobile logo -->
        <RouterLink to="/" class="auth-mobile-logo">
          <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="mobile-logo-img" />
        </RouterLink>

        <!-- Header -->
        <div class="auth-header">
          <h1 class="auth-title">Connexion</h1>
          <p class="auth-subtitle">Connectez-vous à votre espace personnel.</p>
        </div>

        <!-- Error -->
        <div v-if="authStore.error" class="alert alert-error">
          <AlertTriangle :size="18" stroke-width="1.75" />
          <span>{{ authStore.error }}</span>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="auth-form" novalidate>
          <div class="form-group">
            <label for="email" class="form-label">Adresse email</label>
            <div class="input-icon-wrap">
              <Mail :size="18" class="input-icon" />
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-input has-icon"
                :class="{ 'is-error': errors.email }"
                placeholder="vous@exemple.com"
                autocomplete="email"
                required
              />
            </div>
            <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <div class="password-label">
              <label for="password" class="form-label">Mot de passe</label>
              <RouterLink to="/auth/mot-de-passe-oublie" class="forgot-link">
                Mot de passe oublié ?
              </RouterLink>
            </div>
            <div class="input-icon-wrap">
              <Lock :size="18" class="input-icon" />
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input has-icon has-toggle"
                :class="{ 'is-error': errors.password }"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword" :aria-label="showPassword ? 'Masquer' : 'Afficher'">
                <Eye v-if="!showPassword" :size="18" stroke-width="1.75" />
                <EyeOff v-else :size="18" stroke-width="1.75" />
              </button>
            </div>
            <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
          </div>

          <button
            type="submit"
            class="auth-submit-btn"
            :disabled="authStore.loading"
          >
            <span v-if="authStore.loading" class="auth-spinner"></span>
            <LogIn v-else :size="18" />
            <span>{{ authStore.loading ? "Connexion..." : "Se connecter" }}</span>
          </button>
        </form>

        <p class="auth-switch">
          Pas encore de compte ?
          <RouterLink to="/auth/inscription">Créer un compte</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { AlertTriangle, Eye, EyeOff, Mail, Lock, LogIn, GraduationCap, ShieldCheck, Headphones } from "lucide-vue-next";

const authStore = useAuthStore();
const uiStore = useUiStore();
const router = useRouter();
const route = useRoute();

const form = reactive({ email: "", password: "" });
const errors = reactive({ email: "", password: "" });
const showPassword = ref(false);

const features = [
  { icon: GraduationCap, text: "Accès à vos formations" },
  { icon: ShieldCheck, text: "Paiement 100% sécurisé" },
  { icon: Headphones, text: "Support dédié" },
];

function validate() {
  errors.email = "";
  errors.password = "";
  let valid = true;
  if (!form.email || !/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = "Veuillez entrer un email valide.";
    valid = false;
  }
  if (!form.password || form.password.length < 6) {
    errors.password = "Le mot de passe est obligatoire.";
    valid = false;
  }
  return valid;
}

async function handleLogin() {
  if (!validate()) return;
  const result = await authStore.login(form.email, form.password);
  if (result.success) {
    uiStore.showSuccess(`Bienvenue, ${authStore.user?.first_name} !`);
    const redirect = route.query.redirect || "/";
    router.push(redirect);
  }
}
</script>

<style scoped>
/* ── Auth Page ───────────────────────────────────── */
.auth-page {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
}

/* ── Background ──────────────────────────────────── */
.auth-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.auth-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}
.auth-orb-1 {
  width: 600px; height: 600px;
  background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);
  top: -15%; left: -10%;
  opacity: 0.12;
}
.auth-orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, var(--color-secondary) 0%, transparent 70%);
  bottom: -10%; right: -5%;
  opacity: 0.08;
}
.auth-grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,.02) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* ── Left Branding Panel ─────────────────────────── */
.auth-branding {
  flex: 1;
  background: linear-gradient(160deg, var(--color-primary-dark) 0%, #0c3b1e 50%, #0f172a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}
.auth-branding::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 40%, rgba(22,163,74,.2) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 80%, rgba(217,119,6,.1) 0%, transparent 50%);
  pointer-events: none;
}
.auth-branding::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}
.branding-content {
  position: relative;
  z-index: 1;
  max-width: 420px;
  color: #fff;
}
.brand-logo {
  display: inline-flex;
  margin-bottom: 2rem;
  text-decoration: none;
}
.brand-logo-image {
  height: 56px;
  width: auto;
  object-fit: contain;
  filter: brightness(1.1);
}
.brand-tagline {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  color: #fff;
  margin-bottom: 1rem;
}
.brand-accent {
  background: linear-gradient(135deg, var(--color-secondary-500) 0%, var(--color-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.brand-desc {
  font-size: 1rem;
  color: rgba(255,255,255,.6);
  line-height: 1.7;
  margin-bottom: 2rem;
}
.brand-features {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}
.brand-feature {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 0.9rem;
  color: rgba(255,255,255,.75);
}
.brand-feature svg {
  color: var(--color-secondary-500);
  flex-shrink: 0;
}

/* ── Right Form Panel ────────────────────────────── */
.auth-form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--color-neutral-50);
  position: relative;
  z-index: 1;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  animation: slideUp 0.5s ease both;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Mobile Logo ─────────────────────────────────── */
.auth-mobile-logo {
  display: none;
  justify-content: center;
  margin-bottom: 2rem;
  text-decoration: none;
}
.mobile-logo-img {
  height: 48px;
  width: auto;
  object-fit: contain;
}

/* ── Header ──────────────────────────────────────── */
.auth-header { margin-bottom: 1.75rem; }
.auth-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--color-primary-dark);
  margin: 0 0 0.3rem;
}
.auth-subtitle {
  color: var(--color-neutral-500);
  font-size: 0.9rem;
}

/* ── Form ────────────────────────────────────────── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-bottom: 1.5rem;
}

.input-icon-wrap {
  position: relative;
}
.input-icon {
  position: absolute;
  left: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-neutral-400);
  pointer-events: none;
  transition: color var(--transition-fast);
}
.has-icon {
  padding-left: 2.75rem !important;
}
.has-toggle {
  padding-right: 2.75rem !important;
}
.input-icon-wrap:focus-within .input-icon {
  color: var(--color-primary);
}

.password-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.forgot-link {
  font-size: 0.78rem;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}
.forgot-link:hover { text-decoration: underline; }

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-neutral-400);
  transition: color var(--transition-fast);
}
.password-toggle:hover { color: var(--color-neutral-700); }

/* ── Submit Button ───────────────────────────────── */
.auth-submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.85rem 2rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, var(--color-primary) 0%, #15803d 100%);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(.22,1,.36,1);
  box-shadow: 0 4px 14px rgba(22,163,74,.2);
  margin-top: 0.5rem;
}
.auth-submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(22,163,74,.3);
}
.auth-submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.auth-spinner {
  width: 18px; height: 18px;
  border: 2.5px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Switch ──────────────────────────────────────── */
.auth-switch {
  text-align: center;
  font-size: 0.875rem;
  color: var(--color-neutral-500);
}
.auth-switch a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
.auth-switch a:hover { text-decoration: underline; }

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 900px) {
  .auth-page { flex-direction: column; }
  .auth-branding { display: none; }
  .auth-form-panel {
    min-height: 100vh;
    background:
      radial-gradient(ellipse at 20% 0%, rgba(22,163,74,.04) 0%, transparent 60%),
      var(--color-neutral-50);
  }
  .auth-mobile-logo { display: flex; }
}

@media (max-width: 480px) {
  .auth-form-panel { padding: 1.25rem; }
  .auth-title { font-size: 1.35rem; }
}
</style>
