#!/usr/bin/env python3
"""Tests du site ACC avant publication.

    python3 _outils/verifier.py --env preprod [dossier]
    python3 _outils/verifier.py --env prod    [dossier]

Trois familles de contrôles :
  1. l'environnement : indexation, robots.txt, CNAME, domaine, sitemap ;
  2. le contenu : règles éditoriales de regles.py, liens, documents ;
  3. le rendu : chaque page dans un navigateur, à quatre largeurs d'écran.

Une règle en échec bloque la publication. Un écart admis (ECARTS_ADMIS
dans regles.py, décidé par Christophe) est signalé comme ALERTE sans bloquer.
Sortie : rapport en console et fichier rapport-tests.md dans le dossier testé.
"""
import argparse
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config  # noqa: E402
import regles  # noqa: E402

ECARTS_ADMIS = getattr(regles, "ECARTS_ADMIS", {})
EMOJIS = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


class Rapport:
    def __init__(self, env):
        self.env = env
        self.lignes = []

    def verifier(self, condition, regle, detail_ko, detail_ok=""):
        if condition:
            self.lignes.append(("OK", regle, detail_ok))
            return
        admis = None
        for prefixe, valeur in ECARTS_ADMIS.items():
            raison, envs = (valeur, None) if isinstance(valeur, str) else valeur
            if regle.startswith(prefixe) and (envs is None or self.env in envs):
                admis = raison
                break
        if admis:
            self.lignes.append(("ALERTE", regle, f"{detail_ko} — écart admis : {admis}"))
        else:
            self.lignes.append(("ÉCHEC", regle, detail_ko))

    def compte(self, statut):
        return sum(1 for s, _, _ in self.lignes if s == statut)


def texte_visible(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)


def norm(s):
    return s.replace("’", "'").replace("&#x27;", "'").replace("&#39;", "'").replace("&amp;", "&")


# ----------------------------------------------------------------------
# 1. Environnement
# ----------------------------------------------------------------------
def controles_environnement(r, dossier, env):
    p = config.ENVIRONNEMENTS[env]
    toutes = sorted(dossier.glob("*.html"))

    cname = (dossier / "CNAME").read_text().strip() if (dossier / "CNAME").exists() else None
    r.verifier(cname == p["domaine"], f"Environnement — CNAME = {p['domaine']}", f"CNAME = {cname}")

    robots = (dossier / "robots.txt").read_text() if (dossier / "robots.txt").exists() else None
    r.verifier(robots is not None and robots.strip() == p["robots"].strip(),
               f"Environnement — robots.txt conforme à {env}", f"contenu : {robots!r}")

    avec = [f.name for f in toutes if config.BALISE_NOINDEX in f.read_text(encoding="utf-8")]
    if p["indexable"]:
        r.verifier(not avec, "Environnement — aucune balise noindex en prod",
                   f"{len(avec)} page(s) non indexables : " + ", ".join(avec))
        sales = [f.name for f in toutes if "preprod" in f.read_text(encoding="utf-8").lower()]
        r.verifier(not sales, "Environnement — aucune mention de la préprod en prod", ", ".join(sales))
        r.verifier(not (dossier / "_outils").exists(), "Environnement — outils absents de la prod", "_outils présent")
    else:
        sans = [f.name for f in toutes if f.name not in avec]
        r.verifier(not sans, "Environnement — balise noindex sur chaque page de préprod", "sans balise : " + ", ".join(sans))

    # Domaine officiel unique
    www = [f.name for f in [*toutes, dossier / "sitemap.xml", dossier / "robots.txt"]
           if f.exists() and "www.acc-coaching.fr" in f.read_text(encoding="utf-8")]
    r.verifier(not www, f"Domaine — aucune adresse www (officiel : {config.DOMAINE_OFFICIEL})", "présente dans : " + ", ".join(www))

    for cle, fichier in config.PAGES.items():
        f = dossier / fichier
        if not f.exists():
            continue
        html = f.read_text(encoding="utf-8")
        attendu = config.URL_OFFICIELLE + config.URL[cle]
        can = re.search(r'<link rel="canonical" href="([^"]*)"', html)
        og = re.search(r'<meta property="og:url" content="([^"]*)"', html)
        r.verifier(can and can.group(1) == attendu, f"Domaine — canonique de {cle}", f"{can.group(1) if can else 'absente'} au lieu de {attendu}")
        r.verifier(og and og.group(1) == attendu, f"Domaine — og:url de {cle}", f"{og.group(1) if og else 'absent'} au lieu de {attendu}")

    # Sitemap : toutes les pages, rien que des pages existantes
    try:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text for e in ET.parse(dossier / "sitemap.xml").getroot().findall("s:url/s:loc", ns)]
    except Exception as e:  # noqa: BLE001
        locs = []
        r.verifier(False, "Sitemap — lisible", str(e))
    attendus = {config.URL_OFFICIELLE + u for u in config.URL.values()}
    r.verifier(set(locs) == attendus, "Sitemap — exactement les pages publiques",
               f"manquantes : {sorted(attendus - set(locs))} ; en trop : {sorted(set(locs) - attendus)}")


# ----------------------------------------------------------------------
# 2. Contenu
# ----------------------------------------------------------------------
def controles_contenu(r, dossier, sources):
    for motif, raison in regles.INTERDITS:
        fautes = [c for c, h in sources.items() if re.search(motif, h if "class=" in motif else texte_visible(h))]
        r.verifier(not fautes, f"Vocabulaire — {raison}", "présent sur : " + ", ".join(fautes))

    fautes = [c for c, h in sources.items() if EMOJIS.search(texte_visible(h))]
    r.verifier(not fautes, "Vocabulaire — aucun emoji", "emoji sur : " + ", ".join(fautes))

    for cle in ("accueil", "offres"):
        manquants = [t for t in regles.TEMPS if t not in norm(texte_visible(sources.get(cle, "")))]
        r.verifier(not manquants, f"Contenu — intitulés des quatre temps ({cle})", "manquants : " + ", ".join(manquants))

    for cle, attendu, regle in regles.FAITS:
        page = norm(sources.get(cle, ""))
        r.verifier(norm(attendu) in page, f"Contenu — {regle}", f"« {attendu} » absent de la page {cle}")

    bio = re.search(r'<div class="bio">.*?</div>\s*</div>', sources.get("approche", ""), flags=re.S)
    bio_txt = texte_visible(bio.group(0)) if bio else ""
    r.verifier(bio and "Kahler" not in bio_txt and "OpenMind" not in bio_txt,
               "Contenu — encart « Repères » sans Kahler ni OpenMind", "organisme cité dans l'encart")

    eq = texte_visible(sources.get("equipe", ""))
    pos = [eq.find(x) for x in ("Management et leadership, niveaux", "Intelligence émotionnelle, « de",
                                "Techniques du conseil, niveaux", "Culture du feedback")]
    r.verifier(all(p >= 0 for p in pos) and pos == sorted(pos),
               "Contenu — ordre des formations : management, IE, techniques du conseil, feedback", f"positions {pos}")

    for cle in ("accueil", "offres"):
        visibles = re.sub(r'<span class="sr-only">.*?</span>', " ", sources.get(cle, ""))
        r.verifier(re.search(r">\s*Temps [1-4]\s*<", visibles) is None,
                   f"Contenu — pas de mention « Temps n » visible ({cle})", "mention encore affichée")
    for cle, n in (("prise-de-poste", 1), ("leadership", 2), ("equipe", 3), ("transition", 4)):
        r.verifier(f"Temps {n} du cycle de vie du dirigeant" in sources.get(cle, ""),
                   f"Contenu — mention de contexte conservée ({cle})", f"« Temps {n} du cycle de vie du dirigeant » absent")

    acc = norm(texte_visible(sources.get("accueil", "")))
    r.verifier("L'alliance du conseil, du coaching et de la formation" in acc, "Contenu — signature inchangée sur l'accueil", "signature modifiée")
    r.verifier(re.search(r"20 ans\s+de conseil en stratégie\b(?! digitale)", acc) is not None,
               "Contenu — bandeau chiffré de l'accueil inchangé", "bandeau modifié")

    secteurs = [norm(s) for s in re.findall(r'<div class="secteur"><h3>(.*?)</h3>', sources.get("references", ""))]
    r.verifier(secteurs == regles.SECTEURS, "Contenu — références : ordre des six secteurs", f"ordre trouvé : {secteurs}")

    off = sources.get("offres", "")
    col = re.search(r'<div class="catalogue">(.*?)<section class="cat-form"', off, flags=re.S)
    r.verifier(col and "Débriefing psychométrique" not in col.group(1), "Contenu — catalogue : débriefing psychométrique hors des colonnes", "présent dans les colonnes")
    r.verifier(col and "Formation " not in texte_visible(col.group(1)), "Contenu — catalogue : aucune formation dans les colonnes", "formation dans une colonne")
    band = re.search(r'<section class="cat-form".*?</section>', off, flags=re.S)
    nb = len(re.findall(r'class="cat-nom"', band.group(0))) if band else 0
    r.verifier(nb == 4, "Contenu — catalogue : bandeau Formations avec 4 programmes", f"{nb} programmes")


def controles_liens(r, dossier, sources):
    U = config.URL
    for cle, html in sources.items():
        ids = set(re.findall(r'id="([^"]+)"', html))
        orph = sorted({a for a in re.findall(r'href="#([^"]+)"', html) if a not in ids})
        r.verifier(not orph, f"Liens — ancres internes valides ({cle})", "cibles absentes : " + ", ".join(orph))

        # liens internes vers des pages existantes
        internes = set(re.findall(r'href="(/[^"#?]*)', html))
        connus = set(U.values())
        inconnus = sorted(i for i in internes if i not in connus)
        r.verifier(not inconnus, f"Liens — liens internes vers des pages existantes ({cle})", "inconnus : " + ", ".join(inconnus))

        nav = re.search(r'<nav class="nav".*?</nav>', html, flags=re.S)
        nav = nav.group(0) if nav else ""
        attendus = {"L'approche": U["approche"], "Offres": U["offres"], "Références": U["references"], "Contact": U["contact"]}
        err = [lib for lib, u in attendus.items()
               if not (m := re.search(r'<a href="([^"]*)"[^>]*>' + re.escape(lib) + "</a>", nav)) or m.group(1) != u]
        r.verifier(not err, f"Liens — menu principal ({cle})", "à corriger : " + ", ".join(err))

        logo = re.search(r'<a class="logo" href="([^"]*)"', html)
        att = "#haut-page" if cle == "accueil" else "/"
        r.verifier(logo and logo.group(1) == att, f"Liens — logo ({cle})", f"cible {logo.group(1) if logo else 'absente'}")

        pied = re.search(r"<footer.*?</footer>", html, flags=re.S)
        pied = pied.group(0) if pied else ""
        manq = [n for n, u in (("LinkedIn", regles.LINKEDIN), ("Contact", U["contact"]), ("DRH", U["drh"]), ("CGU", U["cgu"]))
                if f'href="{u}"' not in pied]
        r.verifier(not manq, f"Liens — pied de page complet ({cle})", "manque : " + ", ".join(manq))

        vides = [texte_visible(m.group(1)).strip()[:40] for m in re.finditer(r'<a[^>]*href="#"[^>]*>(.*?)</a>', html, flags=re.S)]
        r.verifier(not vides, f"Liens — aucun lien vide ({cle})", "liens vides : " + " | ".join(vides))

        rdv = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>\s*(?:Prendre rendez-vous|Rendez-vous)\s*</a>', html)
        r.verifier(all(u == regles.CALENDLY for u in rdv), f"Liens — « Prendre rendez-vous » vers Calendly ({cle})", "bouton mal ciblé")

        nus = len(re.findall(r"\+33 6 24 39 25 27", texte_visible(html)))
        lies = len(re.findall(r'href="' + re.escape(regles.TEL) + '"', html))
        r.verifier(nus == lies, f"Liens — numéro de téléphone cliquable ({cle})", f"{nus} mention(s), {lies} lien(s) d'appel")

        band = re.search(r'<div class="appel-actions">(.*?)</div>', html, flags=re.S)
        if band:
            libs = [texte_visible(x).strip() for x in re.findall(r"<a[^>]*>(.*?)</a>", band.group(1), flags=re.S)]
            cib = re.findall(r'href="([^"]*)"', band.group(1))
            ok = libs[:3] == ["Préciser votre besoin en 3 minutes", "Prendre rendez-vous", "Appeler le +33 6 24 39 25 27"] \
                and cib[:3] == [regles.TALLY, regles.CALENDLY, regles.TEL]
            r.verifier(ok, f"Liens — bandeau Préciser, Rendez-vous, Appeler ({cle})", f"trouvé : {libs} → {cib}")

        # Documents téléchargeables : chaque lien pointe vers un fichier présent
        docs = sorted(set(re.findall(r'href="/?(documents/[^"]+)"', html)))
        absents = [d for d in docs if not (dossier / d).exists()]
        if docs:
            r.verifier(not absents, f"Documents — fichiers présents ({cle})", f"{len(absents)} absent(s) : " + ", ".join(p.split('/')[-1] for p in absents))

    acc = sources.get("accueil", "")
    for titre, cible in (("Vous êtes dirigeant", U["offres"]), ("Vous êtes DRH", U["drh"])):
        m = re.search(titre + r'</h3>.*?<a href="([^"]*)"', acc, flags=re.S)
        r.verifier(m and m.group(1) == cible, f"Liens — carte « {titre} »", f"cible : {m.group(1) if m else 'absente'}")
    r.verifier(regles.TALLY in sources.get("contact", ""), "Liens — questionnaire Tally sur la page Contact", "lien absent")


def controles_documents(r, dossier):
    import subprocess
    docs = dossier / "documents"
    attendus = getattr(regles, "DOCUMENTS", {})
    for nom in attendus:
        r.verifier((docs / nom).exists(), f"Documents — {nom} déposé", "absent du dossier documents/")
    for pdf in sorted(docs.glob("*.pdf")):
        r.verifier(pdf.name in attendus, f"Documents — {pdf.name} référencé dans regles.py", "fichier inconnu des règles")
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        auteur = next((l.split(":", 1)[1].strip() for l in info.splitlines() if l.startswith("Author:")), "")
        r.verifier(auteur in regles.AUTEURS_ADMIS, f"Documents — métadonnées sans nom de tiers ({pdf.name})", f"auteur : {auteur}")
        texte = subprocess.run(["pdftotext", "-q", str(pdf), "-"], capture_output=True, text=True).stdout
        for nom, attendu, intitule in getattr(regles, "FAITS_DOCUMENTS", []):
            if nom == pdf.name:
                r.verifier(attendu in re.sub(r"\s+", " ", texte), f"Documents — {intitule}", f"« {attendu} » absent de {pdf.name}")
        for motif, cibles, raison in getattr(regles, "INTERDITS_DOCUMENTS", []):
            if cibles and pdf.name not in cibles:
                continue
            trouves = sorted({m.group(0) for m in re.finditer(motif, texte)})
            r.verifier(not trouves, f"Documents — vocabulaire : {raison} ({pdf.name})", "trouvé : " + ", ".join(trouves))


# ----------------------------------------------------------------------
# 3. Rendu
# ----------------------------------------------------------------------
def controles_rendu(r, dossier, sources):
    from playwright.sync_api import sync_playwright
    import functools
    import http.server
    import threading

    # Petit serveur local : les pages sont testées comme sur GitHub Pages (chemins absolus /assets/...)
    class Silencieux(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    gestion = functools.partial(Silencieux, directory=str(dossier))
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), gestion)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{serveur.server_address[1]}/"

    def url(fichier):
        return base + fichier

    fichiers = {**config.PAGES, "404": "404.html"}
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for cle, fichier in fichiers.items():
            if not (dossier / fichier).exists():
                continue
            for largeur in regles.LARGEURS:
                page = nav.new_page(viewport={"width": largeur, "height": 900})
                erreurs = []
                page.on("response", lambda rep, e=erreurs: e.append(rep.url) if rep.url.startswith(base) and rep.status >= 400 else None)
                page.on("requestfailed", lambda req, e=erreurs: e.append(req.url) if req.url.startswith(base) else None)
                page.goto(url(fichier))
                page.wait_for_timeout(250)
                ecart = page.evaluate("document.documentElement.scrollWidth") - largeur
                r.verifier(ecart <= 0, f"Rendu — pas de défilement horizontal ({cle}, {largeur} px)", f"débordement de {ecart} px")
                if largeur >= 760:
                    tabs = page.evaluate("() => [...document.querySelectorAll('.tableau')].filter(e => e.scrollWidth - e.clientWidth > 1).map(e => e.getAttribute('aria-label'))")
                    r.verifier(not tabs, f"Rendu — tableaux lisibles ({cle}, {largeur} px)", "à faire défiler : " + ", ".join(tabs or []))
                if largeur == 1440:
                    r.verifier(not erreurs, f"Rendu — images, polices et styles chargés ({cle})", "introuvables : " + ", ".join(e.split('/')[-1] for e in erreurs))
                    s = page.evaluate("""() => { const h = [...document.querySelectorAll('h1,h2,h3,h4')].map(e => +e.tagName[1]);
                        let saut = null; for (let i = 1; i < h.length; i++) if (h[i] - h[i-1] > 1) saut = [h[i-1], h[i]];
                        const l = {}; [...document.querySelectorAll('a')].forEach(a => { const x = (a.getAttribute('aria-label') || a.innerText).trim().toLowerCase(); const u = a.getAttribute('href'); if (!x) return; l[x] = l[x] || new Set(); l[x].add(u); });
                        const imgs = [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src'));
                        return { h1: document.querySelectorAll('h1').length, saut, lang: document.documentElement.lang, imgs,
                                 ambigus: Object.entries(l).filter(([x, s]) => s.size > 1).map(([x]) => x) }; }""")
                    r.verifier(s["h1"] == 1, f"Rendu — un seul titre de niveau 1 ({cle})", f"{s['h1']} titres h1")
                    r.verifier(s["saut"] is None, f"Rendu — hiérarchie des titres sans saut ({cle})", f"saut {s['saut']}")
                    r.verifier(s["lang"] == "fr", f"Rendu — langue déclarée en français ({cle})", f"lang={s['lang']}")
                    r.verifier(not s["imgs"], f"Rendu — toutes les images s'affichent ({cle})", ", ".join(s["imgs"]))
                    if cle != "404":
                        r.verifier(not s["ambigus"], f"Rendu — libellés de liens non ambigus ({cle})", "répétés : " + ", ".join(s["ambigus"]))
                        ratio = page.evaluate("() => { const i = document.querySelector('img.logo-q'); if (!i) return null; const b = i.getBoundingClientRect(); return b.width / b.height; }")
                        r.verifier(ratio is not None and abs(ratio - 353 / 200) < 0.25, f"Rendu — logo Qualiopi non déformé ({cle})", f"rapport {ratio}")
                        nb = page.evaluate("document.querySelectorAll('footer .badges img').length")
                        r.verifier(nb == 3, f"Rendu — trois badges au pied de page ({cle})", f"{nb} badge(s)")
                page.close()

        if "approche" in sources and "accueil" in sources:
            for largeur, bio_att, rond_att in ((1440, (240, 300), (300, 300)), (390, (220, 275), (260, 260))):
                page = nav.new_page(viewport={"width": largeur, "height": 900})
                page.goto(url(config.PAGES["approche"])); page.wait_for_timeout(250)
                d = page.evaluate("() => { const b = document.querySelector('.bio img').getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; }")
                r.verifier(tuple(d) == bio_att, f"Rendu — photo de l'encart biographique ({largeur} px)", f"{d} au lieu de {bio_att}")
                page.goto(url(config.PAGES["accueil"])); page.wait_for_timeout(250)
                d = page.evaluate("() => { const b = document.querySelector('.portrait img').getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; }")
                r.verifier(tuple(d) == rond_att, f"Rendu — photo ronde de l'accueil ({largeur} px)", f"{d} au lieu de {rond_att}")
                page.close()

            page = nav.new_page(viewport={"width": 1440, "height": 900})
            page.goto(url(config.PAGES["accueil"])); page.wait_for_timeout(250)
            page.evaluate("window.scrollTo(0, 2500)"); page.wait_for_timeout(150)
            page.click("a.logo"); page.wait_for_timeout(1000)
            r.verifier(page.evaluate("window.scrollY") == 0, "Rendu — logo de l'accueil : retour en haut", "la page ne remonte pas")
            h = page.evaluate("() => [...document.querySelectorAll('.temoignage')].map(e => Math.round(e.getBoundingClientRect().height))")
            r.verifier(len(set(h)) == 1, "Rendu — témoignages de même hauteur", f"hauteurs {h}")
            m = page.evaluate("() => [...document.querySelectorAll('.temoignage blockquote')].map(e => e.innerText.split(/\\s+/).length)")
            r.verifier(m and max(m) - min(m) <= 4, "Rendu — extraits de témoignages équilibrés", f"longueurs {m}")
            page.goto(url(config.PAGES["offres"])); page.wait_for_timeout(250)
            h = page.evaluate("() => [...document.querySelectorAll('.cat-col')].map(e => Math.round(e.getBoundingClientRect().height))")
            r.verifier(len(set(h)) == 1, "Rendu — catalogue : quatre colonnes de même hauteur", f"hauteurs {h}")
            page.close()
        nav.close()
    serveur.shutdown()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=config.ENVIRONNEMENTS, required=True)
    ap.add_argument("--sans-rendu", action="store_true", help="contrôles statiques seulement")
    ap.add_argument("dossier", nargs="?", default=".")
    a = ap.parse_args()
    dossier = pathlib.Path(a.dossier).resolve()

    r = Rapport(a.env)
    sources = {}
    for cle, fichier in config.PAGES.items():
        f = dossier / fichier
        r.verifier(f.exists(), f"Présence — {fichier}", "introuvable")
        if f.exists():
            sources[cle] = f.read_text(encoding="utf-8")

    controles_environnement(r, dossier, a.env)
    controles_contenu(r, dossier, sources)
    controles_liens(r, dossier, sources)
    controles_documents(r, dossier)
    if not a.sans_rendu:
        controles_rendu(r, dossier, sources)

    ok, al, ko = r.compte("OK"), r.compte("ALERTE"), r.compte("ÉCHEC")
    entete = (f"# Rapport de tests du site ACC — {a.env} — {date.today().isoformat()}\n\n"
              f"{len(r.lignes)} contrôles : {ok} conformes, {al} alerte(s), {ko} échec(s).\n\n")
    ordre = {"ÉCHEC": 0, "ALERTE": 1, "OK": 2}
    corps = "| Statut | Règle | Détail |\n| --- | --- | --- |\n" + "".join(
        f"| {s} | {g} | {d} |\n" for s, g, d in sorted(r.lignes, key=lambda x: ordre[x[0]]))
    (dossier / "rapport-tests.md").write_text(entete + corps, encoding="utf-8")
    print(entete.strip())
    for s, g, d in r.lignes:
        if s != "OK":
            print(f"  {s:7} {g} : {d}")
    sys.exit(1 if ko else 0)


if __name__ == "__main__":
    main()
