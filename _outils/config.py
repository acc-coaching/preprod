"""Paramètres communs aux outils de publication du site ACC.

Ce fichier est la seule source de vérité sur les deux environnements.
Les fichiers propres à chaque environnement (CNAME, robots.txt) sont
générés à partir d'ici : ils ne sont jamais recopiés d'un dépôt à l'autre.
"""

DOMAINE_OFFICIEL = "acc-coaching.fr"
URL_OFFICIELLE = f"https://{DOMAINE_OFFICIEL}"

ENVIRONNEMENTS = {
    "preprod": {
        "depot": "acc-coaching/preprod",
        "domaine": "preprod.acc-coaching.fr",
        "indexable": False,
        "robots": "User-agent: *\nDisallow: /\n",
    },
    "prod": {
        "depot": "acc-coaching/prod",
        "domaine": DOMAINE_OFFICIEL,
        "indexable": True,
        "robots": f"User-agent: *\nAllow: /\n\nSitemap: {URL_OFFICIELLE}/sitemap.xml\n",
    },
}

# Balise posée sur chaque page de préprod, retirée au passage en prod
BALISE_NOINDEX = '<meta name="robots" content="noindex">'

# Ce qui ne part jamais en prod
EXCLUS_DE_LA_PROD = {".git", "_outils", "CNAME", "robots.txt", "rapport-tests.md"}

# Pages publiques : clé -> fichier dans le dépôt
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
    "cgu": "cgu.html",
}

# Liens internes : le site utilise des adresses sans extension (/approche)
URL = {cle: ("/" if f == "index.html" else "/" + f[:-5]) for cle, f in PAGES.items()}
