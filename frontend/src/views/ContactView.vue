<template>
  <AppLayout>
    <div class="page-header"><div class="container"><h1 class="page-title">Nous contacter</h1><p class="page-subtitle">Notre équipe est disponible pour répondre à toutes vos questions.</p></div></div>
    <section class="section">
      <div class="container contact-layout">
        <!-- Info -->
        <div class="contact-info">
          <h2 class="info-title">Informations de contact</h2>
          <div class="contact-items">
            <div class="contact-item"><span class="ci-icon"><Phone :size="24" stroke-width="1.5" class="text-primary" /></span><div><strong>Téléphone</strong><p><a href="tel:+237691242788">+237 691 242 788</a></p></div></div>
            <div class="contact-item"><span class="ci-icon"><Mail :size="24" stroke-width="1.5" class="text-primary" /></span><div><strong>Email</strong><p><a href="mailto:christinoo120@gmail.com">christinoo120@gmail.com</a></p></div></div>
            <div class="contact-item"><span class="ci-icon"><MapPin :size="24" stroke-width="1.5" class="text-primary" /></span><div><strong>Adresse</strong><p>Ngaoundéré, Cameroun</p></div></div>
            <div class="contact-item"><span class="ci-icon"><Clock :size="24" stroke-width="1.5" class="text-primary" /></span><div><strong>Horaires</strong><p>Lundi – Samedi : 8h – 18h</p></div></div>
          </div>
          <RouterLink to="/formation-personnalisee" class="btn btn-secondary" style="margin-top:1.5rem">
            Demander une formation personnalisée
          </RouterLink>
        </div>
        <!-- Form -->
        <div class="card contact-form-wrap">
                    <div v-if="success" class="form-success">
            <CheckCircle :size="48" stroke-width="1.5" class="text-success" />
            <h3>Message envoyé !</h3>
            <p>Nous vous répondrons sous 24h.</p>
          </div>
          <form v-else @submit.prevent="handleSubmit" class="contact-form">
            <h3 class="form-title">Envoyer un message</h3>
            <div class="form-row">
              <div class="form-group"><label class="form-label">Nom complet *</label><input v-model="form.nom" type="text" class="form-input" required /></div>
              <div class="form-group"><label class="form-label">Email *</label><input v-model="form.email" type="email" class="form-input" required /></div>
            </div>
            <div class="form-group"><label class="form-label">Sujet *</label><input v-model="form.sujet" type="text" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Message *</label><textarea v-model="form.message" class="form-textarea" rows="5" required></textarea></div>
            <button type="submit" class="btn btn-primary btn-lg" style="width:100%" :disabled="loading">
              {{ loading ? "Envoi..." : "Envoyer le message" }}
            </button>
          </form>
        </div>
      </div>
    </section>
  </AppLayout>
</template>
<script setup>
import { ref, reactive } from "vue";
import AppLayout from "@/components/common/AppLayout.vue";
import { Phone, Mail, MapPin, Clock, CheckCircle } from 'lucide-vue-next';
import { demandesApi } from "@/services/api";
const form = reactive({ nom:"", email:"", sujet:"", message:"" });
const loading = ref(false); const success = ref(false);
async function handleSubmit() {
  loading.value = true;
  try {
    await demandesApi.submitContact(form);
    success.value = true;
  } catch (err) {
    // handled by interceptor if global error, or locally
  } finally {
    loading.value = false;
  }
}
</script>
<style scoped>
.page-header{background:var(--color-primary-dark);color:#fff;padding:3.5rem 0 2.5rem}
.page-title{font-size:clamp(1.75rem,3vw,2.5rem);font-weight:800;color:#fff;margin:.5rem 0}
.page-subtitle{color:rgba(255,255,255,.75);max-width:600px}
.contact-layout{display:grid;grid-template-columns:1fr 1.5fr;gap:3rem;align-items:start}
.info-title{font-size:1.25rem;font-weight:700;color:var(--color-primary-dark);margin-bottom:1.5rem}
.contact-items{display:flex;flex-direction:column;gap:1.25rem}
.contact-item{display:flex;gap:1rem;align-items:flex-start}
.ci-icon{font-size:1.5rem;flex-shrink:0}
.contact-item strong{font-size:.875rem;font-weight:700;color:var(--color-primary-dark);display:block;margin-bottom:.2rem}
.contact-item p,.contact-item a{font-size:.875rem;color:var(--color-neutral-600)}
.contact-form-wrap{padding:2rem}
.form-title{font-size:1.1rem;font-weight:700;color:var(--color-primary-dark);margin-bottom:1.25rem}
.contact-form{display:flex;flex-direction:column;gap:1rem}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.form-success{text-align:center;display:flex;flex-direction:column;align-items:center;gap:1rem;padding:2rem}
.form-success h3{font-size:1.4rem;font-weight:700;color:var(--color-secondary-dark)}
@media(max-width:768px){.contact-layout{grid-template-columns:1fr}.form-row{grid-template-columns:1fr}}
</style>
