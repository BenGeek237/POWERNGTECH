/**
 * POWER NG TECHNOLOGIE — Countries and Phone Codes
 * For internationalization support.
 */

export const africanCountries = [
  { code: "CM", name: "Cameroun", prefix: "+237" },
  { code: "CI", name: "Côte d'Ivoire", prefix: "+225" },
  { code: "SN", name: "Sénégal", prefix: "+221" },
  { code: "GA", name: "Gabon", prefix: "+241" },
  { code: "CG", name: "Congo-Brazzaville", prefix: "+242" },
  { code: "CD", name: "RDC", prefix: "+243" },
  { code: "TD", name: "Tchad", prefix: "+235" },
  { code: "CF", name: "RCA", prefix: "+236" },
  { code: "GQ", name: "Guinée équatoriale", prefix: "+240" },
  { code: "TG", name: "Togo", prefix: "+228" },
  { code: "BJ", name: "Bénin", prefix: "+229" },
  { code: "ML", name: "Mali", prefix: "+223" },
  { code: "BF", name: "Burkina Faso", prefix: "+226" },
  { code: "NE", name: "Niger", prefix: "+227" },
  { code: "GN", name: "Guinée", prefix: "+224" },
];

export const otherCountries = [
  { code: "FR", name: "France", prefix: "+33" },
  { code: "BE", name: "Belgique", prefix: "+32" },
  { code: "CH", name: "Suisse", prefix: "+41" },
  { code: "CA", name: "Canada", prefix: "+1" },
  { code: "US", name: "États-Unis", prefix: "+1" },
  { code: "MA", name: "Maroc", prefix: "+212" },
  { code: "DZ", name: "Algérie", prefix: "+213" },
  { code: "TN", name: "Tunisie", prefix: "+216" },
];

export const allCountries = [...africanCountries, ...otherCountries];

export function getPrefixByCountryCode(code) {
  const country = allCountries.find(c => c.code === code);
  return country ? country.prefix : "";
}
