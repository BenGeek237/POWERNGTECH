<template>
  <AppLayout>
    <div class="account-page">
      <div class="container account-layout">
        <AccountSidebar />
        <div class="account-content">
          <!-- Header -->
          <div class="content-header">
            <div>
              <h1 class="content-title">Mon Profil</h1>
              <p class="content-subtitle">Gérez vos informations personnelles</p>
            </div>
          </div>

          <!-- Success alert -->
          <Transition name="fade">
            <div v-if="saved" class="alert alert-success" style="margin-bottom:1.25rem">
              <CheckCircle :size="18" stroke-width="1.75" />
              <span>Profil mis à jour avec succès !</span>
            </div>
          </Transition>

          <!-- Profile form -->
          <div class="card content-card">
            <h3 class="card-section-title">
              <UserCircle :size="20" stroke-width="1.75" class="text-primary" />
              Informations personnelles
            </h3>
            <form @submit.prevent="handleSave" class="profile-form">
              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">Prénom</label>
                  <input v-model="form.first_name" type="text" class="form-input" placeholder="Votre prénom" />
                </div>
                <div class="form-group">
                  <label class="form-label">Nom</label>
                  <input v-model="form.last_name" type="text" class="form-input" placeholder="Votre nom" />
                </div>
                <div class="form-group">
                  <label class="form-label">Email <span class="form-hint">(non modifiable)</span></label>
                  <input :value="authStore.user?.email" type="email" class="form-input" disabled />
                </div>

                <div class="form-group">
                  <label class="form-label">Pays</label>
                  <select v-model="form.country" class="form-select" @change="onCountryChange">
                    <optgroup label="Afrique">
                      <option v-for="c in africanCountries" :key="c.code" :value="c.code">{{ c.name }}</option>
                    </optgroup>
                    <optgroup label="Autres">
                      <option v-for="c in otherCountries" :key="c.code" :value="c.code">{{ c.name }}</option>
                    </optgroup>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">Téléphone</label>
                  <div class="phone-input-wrapper">
                    <span class="phone-prefix">{{ phonePrefix }}</span>
                    <input v-model="rawPhone" type="tel" class="form-input phone-input" placeholder="6XX XXX XXX" />
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">Ville</label>
                  <input v-model="form.city" type="text" class="form-input" placeholder="Votre ville" />
                </div>
              </div>
              <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="authStore.loading">
                  <Save :size="16" v-if="!authStore.loading" />
                  <span v-if="authStore.loading" class="spinner" style="width:16px;height:16px;border-width:2px"></span>
                  {{ authStore.loading ? "Sauvegarde..." : "Sauvegarder les modifications" }}
                </button>
              </div>
            </form>
          </div>

          <!-- Security section -->
          <div class="card content-card" style="margin-top:1.25rem">
            <h3 class="card-section-title">
              <Lock :size="20" stroke-width="1.75" class="text-primary" />
              Sécurité du compte
            </h3>
            <div class="security-info">
              <div class="security-item">
                <div>
                  <strong>Mot de passe</strong>
                  <p>Modifiez votre mot de passe régulièrement pour sécuriser votre compte.</p>
                </div>
                <RouterLink to="/auth/mot-de-passe-oublie" class="btn btn-outline btn-sm">
                  Changer le mot de passe
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import AccountSidebar from "@/components/compte/AccountSidebar.vue";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { CheckCircle, UserCircle, Save, Lock } from "lucide-vue-next";
import { africanCountries, otherCountries, getPrefixByCountryCode } from "@/utils/countries";

const authStore = useAuthStore();
const uiStore   = useUiStore();
const saved     = ref(false);
const form      = reactive({ first_name: "", last_name: "", phone: "", city: "", country: "CM" });

const phonePrefix = ref("+237");
const rawPhone = ref("");

function onCountryChange() {
  phonePrefix.value = getPrefixByCountryCode(form.country);
}

watch([phonePrefix, rawPhone], () => {
  if (rawPhone.value.trim()) {
    form.phone = `${phonePrefix.value} ${rawPhone.value}`.trim();
  } else {
    form.phone = "";
  }
});

onMounted(() => {
  const u = authStore.user;
  if (u) {
    form.first_name = u.first_name || "";
    form.last_name  = u.last_name  || "";
    form.city       = u.city       || "";
    form.country    = u.country    || "CM";
    
    phonePrefix.value = getPrefixByCountryCode(form.country);
    
    if (u.phone) {
      if (u.phone.startsWith(phonePrefix.value)) {
        rawPhone.value = u.phone.substring(phonePrefix.value.length).trim();
      } else {
        // Fallback if prefix does not match
        const parts = u.phone.split(" ");
        if (parts.length > 1 && parts[0].startsWith("+")) {
          phonePrefix.value = parts[0];
          rawPhone.value = parts.slice(1).join(" ");
        } else {
          rawPhone.value = u.phone;
        }
      }
    }
  }
});

async function handleSave() {
  const r = await authStore.updateProfile(form);
  if (r.success) {
    saved.value = true;
    uiStore.showSuccess("Profil mis à jour !");
    setTimeout(() => { saved.value = false; }, 4000);
  }
}
</script>

<style scoped>
.account-page { padding: 2.5rem 0; min-height: 70vh; background: var(--color-neutral-50); }
.account-layout { display: grid; grid-template-columns: 260px 1fr; gap: 1.75rem; align-items: start; }

.account-content {}
.content-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.25rem;
}
.content-title { font-size: 1.4rem; font-weight: 800; color: var(--color-primary-dark); margin: 0; }
.content-subtitle { font-size: .875rem; color: var(--color-neutral-500); margin-top: .2rem; }

.content-card { padding: 1.75rem; }
.card-section-title {
  display: flex; align-items: center; gap: .6rem;
  font-size: 1rem; font-weight: 700; color: var(--color-primary-dark);
  margin-bottom: 1.5rem; padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-neutral-100);
}

.profile-form { display: flex; flex-direction: column; gap: 1rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-hint { font-size: .72rem; color: var(--color-neutral-400); font-weight: 400; }

.form-actions { display: flex; justify-content: flex-end; padding-top: .5rem; }

.security-item {
  display: flex; align-items: center; justify-content: space-between; gap: 2rem;
  padding: 1rem; background: var(--color-neutral-50); border-radius: var(--radius-md);
}
.security-item strong { display: block; font-size: .875rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: .2rem; }
.security-item p { font-size: .8rem; color: var(--color-neutral-600); }

.fade-enter-active, .fade-leave-active { transition: opacity .3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.phone-input-wrapper { display: flex; align-items: center; }
.phone-prefix {
  background: var(--color-neutral-100);
  border: 1px solid var(--color-neutral-300);
  border-right: none;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
  color: var(--color-neutral-700);
  font-size: 0.875rem;
  font-weight: 500;
  height: 42px;
  display: flex;
  align-items: center;
}
.phone-input { border-radius: 0 var(--radius-md) var(--radius-md) 0; }

@media (max-width: 768px) {
  .account-layout { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .security-item { flex-direction: column; align-items: flex-start; }
}
</style>
