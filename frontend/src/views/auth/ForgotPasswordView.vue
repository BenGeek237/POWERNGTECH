<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <RouterLink to="/" class="auth-logo"><img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" /></RouterLink>
        <h1 class="auth-title">Mot de passe oublié</h1>
        <p class="auth-subtitle">Entrez votre email pour recevoir un lien de réinitialisation.</p>
      </div>
            <div v-if="success" class="alert alert-success">
        <CheckCircle :size="18" stroke-width="1.75" />
        <span>Si un compte existe avec cet email, vous recevrez un lien sous peu.</span>
      </div>
      <form v-else @submit.prevent="handleReset" class="auth-form">
        <div class="form-group">
          <label for="reset-email" class="form-label">Adresse email</label>
          <input id="reset-email" v-model="email" type="email" class="form-input" placeholder="vous@exemple.com" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? "Envoi..." : "Envoyer le lien" }}
        </button>
      </form>
      <p class="auth-switch"><RouterLink to="/auth/connexion">← Retour à la connexion</RouterLink></p>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { authApi } from "@/services/api";
import { CheckCircle } from "lucide-vue-next";
const email = ref(""); const loading = ref(false); const success = ref(false);
async function handleReset() {
  loading.value = true;
  try { await authApi.resetPassword(email.value); success.value = true; }
  finally { loading.value = false; }
}
</script>
<style scoped>
.auth-page{min-height:100vh;background:linear-gradient(135deg,var(--color-primary-dark),var(--color-primary));display:flex;align-items:center;justify-content:center;padding:2rem 1rem}
.auth-card{background:#fff;border-radius:var(--radius-xl);padding:2.5rem;width:100%;max-width:440px;box-shadow:var(--shadow-xl)}
.auth-header{text-align:center;margin-bottom:1.75rem}
.auth-logo{display:inline-flex;align-items:center;justify-content:center;margin-bottom:1.5rem;text-decoration:none}
.logo-image{height:60px;width:auto;object-fit:contain;background:white;border-radius:8px;padding:4px}
.auth-title{font-size:1.6rem;font-weight:800;color:var(--color-primary-dark);margin-bottom:.4rem}
.auth-subtitle{color:var(--color-neutral-600);font-size:.9rem}
.auth-form{display:flex;flex-direction:column;gap:1rem;margin-bottom:1.25rem}
.auth-switch{text-align:center;font-size:.875rem}
.auth-switch a{color:var(--color-primary);font-weight:600;text-decoration:none}
</style>
