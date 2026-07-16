<template>
  <AppLayout>
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">Mentions Légales</h1>
        <p class="page-subtitle">Informations juridiques de POWER.NG TECHNOLOGY SARL</p>
      </div>
    </div>

    <section class="section">
      <div class="container legal-layout">
        <div class="legal-grid">
          <!-- Card 1: Identification -->
          <div class="card legal-card">
            <h3 class="card-title">
              <Building :size="20" class="text-primary" />
              Identification de l'Entreprise
            </h3>
            <div class="legal-info-list">
              <div class="info-row">
                <span class="info-label">Raison Sociale</span>
                <span class="info-value">POWER.NG TECHNOLOGY SARL</span>
              </div>
              <div class="info-row">
                <span class="info-label">Nom Commercial / Sigle</span>
                <span class="info-value">PNT SARL</span>
              </div>
              <div class="info-row">
                <span class="info-label">Forme Juridique</span>
                <span class="info-value">SARL Unipersonnelle</span>
              </div>
              <div class="info-row">
                <span class="info-label">Capital Social</span>
                <span class="info-value">1 000 000 FCFA (divisé en 100 parts)</span>
              </div>
              <div class="info-row">
                <span class="info-label">Date de Création</span>
                <span class="info-value">26 Juillet 2021 (Durée : 99 ans)</span>
              </div>
              <div class="info-row">
                <span class="info-label">Gérant / Promoteur</span>
                <span class="info-value">M. NGAMO JEAN CHRISTIN</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Enregistrements & Impôts -->
          <div class="card legal-card">
            <h3 class="card-title">
              <FileText :size="20" class="text-primary" />
              Immatriculation & Fiscalité
            </h3>
            <div class="legal-info-list">
              <div class="info-row">
                <span class="info-label">Numéro RCCM</span>
                <span class="info-value">RC/NGA/2021/B/290 (Ngaoundéré)</span>
              </div>
              <div class="info-row">
                <span class="info-label">NIU (N° Identifiant Unique)</span>
                <span class="info-value">M072116365747U</span>
              </div>
              <div class="info-row">
                <span class="info-label">Régime Fiscal</span>
                <span class="info-value">Régime Simplifié d'Imposition (RSI)</span>
              </div>
              <div class="info-row">
                <span class="info-label">Centre de Rattachement</span>
                <span class="info-value">Centre Divisionnaire des Impôts (CDI) de la VINA</span>
              </div>
              <div class="info-row">
                <span class="info-label">Situation Fiscale</span>
                <span class="info-value text-success">À jour (Attestation de non-redevance disponible)</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Localisation & Contacts -->
          <div class="card legal-card">
            <h3 class="card-title">
              <MapPin :size="20" class="text-primary" />
              Coordonnées & Siège Social
            </h3>
            <div class="legal-info-list">
              <div class="info-row">
                <span class="info-label">Siège Social</span>
                <span class="info-value">Ngaoundéré, Cameroun</span>
              </div>
              <div class="info-row">
                <span class="info-label">Localisation</span>
                <span class="info-value">Bali, Carrefour Mosquée ISSA SANTI</span>
              </div>
              <div class="info-row">
                <span class="info-label">Boîte Postale</span>
                <span class="info-value">B.P. 000, Ngaoundéré</span>
              </div>
              <div class="info-row">
                <span class="info-label">Téléphone 1</span>
                <span class="info-value"><a href="tel:+237691242788">+237 691 242 788</a></span>
              </div>
              <div class="info-row">
                <span class="info-label">Téléphone 2</span>
                <span class="info-value"><a href="tel:+237683798201">+237 683 798 201</a></span>
              </div>
              <div class="info-row">
                <span class="info-label">E-mail</span>
                <span class="info-value"><a href="mailto:PNT@GMAIL.COM">PNT@GMAIL.COM</a></span>
              </div>
            </div>
          </div>

          <!-- Card 4: Coordonnées Bancaires -->
          <div class="card legal-card">
            <h3 class="card-title">
              <CreditCard :size="20" class="text-primary" />
              Coordonnées Bancaires
            </h3>
            <div class="legal-info-list">
              <div class="info-row">
                <span class="info-label">Banque</span>
                <span class="info-value">Afriland First Bank (Agence Ngaoundéré)</span>
              </div>
              <div class="info-row">
                <span class="info-label">Code Banque / Guichet</span>
                <span class="info-value">10005 / 00019</span>
              </div>
              <div class="info-row">
                <span class="info-label">N° de Compte</span>
                <span class="info-value">07158181001</span>
              </div>
              <div class="info-row">
                <span class="info-label">Clé RIB</span>
                <span class="info-value">92</span>
              </div>
              <div class="info-row">
                <span class="info-label">IBAN</span>
                <span class="info-value">CM21 10005 00019 07158181001-92</span>
              </div>
              <div class="info-row">
                <span class="info-label">Code SWIFT / BIC</span>
                <span class="info-value">CCEICMCX</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card object-social-card">
          <h3 class="card-title">
            <Award :size="20" class="text-primary" />
            Activités Principales & Objet Social
          </h3>
          <p class="social-desc">
            POWER.NG TECHNOLOGY SARL est habilitée à opérer dans les secteurs clés suivants en Afrique centrale :
          </p>
          <ul class="activities-list">
            <li><span>✓</span> Marchés publics et prestations de services</li>
            <li><span>✓</span> Travaux en énergie solaire, biomasse, hydraulique et éolienne</li>
            <li><span>✓</span> Installation et maintenance industrielle</li>
            <li><span>✓</span> Travaux d'électronique, d'électrotechnique et d'automatique</li>
            <li><span>✓</span> Froid et climatisation</li>
            <li><span>✓</span> Bâtiment et Travaux Publics (B.T.P.) et Commerce Général</li>
          </ul>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup>
import AppLayout from "@/components/common/AppLayout.vue";
import { Building, FileText, MapPin, CreditCard, Award } from "lucide-vue-next";
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
  color: #fff;
  padding: 3.5rem 0 2.5rem;
}
.page-title {
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 800;
  color: #fff;
  margin: 0.5rem 0;
}
.page-subtitle {
  color: rgba(255, 255, 255, 0.75);
  max-width: 600px;
}

.legal-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.legal-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.legal-card {
  padding: 1.75rem;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-primary-dark);
  margin-bottom: 1.25rem;
  border-bottom: 1px solid var(--color-neutral-100);
  padding-bottom: 0.75rem;
}

.legal-info-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  font-size: 0.875rem;
}

.info-label {
  color: var(--color-neutral-500);
  font-weight: 500;
}

.info-value {
  color: var(--color-neutral-800);
  font-weight: 600;
  text-align: right;
}

.info-value a {
  color: var(--color-primary);
  text-decoration: none;
}
.info-value a:hover {
  text-decoration: underline;
}

.object-social-card {
  padding: 2rem;
}

.social-desc {
  font-size: 0.9rem;
  color: var(--color-neutral-600);
  margin-bottom: 1rem;
}

.activities-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.85rem;
}

.activities-list li {
  font-size: 0.875rem;
  color: var(--color-neutral-700);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.activities-list li span {
  color: var(--color-secondary);
  font-weight: bold;
}

@media (max-width: 768px) {
  .legal-grid {
    grid-template-columns: 1fr;
  }
  .activities-list {
    grid-template-columns: 1fr;
  }
}
</style>
