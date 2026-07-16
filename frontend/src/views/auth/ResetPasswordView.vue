<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <RouterLink to="/" class="auth-logo"><img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" /></RouterLink>
        <h1 class="auth-title">Nouveau mot de passe</h1>
        <p class="auth-subtitle">Veuillez entrer votre nouveau mot de passe.</p>
      </div>
      
      <div v-if="success" class="alert alert-success">
        ✅ Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter.
      </div>
      
      <div v-else-if="errorMsg" class="alert alert-error">
        ⚠️ {{ errorMsg }}
      </div>
      
      <form v-if="!success" @submit.prevent="handleResetConfirm" class="auth-form" novalidate>
        <div class="form-group">
          <label for="password" class="form-label">Nouveau mot de passe</label>
          <div class="password-input-wrap">
            <input
              id="password"
              v-model="form.new_password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              :class="{ 'is-error': errors.new_password }"
              placeholder="••••••••"
              required
            />
                        <button type="button" class="password-toggle" @click="showPassword = !showPassword">
              <Eye v-if="!showPassword" :size="18" stroke-width="1.75" />
              <EyeOff v-else :size="18" stroke-width="1.75" />
            </button>
          </div>
          <span v-if="errors.new_password" class="form-error">{{ errors.new_password }}</span>
        </div>
        
        <div class="form-group">
          <label for="password_confirm" class="form-label">Confirmer le mot de passe</label>
          <div class="password-input-wrap">
            <input
              id="password_confirm"
              v-model="form.new_password_confirm"
              :type="showPasswordConfirm ? 'text' : 'password'"
              class="form-input"
              :class="{ 'is-error': errors.new_password_confirm }"
              placeholder="••••••••"
              required
            />
                        <button type="button" class="password-toggle" @click="showPasswordConfirm = !showPasswordConfirm">
              <Eye v-if="!showPasswordConfirm" :size="18" stroke-width="1.75" />
              <EyeOff v-else :size="18" stroke-width="1.75" />
            </button>
          </div>
          <span v-if="errors.new_password_confirm" class="form-error">{{ errors.new_password_confirm }}</span>
        </div>

        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? "Réinitialisation..." : "Enregistrer" }}
        </button>
      </form>
      
      <p class="auth-switch">
        <RouterLink to="/auth/connexion">← Retour à la connexion</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authApi } from "@/services/api";
import { Eye, EyeOff } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();

const form = reactive({
  new_password: "",
  new_password_confirm: ""
});

const errors = reactive({
  new_password: "",
  new_password_confirm: ""
});

const loading = ref(false);
const success = ref(false);
const errorMsg = ref("");

const showPassword = ref(false);
const showPasswordConfirm = ref(false);

function validate() {
  errors.new_password = "";
  errors.new_password_confirm = "";
  let valid = true;

  if (!form.new_password || form.new_password.length < 8) {
    errors.new_password = "Le mot de passe doit contenir au moins 8 caractères.";
    valid = false;
  }
  if (form.new_password !== form.new_password_confirm) {
    errors.new_password_confirm = "Les mots de passe ne correspondent pas.";
    valid = false;
  }

  return valid;
}

async function handleResetConfirm() {
  if (!validate()) return;
  
  loading.value = true;
  errorMsg.value = "";
  
  try {
    const data = {
      uidb64: route.params.uid,
      token: route.params.token,
      new_password: form.new_password,
      new_password_confirm: form.new_password_confirm
    };
    
    await authApi.resetPasswordConfirm(data);
    success.value = true;
    
    // Redirect to login after 3 seconds
    setTimeout(() => {
      router.push("/auth/connexion");
    }, 3000);
    
  } catch (err) {
    const errData = err.response?.data;
    if (errData && errData.token) {
      errorMsg.value = errData.token[0] || errData.token;
    } else if (errData && errData.new_password) {
      errors.new_password = errData.new_password[0] || errData.new_password;
    } else {
      errorMsg.value = "Une erreur inattendue s'est produite ou le lien a expiré.";
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
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
.auth-form { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem; }

.password-input-wrap { position: relative; }
.password-input-wrap .form-input { padding-right: 2.75rem; }
.password-toggle {
  position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; font-size: 1rem;
  opacity: 0.6; transition: opacity var(--transition-fast);
}
.password-toggle:hover { opacity: 1; }

.auth-switch { text-align: center; font-size: 0.875rem; margin-top: 1rem; }
.auth-switch a { color: var(--color-primary); font-weight: 600; text-decoration: none; }
</style>
