<template>
  <div class="auth-page">
    <div class="auth-card">
      <!-- Header -->
      <div class="auth-header">
        <RouterLink to="/" class="auth-logo">
          <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" />
        </RouterLink>
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
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            :class="{ 'is-error': errors.email }"
            placeholder="vous@exemple.com"
            autocomplete="email"
            required
          />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <div class="password-label">
            <label for="password" class="form-label">Mot de passe</label>
            <RouterLink to="/auth/mot-de-passe-oublie" class="forgot-link">
              Mot de passe oublié ?
            </RouterLink>
          </div>
          <div class="password-input-wrap">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
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
          class="btn btn-primary"
          style="width:100%"
          :disabled="authStore.loading"
        >
          <span v-if="authStore.loading" class="spinner" style="width:18px;height:18px;border-width:2px"></span>
          <span>{{ authStore.loading ? "Connexion..." : "Se connecter" }}</span>
        </button>
      </form>

      <p class="auth-switch">
        Pas encore de compte ?
        <RouterLink to="/auth/inscription">Créer un compte</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { AlertTriangle, Eye, EyeOff } from "lucide-vue-next";

const authStore = useAuthStore();
const uiStore = useUiStore();
const router = useRouter();
const route = useRoute();

const form = reactive({ email: "", password: "" });
const errors = reactive({ email: "", password: "" });
const showPassword = ref(false);

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
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}
.auth-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 2.5rem;
  width: 100%;
  max-width: 440px;
  box-shadow: var(--shadow-xl);
}
.auth-header { text-align: center; margin-bottom: 1.75rem; }
.auth-logo {
  display: inline-flex; align-items: center; justify-content: center;
  margin-bottom: 1.5rem; text-decoration: none;
}
.logo-image {
  height: 60px; width: auto; object-fit: contain;
  background: white; border-radius: 8px; padding: 4px;
}
.auth-title {
  font-size: 1.6rem; font-weight: 800;
  color: var(--color-primary-dark); margin-bottom: 0.4rem;
}
.auth-subtitle { color: var(--color-neutral-600); font-size: 0.9rem; }
.auth-form { display: flex; flex-direction: column; gap: 1.1rem; margin-bottom: 1.25rem; }
.password-label { display: flex; justify-content: space-between; align-items: center; }
.forgot-link { font-size: 0.8rem; color: var(--color-primary); text-decoration: none; }
.forgot-link:hover { text-decoration: underline; }
.password-input-wrap { position: relative; }
.password-input-wrap .form-input { padding-right: 2.75rem; }
.password-toggle {
  position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; font-size: 1rem;
  opacity: 0.6; transition: opacity var(--transition-fast);
}
.password-toggle:hover { opacity: 1; }
.auth-switch { text-align: center; font-size: 0.875rem; color: var(--color-neutral-600); }
.auth-switch a { color: var(--color-primary); font-weight: 600; text-decoration: none; }
.auth-switch a:hover { text-decoration: underline; }
</style>
