<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <RouterLink to="/" class="auth-logo">
          <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" />
        </RouterLink>
        <h1 class="auth-title">Créer un compte</h1>
        <p class="auth-subtitle">Rejoignez notre communauté d'apprenants.</p>
      </div>

      <div v-if="authStore.error" class="alert alert-error" style="margin-bottom:1rem">
        <span>⚠️</span><span>{{ authStore.error }}</span>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form" novalidate>
        <div class="form-row">
          <div class="form-group">
            <label for="first_name" class="form-label">Prénom</label>
            <input id="first_name" v-model="form.first_name" type="text" class="form-input" :class="{'is-error':errors.first_name}" placeholder="Votre prénom" required />
            <span v-if="errors.first_name" class="form-error">{{ errors.first_name }}</span>
          </div>
          <div class="form-group">
            <label for="last_name" class="form-label">Nom</label>
            <input id="last_name" v-model="form.last_name" type="text" class="form-input" :class="{'is-error':errors.last_name}" placeholder="Votre nom" required />
            <span v-if="errors.last_name" class="form-error">{{ errors.last_name }}</span>
          </div>
        </div>
        <div class="form-group">
          <label for="reg-email" class="form-label">Adresse email</label>
          <input id="reg-email" v-model="form.email" type="email" class="form-input" :class="{'is-error':errors.email}" placeholder="vous@exemple.com" required />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="phone" class="form-label">Téléphone</label>
            <input id="phone" v-model="form.phone" type="tel" class="form-input" placeholder="+237 6XX..." />
          </div>
          <div class="form-group">
            <label for="city" class="form-label">Ville</label>
            <input id="city" v-model="form.city" type="text" class="form-input" placeholder="Douala..." />
          </div>
        </div>
        <div class="form-group">
          <label for="reg-password" class="form-label">Mot de passe</label>
          <input id="reg-password" v-model="form.password" type="password" class="form-input" :class="{'is-error':errors.password}" placeholder="Min. 8 caractères" required />
          <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
        </div>
        <div class="form-group">
          <label for="reg-password-confirm" class="form-label">Confirmer le mot de passe</label>
          <input id="reg-password-confirm" v-model="form.password_confirm" type="password" class="form-input" :class="{'is-error':errors.password_confirm}" placeholder="Répétez le mot de passe" required />
          <span v-if="errors.password_confirm" class="form-error">{{ errors.password_confirm }}</span>
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="authStore.loading">
          <span v-if="authStore.loading" class="spinner" style="width:18px;height:18px;border-width:2px"></span>
          {{ authStore.loading ? "Création..." : "Créer mon compte" }}
        </button>
      </form>
      <p class="auth-switch">
        Déjà un compte ? <RouterLink to="/auth/connexion">Se connecter</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";

const authStore = useAuthStore();
const uiStore = useUiStore();
const router = useRouter();

const form = reactive({ first_name:"", last_name:"", email:"", phone:"", city:"", password:"", password_confirm:"" });
const errors = reactive({ first_name:"", last_name:"", email:"", password:"", password_confirm:"" });

function validate() {
  Object.keys(errors).forEach(k => errors[k] = "");
  let valid = true;
  if (!form.first_name.trim()) { errors.first_name = "Le prénom est requis."; valid = false; }
  if (!form.last_name.trim())  { errors.last_name  = "Le nom est requis."; valid = false; }
  if (!form.email || !/\S+@\S+\.\S+/.test(form.email)) { errors.email = "Email invalide."; valid = false; }
  if (!form.password || form.password.length < 8) { errors.password = "Minimum 8 caractères."; valid = false; }
  if (form.password !== form.password_confirm) { errors.password_confirm = "Les mots de passe ne correspondent pas."; valid = false; }
  return valid;
}

async function handleRegister() {
  if (!validate()) return;
  const result = await authStore.register(form);
  if (result.success) {
    uiStore.showSuccess("Compte créé avec succès ! Bienvenue !");
    router.push("/");
  }
}
</script>

<style scoped>
/* Shared with LoginView */
.auth-page { min-height:100vh; background:linear-gradient(135deg,var(--color-primary-dark),var(--color-primary)); display:flex; align-items:center; justify-content:center; padding:2rem 1rem; }
.auth-card { background:#fff; border-radius:var(--radius-xl); padding:2.5rem; width:100%; max-width:520px; box-shadow:var(--shadow-xl); }
.auth-header { text-align:center; margin-bottom:1.75rem; }
.auth-logo { display:inline-flex; align-items:center; justify-content:center; margin-bottom:1.5rem; text-decoration:none; }
.logo-image { height:60px; width:auto; object-fit:contain; background:white; border-radius:8px; padding:4px; }
.auth-title { font-size:1.6rem; font-weight:800; color:var(--color-primary-dark); margin-bottom:0.4rem; }
.auth-subtitle { color:var(--color-neutral-600); font-size:0.9rem; }
.auth-form { display:flex; flex-direction:column; gap:1rem; margin-bottom:1.25rem; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.auth-switch { text-align:center; font-size:0.875rem; color:var(--color-neutral-600); }
.auth-switch a { color:var(--color-primary); font-weight:600; text-decoration:none; }
</style>
