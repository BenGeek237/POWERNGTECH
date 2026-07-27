<template>
  <AppLayout>
    <div class="page-header">
      <div class="container">
        <p class="section-label">Besoin d'une formation adaptée ?</p>
        <h1 class="page-title">Formation Personnalisée</h1>
        <p class="page-subtitle">
          Nous élaborons des programmes de formation sur mesure selon vos besoins,
          votre niveau et votre secteur d'activité.
        </p>
      </div>
    </div>

    <section class="section">
      <div class="container custom-layout">
        <!-- Info -->
        <div class="custom-info">
          <h2 class="info-title">Pourquoi une formation personnalisée ?</h2>
          <div class="info-points">
            <div v-for="pt in infoPoints" :key="pt.title" class="info-point">
              <span class="info-point-icon"><component :is="pt.icon" :size="24" stroke-width="1.5" /></span>
              <div>
                <h4>{{ pt.title }}</h4>
                <p>{{ pt.desc }}</p>
              </div>
            </div>
          </div>
          <div class="info-note">
            <p><Phone :size="16" stroke-width="2" style="display:inline-block;vertical-align:text-bottom;margin-right:4px;" /> Notre équipe vous contactera dans les <strong>48h</strong> suivant votre demande pour discuter de votre projet.</p>
          </div>
        </div>

        <!-- Form -->
        <div class="custom-form-wrap card">
          <div v-if="success" class="form-success">
            <CheckCircle :size="48" stroke-width="1.5" class="text-success" />
            <h3>Demande envoyée !</h3>
            <p>Merci {{ sentName }}. Notre équipe vous contactera dans les meilleurs délais.</p>
            <button class="btn btn-outline" @click="resetForm">Faire une autre demande</button>
          </div>
          <form v-else @submit.prevent="handleSubmit" class="custom-form" novalidate>
            <h3 class="form-title">Formulaire de demande</h3>
            <div class="form-grid">
              <div class="form-group">
                <label for="cf-nom" class="form-label">Nom complet *</label>
                <input id="cf-nom" v-model="form.nom" type="text" class="form-input" :class="{'is-error':errors.nom}" placeholder="Votre nom" />
                <span v-if="errors.nom" class="form-error">{{ errors.nom }}</span>
              </div>
              <div class="form-group">
                <label for="cf-email" class="form-label">Email *</label>
                <input id="cf-email" v-model="form.email" type="email" class="form-input" :class="{'is-error':errors.email}" placeholder="vous@exemple.com" />
                <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
              </div>
              
              <div class="form-group">
                <label for="country" class="form-label">Pays</label>
                <select id="country" v-model="form.country" class="form-select" @change="onCountryChange">
                  <optgroup label="Afrique">
                    <option v-for="c in africanCountries" :key="c.code" :value="c.code">{{ c.name }}</option>
                  </optgroup>
                  <optgroup label="Autres">
                    <option v-for="c in otherCountries" :key="c.code" :value="c.code">{{ c.name }}</option>
                  </optgroup>
                </select>
              </div>
              
              <div class="form-group">
                <label for="cf-ville" class="form-label">Ville *</label>
                <input id="cf-ville" v-model="form.ville" type="text" class="form-input" :class="{'is-error':errors.ville}" placeholder="Douala, Yaoundé..." />
                <span v-if="errors.ville" class="form-error">{{ errors.ville }}</span>
              </div>

              <div class="form-group">
                <label for="cf-tel" class="form-label">Téléphone *</label>
                <div class="phone-input-wrapper" :class="{'is-error':errors.telephone}">
                  <span class="phone-prefix">{{ phonePrefix }}</span>
                  <input id="cf-tel" v-model="rawPhone" type="tel" class="form-input phone-input" placeholder="6XX XXX XXX" />
                </div>
                <span v-if="errors.telephone" class="form-error">{{ errors.telephone }}</span>
              </div>

            </div>
            <div class="form-group">
              <label for="cf-domaine" class="form-label">Domaine souhaité *</label>
              <input id="cf-domaine" v-model="form.domaine" type="text" class="form-input" :class="{'is-error':errors.domaine}" placeholder="Ex: Installation panneaux solaires, Électrotechnique..." />
              <span v-if="errors.domaine" class="form-error">{{ errors.domaine }}</span>
            </div>
            <div class="form-group">
              <label for="cf-niveau" class="form-label">Niveau actuel</label>
              <select id="cf-niveau" v-model="form.niveau" class="form-select">
                <option value="DEBUTANT">Débutant — Je débute dans ce domaine</option>
                <option value="INTERMEDIAIRE">Intermédiaire — J'ai quelques bases</option>
                <option value="AVANCE">Avancé — Je cherche à me spécialiser</option>
                <option value="PROFESSIONNEL">Professionnel — Formation d'équipe</option>
              </select>
            </div>
            <div class="form-group">
              <label for="cf-message" class="form-label">Message / Précisions *</label>
              <textarea id="cf-message" v-model="form.message" class="form-textarea" :class="{'is-error':errors.message}" placeholder="Décrivez votre projet de formation, vos objectifs, le nombre de participants..." rows="5"></textarea>
              <span v-if="errors.message" class="form-error">{{ errors.message }}</span>
            </div>
            <button type="submit" class="btn btn-primary btn-lg" style="width:100%" :disabled="loading">
              <span v-if="loading" class="spinner" style="width:18px;height:18px;border-width:2px"></span>
              {{ loading ? "Envoi en cours..." : "Envoyer ma demande" }}
            </button>
            <p class="form-note">* Champs obligatoires. Aucun paiement requis.</p>
          </form>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import { demandesApi } from "@/services/api";
import { Target, Users, BookOpen, Phone, CheckCircle } from "lucide-vue-next";
import { africanCountries, otherCountries, getPrefixByCountryCode } from "@/utils/countries";

const infoPoints = [
  { icon: Target, title: "Contenu sur mesure", desc: "Le programme est adapté à vos objectifs spécifiques et à votre niveau." },
  { icon: Users, title: "Formateurs experts", desc: "Des professionnels du terrain vous accompagnent tout au long de la formation." },
  { icon: BookOpen, title: "Pratique avant tout", desc: "Mise en situation réelle avec du matériel professionnel." },
];

const form = reactive({
  nom: "",
  email: "",
  telephone: "",
  ville: "",
  domaine: "",
  niveau: "DEBUTANT",
  message: "",
  country: "CM"
});

const errors = reactive({
  nom: "", email: "", telephone: "", ville: "", domaine: "", message: "",
});

const loading = ref(false);
const success = ref(false);
const sentName = ref("");

const phonePrefix = ref("+237");
const rawPhone = ref("");

function onCountryChange() {
  phonePrefix.value = getPrefixByCountryCode(form.country);
}

watch([phonePrefix, rawPhone], () => {
  if (rawPhone.value.trim()) {
    form.telephone = `${phonePrefix.value} ${rawPhone.value}`.trim();
  } else {
    form.telephone = "";
  }
});

function validate() {
  Object.keys(errors).forEach(k => errors[k] = "");
  let valid = true;
  if (!form.nom.trim()) { errors.nom = "Ce champ est requis"; valid = false; }
  if (!form.email || !/\S+@\S+\.\S+/.test(form.email)) { errors.email = "Email invalide"; valid = false; }
  if (!form.telephone.trim()) { errors.telephone = "Ce champ est requis"; valid = false; }
  if (!form.ville.trim()) { errors.ville = "Ce champ est requis"; valid = false; }
  if (!form.domaine.trim()) { errors.domaine = "Ce champ est requis"; valid = false; }
  if (!form.message.trim()) { errors.message = "Ce champ est requis"; valid = false; }
  return valid;
}

async function handleSubmit() {
  if (!validate()) return;
  loading.value = true;
  try {
    await demandesApi.createDemandeFormation(form);
    sentName.value = form.nom;
    success.value = true;
  } catch (err) {
    // handled by interceptor or local error handling
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  Object.assign(form, { nom: "", email: "", telephone: "", ville: "", domaine: "", niveau: "DEBUTANT", message: "", country: "CM" });
  rawPhone.value = "";
  phonePrefix.value = "+237";
  success.value = false;
  sentName.value = "";
}
</script>

<style scoped>
.page-header { background: var(--color-primary-dark); color: #fff; padding: 4rem 0 3rem; text-align: center; }
.section-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5); margin-bottom: 0.5rem; }
.page-title { font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 800; margin-bottom: 1rem; color: #fff; }
.page-subtitle { color: rgba(255,255,255,0.7); max-width: 600px; margin: 0 auto; line-height: 1.6; }

.custom-layout { display: grid; grid-template-columns: 1fr 1.2fr; gap: 4rem; align-items: start; }

.custom-info {}
.info-title { font-size: 1.5rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: 2rem; }
.info-points { display: flex; flex-direction: column; gap: 1.75rem; }
.info-point { display: flex; gap: 1rem; }
.info-point-icon { display: flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 12px; background: var(--color-primary-50); color: var(--color-primary); flex-shrink: 0; }
.info-point h4 { font-size: 1rem; font-weight: 700; color: var(--color-neutral-900); margin-bottom: 0.3rem; }
.info-point p { font-size: 0.875rem; color: var(--color-neutral-600); line-height: 1.5; }
.info-note { margin-top: 2.5rem; padding: 1.25rem; background: var(--color-secondary-50); border: 1px solid var(--color-secondary-200); border-radius: var(--radius-md); font-size: 0.85rem; color: var(--color-secondary-dark); line-height: 1.5; }

.custom-form-wrap { padding: 2.5rem; background: #fff; }
.form-title { font-size: 1.25rem; font-weight: 700; color: var(--color-primary-dark); margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--color-neutral-100); }
.custom-form { display: flex; flex-direction: column; gap: 1.25rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.form-note { font-size: 0.8rem; color: var(--color-neutral-500); text-align: center; margin-top: 0.5rem; }

.form-success { text-align: center; padding: 3rem 0; }
.form-success h3 { font-size: 1.5rem; font-weight: 700; color: var(--color-primary-dark); margin: 1rem 0 0.5rem; }
.form-success p { font-size: 0.9rem; color: var(--color-neutral-600); margin-bottom: 2rem; }

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
.phone-input-wrapper.is-error .phone-prefix { border-color: var(--color-error); }
.phone-input-wrapper.is-error .phone-input { border-color: var(--color-error); }

@media (max-width: 900px) {
  .custom-layout { grid-template-columns: 1fr; gap: 3rem; }
}
@media (max-width: 640px) {
  .form-grid { grid-template-columns: 1fr; }
  .custom-form-wrap { padding: 1.5rem; }
}
</style>
