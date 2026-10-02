#!/usr/bin/env python3
"""
Tests de cohérence du site acc-coaching.fr

Chaque règle traduit une remarque déjà formulée par Christophe pendant la
construction du site. Le script s'exécute avant chaque publication :

    python3 test-coherence-site-acc.py [dossier des pages]

Il produit un rapport en console et un fichier rapport-tests.md.
Une règle en échec bloque la publication tant qu'elle n'est pas corrigée
ou explicitement levée par Christophe.
"""
import re
import sys
import pathlib
from datetime import date

from playwright.sync_api import sync_playwright

DOSSIER = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

# --------------------------------------------------------------------------
# Référentiel : pages, adresses et libellés de référence
# --------------------------------------------------------------------------
PAGES = {
    "accueil": "index.html",
    "offres": "offres.html",
    "drh": "drh.html",
    "approche": "approche.html",
    "prise-de-poste": "prise-de-poste.html",
    "leadership": "leadership.html",
    "equipe": "equipe.html",
    "transition": "transition.html",
    "references": "references.html",
    "contact": "contact.html",
    "mentions": "mentions-legales.html",
    "confidentialite": "confidentialite.html",
    "qualiopi": "qualiopi.html",
    "accessibilite": "accessibilite.html",
}
URL = {
    "accueil": "/",
    "offres": "/offres",
    "approche": "/approche",
    "references": "/references",
    "contact": "/contact",
    "drh": "/drh",
}
CALENDLY = "https://calendly.com/christophe-andreu/30min/"
TALLY = "https://tally.so/r/lbpZMp"
LINKEDIN = "https://www.linkedin.com/in/christopheandreu/"
TEL = "tel:+33624392527"
LARGEURS = [390, 760, 1100, 1440]
TEMPS = ["Réussir sa prise de poste", "Développer son leadership",
         "Faire grandir l'équipe", "Réussir sa transition"]

# Vocabulaire proscrit : chaque entrée rappelle la décision d'origine
INTERDITS = [
    (r"\bRebondir\b", "Le temps 4 s'appelle « Réussir sa transition »"),
    (r"Consulting Skills", "La formation s'appelle « Techniques du conseil »"),
    (r"\blivrables?\b", "Pas d'engagement sur des livrables ; parler de « ce qui en ressort »"),
    (r"[Tt]reize livrables|13 livrables", "Engagement retiré de l'outplacement"),
    (r"\bZoom\b", "Visioconférence sur Google Meet uniquement"),
    (r"Deuxième niveau", "Retiré du bloc de certification PCC"),
    (r"DRH monde", "Témoignage : « rejoindre le COMEX du groupe »"),
    (r"Communication C-level", "Formation retirée du catalogue"),
    (r"[Pp]rogramme récent", "Mention retirée de l'intelligence émotionnelle"),
    (r"jeux d'acteurs", "Formulation retenue : « jeux d'influences »"),
    (r"\bQ\d+[AB]?\.", "Codes internes du formulaire à ne jamais afficher"),
    (r"\((?:[A-J])\)\s*<", "Lettres de l'ancien formulaire à ne jamais afficher"),
    (r"CoachHub|Click&amp;Coach|Click & Coach|EZRA|LHH|\bChance\b", "Marque ACC seule, sans plateformes"),
    (r"\[[^\]\"=]{3,80}\]", "Aucun élément entre crochets restant à compléter"),
    (r"class=\"a-completer\"", "Aucun surlignage « à compléter »"),
]
EMOJIS = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


class Rapport:
    def __init__(self):
        self.lignes = []
        self.echecs = 0

    def ok(self, regle, detail=""):
        self.lignes.append(("OK", regle, detail))

    def ko(self, regle, detail):
        self.echecs += 1
        self.lignes.append(("ÉCHEC", regle, detail))

    def verifier(self, condition, regle, detail_ko, detail_ok=""):
        (self.ok if condition else lambda r, d: self.ko(r, d))(regle, detail_ok if condition else detail_ko)


def texte_visible(html):
    """Texte hors balises, styles, scripts et attributs."""
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)


def main():
    r = Rapport()
    sources = {}
    for cle, fichier in PAGES.items():
        chemin = DOSSIER / fichier
        if not chemin.exists():
            r.ko("Présence des pages", f"{fichier} introuvable")
            continue
        sources[cle] = chemin.read_text(encoding="utf-8")
    r.verifier(len(sources) == len(PAGES), "Présence des pages", "", f"{len(sources)} pages trouvées")

    # ------------------------------------------------------------------
    # 1. Vocabulaire et engagements (tests statiques)
    # ------------------------------------------------------------------
    for motif, raison in INTERDITS:
        fautes = []
        for cle, html in sources.items():
            cible = html if "class=" in motif else texte_visible(html)
            if re.search(motif, cible):
                fautes.append(cle)
        r.verifier(not fautes, f"Vocabulaire — {raison}", "présent sur : " + ", ".join(fautes))

    fautes = [c for c, h in sources.items() if EMOJIS.search(texte_visible(h))]
    r.verifier(not fautes, "Aucun emoji dans les textes", "emoji sur : " + ", ".join(fautes))

    # Les quatre temps, avec leurs intitulés exacts, sur l'accueil et la page Offres
    for cle in ("accueil", "offres"):
        manquants = [t for t in TEMPS if t not in texte_visible(sources.get(cle, "")).replace("’", "'")]
        r.verifier(not manquants, f"Intitulés des quatre temps — {cle}", "manquants : " + ", ".join(manquants))

    # Engagements factuels
    faits = [
        ("transition", "100 % à distance", "Bilan de compétences 100 % à distance"),
        ("transition", "Google Meet", "Bilan sur Google Meet"),
        ("transition", "10 séances de 2 heures", "Outplacement en 10 séances de 2 heures"),
        ("mentions", "à associé unique au capital de 1 000", "Forme juridique conforme au Kbis"),
        ("mentions", "11 92 257 53 92", "Numéro de déclaration d'activité"),
        ("qualiopi", "348711-1", "Numéro du certificat Qualiopi"),
        ("prise-de-poste", "jeux d'influences", "Prise de poste : jeux d'influences"),
        ("prise-de-poste", "mise en mouvement concrète", "Prise de poste : pas d'engagement de résultat"),
        ("approche", "circuler les énergies du changement", "Accroche de l'approche"),
        ("approche", "Assessments 24x7", "Certificateur DISC mentionné"),
        ("equipe", "Management et leadership", "Formation management présente"),
        ("equipe", "Culture du feedback", "Formation feedback présente"),
        ("approche", "Ingénieur de formation (EPITA)", "Encart biographique : ingénieur EPITA"),
        ("approche", "conseil en stratégie digitale et IT", "Encart biographique : stratégie digitale et IT"),
        ("approche", "business, digitale, agile et RH", "Parcours : transformations business, digitale, agile et RH"),
        ("approche", "le Ministère de la Défense", "Parcours : Ministère de la Défense cité"),
        ("accueil", "Une culture tech", "Pourquoi ACC : quatrième raison « Une culture tech »"),
        ("accueil", "Transformer un départ en repositionnement stratégique", "Temps 4 : description orientée outplacement"),
        ("offres", "Transformer un départ en repositionnement stratégique", "Temps 4 : description orientée outplacement (offres)"),
        ("leadership", "dirigeants de la tech (CTO, DSI, CDO)", "Leadership : dirigeants de la tech"),
        ("drh", "confronté à l'arrivée de l'IA", "DRH : comité exécutif confronté à l'IA"),
        ("drh", "vos dirigeants, vos managers et vos talents", "DRH : titre ouvert aux trois populations"),
        ("drh", "Trois populations, une même exigence", "DRH : bloc des trois populations"),
        ("confidentialite", "Calendly, synchronisé avec mon agenda Google", "Confidentialité : réservation via Calendly"),
        ("confidentialite", "Tally, Calendly, Google et Cloudflare", "Confidentialité : Calendly parmi les sous-traitants"),
        ("drh", "Managers et managers de managers", "DRH : libellé de la ligne managers"),
    ]
    for cle, attendu, regle in faits:
        present = attendu.replace("'", "’") in sources.get(cle, "") or attendu in sources.get(cle, "")
        r.verifier(present, regle, f"« {attendu} » absent de la page {cle}")

    # Encart biographique : sans noms d'organismes (Kahler, OpenMind)
    bio = re.search(r'<div class="bio">.*?</div>\s*</div>', sources.get("approche", ""), flags=re.S)
    bio_txt = texte_visible(bio.group(0)) if bio else ""
    r.verifier(bio and "Kahler" not in bio_txt and "OpenMind" not in bio_txt,
               "Encart « Repères » sans Kahler ni OpenMind", "organisme cité dans l'encart")

    # Ordre des formations
    eq = texte_visible(sources.get("equipe", ""))
    positions = [eq.find(x) for x in ("Management et leadership, niveaux", "Intelligence émotionnelle, « de",
                                      "Techniques du conseil, niveaux", "Culture du feedback")]
    r.verifier(all(p >= 0 for p in positions) and positions == sorted(positions),
               "Ordre des formations : management, IE, techniques du conseil, feedback", f"positions {positions}")

    # Frise et catalogue sans mention visible « Temps n » ; pages d'offres avec la mention de contexte
    for cle in ("accueil", "offres"):
        visibles = re.sub(r'<span class="sr-only">.*?</span>', " ", sources.get(cle, ""))
        r.verifier(re.search(r">\s*Temps [1-4]\s*<", visibles) is None,
                   f"Pas de mention « Temps n » visible — {cle}", "mention encore affichée")
    for cle, n in (("prise-de-poste", 1), ("leadership", 2), ("equipe", 3), ("transition", 4)):
        r.verifier(f"Temps {n} du cycle de vie du dirigeant" in sources.get(cle, ""),
                   f"Mention de contexte conservée — {cle}", f"« Temps {n} du cycle de vie du dirigeant » absent")

    # Accueil : bandeau chiffré et signature inchangés
    acc_txt = texte_visible(sources.get("accueil", ""))
    r.verifier("L'alliance du conseil, du coaching et de la formation" in acc_txt.replace("’", "'"),
               "Signature inchangée sur l'accueil", "signature modifiée")
    r.verifier(re.search(r"20 ans\s+de conseil en stratégie\b(?! digitale)", acc_txt) is not None,
               "Bandeau chiffré de l'accueil inchangé", "bandeau modifié")

    # Références : ordre des secteurs
    secteurs = re.findall(r'<div class="secteur"><h3>(.*?)</h3>', sources.get("references", ""))
    attendu = ["Banque, assurance, investissement", "Conseil et cabinets d&#x27;avocats", "Tech, digital, télécoms",
               "Luxe, consommation, distribution", "Énergie, industrie, construction", "Services, santé, éducation"]
    secteurs = [s.replace("&#x27;", "'").replace("’", "'") for s in secteurs]
    attendu = [s.replace("&#x27;", "'") for s in attendu]
    r.verifier(secteurs == attendu, "Références : ordre des six secteurs", f"ordre trouvé : {secteurs}")

    # Catalogue : pas de débriefing psychométrique, formations dans le bandeau transverse
    off = sources.get("offres", "")
    colonnes = re.search(r'<div class="catalogue">(.*?)<section class="cat-form"', off, flags=re.S)
    r.verifier(colonnes and "Débriefing psychométrique" not in colonnes.group(1),
               "Catalogue : débriefing psychométrique hors des colonnes", "présent dans les colonnes")
    r.verifier(colonnes and "Formation " not in texte_visible(colonnes.group(1)),
               "Catalogue : aucune formation dans les colonnes des temps", "formation dans une colonne")
    bandeau = re.search(r'<section class="cat-form".*?</section>', off, flags=re.S)
    nb_form = len(re.findall(r'class="cat-nom"', bandeau.group(0))) if bandeau else 0
    r.verifier(nb_form == 4, "Catalogue : bandeau Formations avec 4 programmes", f"{nb_form} programmes")

    # ------------------------------------------------------------------
    # 2. Liens (tests statiques)
    # ------------------------------------------------------------------
    for cle, html in sources.items():
        # ancres internes : la cible doit exister sur la page
        ids = set(re.findall(r'id="([^"]+)"', html))
        orphelines = sorted({a for a in re.findall(r'href="#([^"]+)"', html) if a not in ids})
        r.verifier(not orphelines, f"Ancres internes valides — {cle}", "cibles absentes : " + ", ".join(orphelines))

        # menu principal
        nav = re.search(r'<nav class="nav".*?</nav>', html, flags=re.S)
        nav = nav.group(0) if nav else ""
        attendus = {"L'approche": URL["approche"], "Offres": URL["offres"], "Références": URL["references"]}
        if cle != "contact":
            attendus["Contact"] = URL["contact"]
        erreurs = []
        for libelle, url in attendus.items():
            m = re.search(r'<a href="([^"]*)"[^>]*>' + re.escape(libelle) + "</a>", nav)
            if not m or m.group(1) != url:
                erreurs.append(libelle)
        r.verifier(not erreurs, f"Menu principal vers les bonnes pages — {cle}", "à corriger : " + ", ".join(erreurs))

        # logo
        logo = re.search(r'<a class="logo" href="([^"]*)"', html)
        attendu = "#haut-page" if cle == "accueil" else URL["accueil"]
        r.verifier(logo and logo.group(1) == attendu, f"Logo — {cle}", f"cible {logo.group(1) if logo else 'absente'}")

        # pied de page : LinkedIn, Contact, DRH
        pied = re.search(r'<footer.*?</footer>', html, flags=re.S)
        pied = pied.group(0) if pied else ""
        manques = [n for n, u in (("LinkedIn", LINKEDIN), ("Contact", URL["contact"]), ("DRH", URL["drh"])) if u not in pied]
        r.verifier(not manques, f"Pied de page complet — {cle}", "manque : " + ", ".join(manques))

        # liens morts autorisés : uniquement les PDF à déposer à la mise en ligne
        morts = []
        for m in re.finditer(r'<a([^>]*)href="#"([^>]*)>(.*?)</a>', html, flags=re.S):
            lib = texte_visible(m.group(3)).strip()
            if "PDF" not in lib:
                morts.append(lib[:40])
        r.verifier(not morts, f"Aucun lien vide hors PDF — {cle}", "liens vides : " + " | ".join(morts))

        # boutons de rendez-vous : toujours Calendly
        rdv = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>\s*(?:Prendre rendez-vous|Rendez-vous)\s*</a>', html)
        mauvais = [u for u in rdv if u != CALENDLY]
        r.verifier(not mauvais, f"« Prendre rendez-vous » vers Calendly — {cle}", f"{len(mauvais)} bouton(s) mal ciblé(s)")

        # téléphone : toujours cliquable
        nus = len(re.findall(r"\+33 6 24 39 25 27", texte_visible(html)))
        lies = len(re.findall(r'href="' + re.escape(TEL) + '"', html))
        r.verifier(nus == lies, f"Numéro de téléphone cliquable — {cle}", f"{nus} mention(s), {lies} lien(s) d'appel")

        # bandeau d'appel à l'action : trois boutons, dans l'ordre demandé
        bandeau = re.search(r'<div class="appel-actions">(.*?)</div>', html, flags=re.S)
        if bandeau:
            libs = [texte_visible(x).strip() for x in re.findall(r"<a[^>]*>(.*?)</a>", bandeau.group(1), flags=re.S)]
            cibles = re.findall(r'href="([^"]*)"', bandeau.group(1))
            ordre_ok = libs[:3] == ["Préciser votre besoin en 3 minutes", "Prendre rendez-vous", "Appeler le +33 6 24 39 25 27"]
            cibles_ok = cibles[:3] == [TALLY, CALENDLY, TEL]
            r.verifier(ordre_ok and cibles_ok, f"Bandeau : Préciser, Rendez-vous, Appeler — {cle}", f"trouvé : {libs} → {cibles}")

    # Carte « Vous êtes dirigeant » : vers les quatre temps
    carte = re.search(r'Vous êtes dirigeant</h3>.*?<a href="([^"]*)"', sources.get("accueil", ""), flags=re.S)
    r.verifier(carte and carte.group(1) == URL["offres"], "Carte « Vous êtes dirigeant » vers la page Offres",
               f"cible : {carte.group(1) if carte else 'absente'}")
    carte = re.search(r'Vous êtes DRH</h3>.*?<a href="([^"]*)"', sources.get("accueil", ""), flags=re.S)
    r.verifier(carte and carte.group(1) == URL["drh"], "Carte « Vous êtes DRH » vers la page DRH",
               f"cible : {carte.group(1) if carte else 'absente'}")
    r.verifier(TALLY in sources.get("contact", ""), "Questionnaire Tally sur la page Contact", "lien absent")

    # ------------------------------------------------------------------
    # 3. Rendu (tests dans un navigateur, à plusieurs largeurs)
    # ------------------------------------------------------------------
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for cle, fichier in PAGES.items():
            if cle not in sources:
                continue
            for largeur in LARGEURS:
                page = nav.new_page(viewport={"width": largeur, "height": 900})
                page.goto((DOSSIER / fichier).resolve().as_uri())
                page.wait_for_timeout(250)
                ecart = page.evaluate("document.documentElement.scrollWidth") - largeur
                if largeur >= 760:
                    tabs = page.evaluate("() => [...document.querySelectorAll('.tableau')].filter(e => e.scrollWidth - e.clientWidth > 1).map(e => e.getAttribute('aria-label'))")
                    r.verifier(not tabs, f"Tableaux lisibles sans défilement — {cle} à {largeur} px", "à faire défiler : " + ", ".join(tabs or []))
                r.verifier(ecart <= 0, f"Pas de défilement horizontal — {cle} à {largeur} px", f"débordement de {ecart} px")
                if largeur == 1440:
                    r.verifier(page.evaluate("window.scrollY") == 0, f"Ouverture en haut de page — {cle}", "page ouverte décalée")
                    # logo Qualiopi : proportions d'origine (353 x 200)
                    ratio = page.evaluate("""() => { const i = document.querySelector('img.logo-q');
                        if (!i) return null; const r = i.getBoundingClientRect(); return r.width / r.height; }""")
                    r.verifier(ratio is not None and abs(ratio - 353 / 200) < 0.25,
                               f"Logo Qualiopi non déformé — {cle}", f"rapport largeur/hauteur {ratio}")
                    # trois badges au pied de page
                    nb = page.evaluate("document.querySelectorAll('footer .badges img').length")
                    r.verifier(nb == 3, f"Trois badges au pied de page — {cle}", f"{nb} badge(s)")
                    geo = page.evaluate("""() => { const bs = [...document.querySelectorAll('footer .badges .badge')].map(e => e.getBoundingClientRect());
                        const t = document.querySelector('footer .qualiopi p'); if (!bs.length || !t) return null; const tr = t.getBoundingClientRect();
                        return { h: bs.map(r => Math.round(r.height)), d: Math.round(bs[bs.length - 1].right), td: Math.round(tr.right) }; }""")
                    r.verifier(geo and len(set(geo["h"])) == 1 and geo["d"] <= geo["td"] + 1,
                               f"Badges de même hauteur, dans la largeur du texte — {cle}", f"mesures {geo}")
                page.close()

        # Photos : dimensions fixes, indépendantes du fichier utilisé
        for largeur, attendu_bio, attendu_rond in ((1440, (240, 300), (300, 300)), (390, (220, 275), (260, 260))):
            page = nav.new_page(viewport={"width": largeur, "height": 900})
            page.goto((DOSSIER / PAGES["approche"]).resolve().as_uri()); page.wait_for_timeout(250)
            dims = page.evaluate("() => { const r = document.querySelector('.bio img').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
            r.verifier(tuple(dims) == attendu_bio, f"Photo de l'encart biographique à {largeur} px", f"{dims} au lieu de {attendu_bio}")
            page.goto((DOSSIER / PAGES["accueil"]).resolve().as_uri()); page.wait_for_timeout(250)
            dims = page.evaluate("() => { const r = document.querySelector('.portrait img').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
            r.verifier(tuple(dims) == attendu_rond, f"Photo ronde de l'accueil à {largeur} px", f"{dims} au lieu de {attendu_rond}")
            page.close()

        # Logo de l'accueil : retour en haut de page
        page = nav.new_page(viewport={"width": 1440, "height": 900})
        page.goto((DOSSIER / PAGES["accueil"]).resolve().as_uri()); page.wait_for_timeout(250)
        page.evaluate("window.scrollTo(0, 2500)"); page.wait_for_timeout(150)
        page.click("a.logo"); page.wait_for_timeout(1000)
        r.verifier(page.evaluate("window.scrollY") == 0, "Logo de l'accueil : retour en haut", "la page ne remonte pas")

        # Témoignages de l'accueil : cartes de même hauteur, extraits équilibrés
        hauteurs = page.evaluate("() => Array.from(document.querySelectorAll('.temoignage')).map(e => Math.round(e.getBoundingClientRect().height))")
        r.verifier(len(set(hauteurs)) == 1, "Témoignages de l'accueil de même hauteur", f"hauteurs {hauteurs}")
        mots = page.evaluate("() => Array.from(document.querySelectorAll('.temoignage blockquote')).map(e => e.innerText.split(/\\s+/).length)")
        r.verifier(mots and max(mots) - min(mots) <= 4, "Extraits de témoignages équilibrés (écart ≤ 4 mots)", f"longueurs {mots}")

        # Catalogue : colonnes de même hauteur
        page.goto((DOSSIER / PAGES["offres"]).resolve().as_uri()); page.wait_for_timeout(250)
        hauteurs = page.evaluate("() => Array.from(document.querySelectorAll('.cat-col')).map(e => Math.round(e.getBoundingClientRect().height))")
        r.verifier(len(set(hauteurs)) == 1, "Catalogue : quatre colonnes de même hauteur", f"hauteurs {hauteurs}")
        page.close()
        nav.close()

    # ------------------------------------------------------------------
    # Rapport
    # ------------------------------------------------------------------
    total = len(r.lignes)
    entete = f"# Rapport de tests du site ACC — {date.today().isoformat()}\n\n{total - r.echecs} règles respectées sur {total}, {r.echecs} échec(s).\n\n"
    corps = "| Statut | Règle | Détail |\n| --- | --- | --- |\n"
    for statut, regle, detail in sorted(r.lignes, key=lambda x: x[0] != "ÉCHEC"):
        corps += f"| {statut} | {regle} | {detail} |\n"
    (DOSSIER / "rapport-tests.md").write_text(entete + corps, encoding="utf-8")
    print(entete)
    for statut, regle, detail in r.lignes:
        if statut == "ÉCHEC":
            print(f"  ÉCHEC  {regle} : {detail}")
    sys.exit(1 if r.echecs else 0)


if __name__ == "__main__":
    main()
