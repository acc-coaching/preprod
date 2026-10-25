"""Règles éditoriales du site ACC.

Chaque règle traduit une décision déjà prise par Christophe. Ce fichier
évolue à chaque mise à jour du site : une nouvelle décision ajoute ou
modifie une règle ici, le moteur (verifier.py) ne change pas.
"""

CALENDLY = "https://calendly.com/christophe-andreu/30min/"
TALLY = "https://tally.so/r/lbpZMp"
LINKEDIN = "https://www.linkedin.com/in/christopheandreu/"
TEL = "tel:+33624392527"
LARGEURS = [390, 760, 1100, 1440]
TEMPS = ["Réussir sa prise de poste", "Développer son leadership",
         "Faire grandir l'équipe", "Réussir sa transition"]

# Vocabulaire proscrit dans le texte visible : (motif, décision d'origine)
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
    (r"accompagnées depuis 2020|\b272\b", "Indicateurs bilan périmés : 272 personnes depuis 2020"),
    (r"13 octobre 2025", "Date d'indicateurs bilan périmée (màj 08/10/2026)"),
    (r"Cloudflare", "Hébergement sur GitHub Pages, plus de Cloudflare"),
]

# Contenus attendus : (page, texte exact, intitulé de la règle)
FAITS = [
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
    ("drh", "Managers et managers de managers", "DRH : libellé de la ligne managers"),
    ("confidentialite", "Calendly, synchronisé avec mon agenda Google", "Confidentialité : réservation via Calendly"),
    ("confidentialite", "Tally, Calendly, Google et GitHub", "Confidentialité : sous-traitants à jour (GitHub)"),
    ("cgu", "Aucune prestation n'est vendue ni payée en ligne", "CGU : pas de vente en ligne"),
    ("cgu", "ce sont eux qui prévalent sur les présentes conditions", "CGU : primauté des CGV et conventions"),
    # Indicateurs des bilans de compétences — mis à jour le 08/10/2026
    ("qualiopi", "personnes accompagnées depuis 2023", "Qualiopi : millésime des bilans (2023)"),
    ("qualiopi", "de bilans menés à terme", "Qualiopi : indicateur d'abandon"),
    ("qualiopi", "hors prestations en sous-traitance", "Qualiopi : périmètre des indicateurs bilan"),
    ("qualiopi", "Mis à jour le 8 octobre 2026", "Qualiopi : date des indicateurs bilan"),
    ("qualiopi", "personnes formées depuis 2023", "Qualiopi : indicateurs formations préservés"),
    ("qualiopi", "Mis à jour le 4 août 2025", "Qualiopi : date des indicateurs formations préservée"),
    ("transition", "personnes accompagnées depuis 2023", "Transition : millésime des bilans (2023)"),
    ("transition", "de bilans menés à terme", "Transition : indicateur d'abandon"),
    ("transition", "hors prestations en sous-traitance", "Transition : périmètre des indicateurs bilan"),
    ("transition", "Mis à jour le 8 octobre 2026", "Transition : date des indicateurs bilan"),
]

# Ordre des secteurs sur la page Références
SECTEURS = ["Banque, assurance, investissement", "Conseil et cabinets d'avocats", "Tech, digital, télécoms",
            "Luxe, consommation, distribution", "Énergie, industrie, construction", "Services, santé, éducation"]

# Écarts admis : signalés en ALERTE sans bloquer la publication.
# Chaque entrée est une décision de Christophe, datée, à retirer dès que l'écart est résolu.
ECARTS_ADMIS = {
    "Documents — fichiers présents": "PDF réglementaires pas encore déposés, liens morts déjà présents en ligne ; "
                                     "à résoudre par la mise à jour des bilans (25/10/2026)",
}
