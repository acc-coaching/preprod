// Contrôle du site en ligne, exécuté dans Chrome sur la page d'accueil de l'environnement testé.
// Renvoie un rapport JSON : chaque page du sitemap, son indexation, sa canonique,
// les documents téléchargeables et les fichiers propres à l'environnement.
// Paramètre facultatif : window.ACC_ATTENDU = { texte: { "/qualiopi": ["Mis à jour le …"] } }
(async () => {
  const OFFICIEL = "https://acc-coaching.fr";
  const env = location.host.startsWith("preprod.") ? "preprod" : "prod";
  const attendu = (window.ACC_ATTENDU && window.ACC_ATTENDU.texte) || {};
  const echecs = [];
  const lire = async (u) => { const r = await fetch(u, { cache: "no-store", redirect: "follow" }); return { statut: r.status, texte: await r.text() }; };

  const robots = await lire("/robots.txt");
  if (env === "prod" && !/Allow: \//.test(robots.texte)) echecs.push("robots.txt de prod n'autorise pas l'indexation");
  if (env === "preprod" && !/Disallow: \//.test(robots.texte)) echecs.push("robots.txt de préprod n'interdit pas l'indexation");

  const sitemap = await lire("/sitemap.xml");
  const chemins = [...sitemap.texte.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => new URL(m[1]).pathname);
  const pages = {};
  const documents = new Set();
  for (const chemin of chemins) {
    const { statut, texte } = await lire(chemin);
    const doc = new DOMParser().parseFromString(texte, "text/html");
    const noindex = !!doc.querySelector('meta[name="robots"][content*="noindex"]');
    const canonique = doc.querySelector('link[rel="canonical"]')?.getAttribute("href");
    pages[chemin] = { statut, noindex, canonique };
    if (statut !== 200) echecs.push(`${chemin} : statut ${statut}`);
    if (env === "prod" && noindex) echecs.push(`${chemin} : balise noindex en prod`);
    if (env === "preprod" && !noindex) echecs.push(`${chemin} : balise noindex absente en préprod`);
    if (canonique !== OFFICIEL + chemin) echecs.push(`${chemin} : canonique ${canonique}`);
    for (const t of attendu[chemin] || []) if (!doc.body.innerText.includes(t)) echecs.push(`${chemin} : texte attendu absent « ${t} »`);
    doc.querySelectorAll('a[href*="documents/"]').forEach(a => documents.add(new URL(a.getAttribute("href"), location.origin + chemin).pathname));
  }

  const docs = {};
  for (const d of documents) {
    const r = await fetch(d, { method: "HEAD", cache: "no-store" });
    docs[d] = { statut: r.status, type: r.headers.get("content-type"), taille: r.headers.get("content-length") };
    if (r.status !== 200) echecs.push(`${d} : document introuvable (${r.status})`);
  }

  const outils = (await fetch("/_outils/verifier.py", { method: "HEAD", cache: "no-store" })).status;
  if (outils === 200) echecs.push("les outils internes sont exposés en ligne (/_outils)");

  return { env, origine: location.origin, nbPages: chemins.length, echecs, pages, documents: docs };
})();
