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
                <label for="cf-tel" class="form-label">Téléphone *</label>
                <input id="cf-tel" v-model="form.telephone" type="tel" class="form-input" :class="{'is-error':errors.telephone}" placeholder="+237 6XX..." />
                <span v-if="errors.telephone" class="form-error">{{ errors.telephone }}</span>
              </div>
              <div class="form-group">
                <label for="cf-email" class="form-label">Email *</label>
                <input id="cf-email" v-model="form.email" type="email" class="form-input" :class="{'is-error':errors.email}" placeholder="vous@exemple.com" />
                <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
              </div>
              <div class="form-group">
                <label for="cf-ville" class="form-label">Ville *</label>
                <input id="cf-ville" v-model="form.ville" type="text" class="form-input" :class="{'is-error':errors.ville}" placeholder="Douala, Yaoundé..." />
                <span v-if="errors.ville" class="form-error">{{ errors.ville }}</span>
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
import { ref, reactive } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import { demandesApi } from "@/services/api";

const loading = ref(false);
const success = ref(false);
const sentName = ref("");
const form = reactive({ nom:"", telephone:"", email:"", ville:"", domaine:"", niveau:"DEBUTANT", message:"" });
const errors = reactive({ nom:"", telephone:"", email:"", ville:"", domaine:"", message:"" });

import { Target, Users, Calendar, Trophy, Phone, CheckCircle } from 'lucide-vue-next';

const infoPoints = [
  { icon:Target, title:"Programme sur mesure", desc:"Formation adaptée à vos objectifs spécifiques et votre rythme d'apprentissage." },
  { icon:Users, title:"Groupe ou individuel", desc:"Que vous soyez seul ou en équipe, nous adaptons le format à vos besoins." },
  { icon:Calendar, title:"Horaires flexibles", desc:"Choisissez les horaires qui correspondent à votre emploi du temps." },
  { icon:Trophy, title:"Résultats garantis", desc:"Nos formations pratiques assurent une montée en compétences réelle et rapide." },
];

function validate() {
  Object.keys(errors).forEach(k => errors[k] = "");
  let v = true;
  if (!form.nom.trim())      { errors.nom = "Requis"; v = false; }
  if (!form.telephone.trim()){ errors.telephone = "Requis"; v = false; }
  if (!form.email || !/\S+@\S+\.\S+/.test(form.email)){ errors.email = "Email invalide"; v = false; }
  if (!form.ville.trim())    { errors.ville = "Requis"; v = false; }
  if (!form.domaine.trim())  { errors.domaine = "Requis"; v = false; }
  if (!form.message.trim())  { errors.message = "Requis"; v = false; }
  return v;
}

async function handleSubmit() {
  if (!validate()) return;
  loading.value = true;
  try {
    await demandesApi.submit(form);
    sentName.value = form.nom;
    success.value = true;
  } finally { loading.value = false; }
}

function resetForm() {
  Object.keys(form).forEach(k => form[k] = k === "niveau" ? "DEBUTANT" : "");
  success.value = false;
}
</script>

<style scoped>
.page-header { background:linear-gradient(135deg,var(--color-primary-dark),var(--color-primary)); color:#fff; padding:3.5rem 0 2.5rem; }
.page-title { font-size:clamp(1.75rem,3vw,2.5rem); font-weight:800; color:#fff; margin:.5rem 0; }
.page-subtitle { color:rgba(255,255,255,.75); max-width:600px; }
.custom-layout { display:grid; grid-template-columns:1fr 1.4fr; gap:3rem; align-items:start; }
.info-title { font-size:1.25rem; font-weight:700; color:var(--color-primary-dark); margin-bottom:1.5rem; }
.info-points { display:flex; flex-direction:column; gap:1.25rem; margin-bottom:2rem; }
.info-point { display:flex; align-items:flex-start; gap:1rem; }
.info-point-icon { font-size:1.5rem; flex-shrink:0; }
.info-point h4 { font-size:.9rem; font-weight:700; margin-bottom:.25rem; color:var(--color-primary-dark); }
.info-point p { font-size:.85rem; color:var(--color-neutral-600); line-height:1.55; }
.info-note { background:var(--color-primary-50); border:1px solid var(--color-primary-100); border-radius:var(--radius-md); padding:1rem 1.25rem; font-size:.875rem; color:var(--color-primary-dark); }
.custom-form-wrap { padding:2rem; }
.form-title { font-size:1.1rem; font-weight:700; color:var(--color-primary-dark); margin-bottom:1.5rem; }
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.custom-form { display:flex; flex-direction:column; gap:1.1rem; }
.form-note { text-align:center; font-size:.78rem; color:var(--color-neutral-500); }
.form-success { text-align:center; padding:2rem; display:flex; flex-direction:column; align-items:center; gap:1rem; }
.form-success h3 { font-size:1.4rem; font-weight:700; color:var(--color-secondary-dark); }
@media (max-width:900px) { .custom-layout{grid-template-columns:1fr} .form-grid{grid-template-columns:1fr} }
</style>
