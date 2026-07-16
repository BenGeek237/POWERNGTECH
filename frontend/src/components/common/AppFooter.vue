<template>
  <footer class="site-footer">
    <div class="footer-main">
      <div class="container footer-grid">
        <!-- Brand column -->
        <div class="footer-brand">
          <RouterLink to="/" class="footer-logo">
            <img src="@/assets/logo.png" alt="POWER NG TECHNOLOGIE" class="logo-image" />
          </RouterLink>
          <p class="footer-desc">
            Votre partenaire de confiance en énergie solaire, électronique,
            formation professionnelle et solutions technologiques au Cameroun.
          </p>
          <!-- Social -->
          <div class="social-links">
            <a href="#" class="social-link" aria-label="Facebook" target="_blank" rel="noopener">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
            </a>
            <a href="#" class="social-link" aria-label="LinkedIn" target="_blank" rel="noopener">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
            </a>
            <a href="#" class="social-link" aria-label="WhatsApp" target="_blank" rel="noopener">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.464 3.488"/></svg>
            </a>
            <a href="#" class="social-link" aria-label="YouTube" target="_blank" rel="noopener">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M22.54 6.42a2.78 2.78 0 00-1.94-1.96C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 00-1.94 1.96A29 29 0 001 12a29 29 0 00.46 5.58A2.78 2.78 0 003.4 19.54C5.12 20 12 20 12 20s6.88 0 8.6-.46a2.78 2.78 0 001.94-1.96A29 29 0 0023 12a29 29 0 00-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="white"/></svg>
            </a>
          </div>
        </div>

        <!-- Quick links -->
        <div class="footer-col">
          <h4 class="footer-col-title">Liens rapides</h4>
          <ul class="footer-links">
            <li><RouterLink to="/">Accueil</RouterLink></li>
            <li><RouterLink to="/formations">Formations</RouterLink></li>
            <li><RouterLink to="/formation-personnalisee">Formation personnalisée</RouterLink></li>
            <li><RouterLink to="/boutique">Boutique</RouterLink></li>
            <li><RouterLink to="/services">Services</RouterLink></li>
            <li><RouterLink to="/a-propos">À Propos</RouterLink></li>
            <li><RouterLink to="/contact">Contact</RouterLink></li>
          </ul>
        </div>

        <!-- Services -->
        <div class="footer-col">
          <h4 class="footer-col-title">Nos domaines</h4>
          <ul class="footer-links">
            <li><a href="#">Énergie solaire</a></li>
            <li><a href="#">Électronique</a></li>
            <li><a href="#">Électrotechnique</a></li>
            <li><a href="#">Maintenance industrielle</a></li>
            <li><a href="#">Climatisation</a></li>
            <li><a href="#">Formation professionnelle</a></li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="footer-col">
          <h4 class="footer-col-title">Contact</h4>
          <ul class="footer-contact">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 10.8a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>
              <a href="tel:+237691242788">+237 691 242 788</a>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              <a href="mailto:christinoo120@gmail.com">christinoo120@gmail.com</a>
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>Ngaoundéré, Cameroun</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Footer bottom -->
    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p class="copyright">
          © {{ currentYear }} POWER.NG TECHNOLOGY SARL. Tous droits réservés.
        </p>
        <div class="footer-bottom-links">
          <RouterLink to="/mentions-legales" class="footer-legal-link">Mentions Légales</RouterLink>
        </div>
        <p class="footer-tagline">Votre partenaire technologique au Cameroun</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear();
</script>

<style scoped>
.site-footer {
  background: var(--color-primary-dark);
  color: #fff;
  margin-top: auto;
}
.footer-main { padding: 4rem 0 3rem; }
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.2fr;
  gap: 3rem;
}

/* Brand */
.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  margin-bottom: 1rem;
}
.logo-image {
  height: 60px;
  width: auto;
  object-fit: contain;
  background: white; /* Added in case the image needs a white background on dark footer */
  border-radius: 4px;
  padding: 4px;
}
.footer-desc {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.65);
  line-height: 1.7;
  margin-bottom: 1.25rem;
}

/* Social */
.social-links { display: flex; gap: 0.5rem; }
.social-link {
  width: 36px; height: 36px;
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.7);
  transition: background var(--transition-fast), color var(--transition-fast);
  text-decoration: none;
}
.social-link:hover { background: var(--color-secondary); color: #fff; }

/* Columns */
.footer-col-title {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.9);
  margin-bottom: 1.25rem;
}
.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.footer-links a {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.footer-links a:hover { color: #fff; }

/* Contact */
.footer-contact {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}
.footer-contact li {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  font-size: 0.875rem;
  color: rgba(255,255,255,0.6);
}
.footer-contact svg { flex-shrink: 0; margin-top: 2px; opacity: 0.7; }
.footer-contact a {
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.footer-contact a:hover { color: #fff; }

/* Bottom bar */
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding: 1.25rem 0;
}
.footer-bottom-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.copyright { font-size: 0.8rem; color: rgba(255,255,255,0.5); }
.footer-bottom-links { display: flex; gap: 1rem; }
.footer-legal-link { font-size: 0.8rem; color: rgba(255,255,255,0.5); text-decoration: none; transition: color var(--transition-fast); }
.footer-legal-link:hover { color: #fff; }
.footer-tagline { font-size: 0.8rem; color: var(--color-secondary-500); }

@media (max-width: 1024px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .footer-brand { grid-column: 1 / -1; }
}
@media (max-width: 640px) {
  .footer-grid { grid-template-columns: 1fr; }
  .footer-main { padding: 3rem 0 2rem; }
  .footer-bottom-inner { flex-direction: column; text-align: center; }
}
</style>
