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
    (r"Opale", "Sous-traitance formation : ne pas nommer le donneur d'ordre"),
    (r"remis sur demande", "Formations : programme établi après l'analyse du besoin (décision du 25/10/2026)"),
    (r"recevant du public", "Locaux d'ACC non aménagés pour l'accueil du public (décision du 25/10/2026)"),
    (r"au plus tard 10 jours", "Convocation du bilan entre 15 et 7 jours avant la première séance (décision du 25/10/2026)"),
    (r"procedure-prevention", "La procédure de prévention est interne, non publiée (décision du 25/10/2026)"),
    (r"personnes accompagnées depuis 2023", "Libellé de la fiche Information du public : « bilans terminés »"),
    (r"8 octobre 2026|4 août 2025", "Dates d'indicateurs périmées (màj 19/10/2026 et 06/10/2026)"),
    (r"\b93 %", "Atteinte des objectifs des bilans : 94 % au 19/10/2026"),
    (r"entièrement à distance|Il se déroule à distance|>100 % à distance", "Bilan : en présentiel ou 100 % à distance (décision du 25/10/2026)"),
]

# Contenus attendus : (page, texte exact, intitulé de la règle)
FAITS = [
    ("transition", "En présentiel ou 100 % à distance, sur Google Meet", "Bilan : en présentiel ou 100 % à distance sur Google Meet (fiche)"),
    ("transition", "dans les locaux d'ACC à Nanterre, ou 100 % à distance", "Bilan : en présentiel ou 100 % à distance (modalités)"),
    ("offres", "en présentiel ou 100 % à distance, éligible CPF", "Bilan : modalités dans le catalogue"),
    ("drh", "en présentiel ou 100 % à distance sur Google Meet", "Bilan : modalités sur la page DRH"),
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
    # Indicateurs Qualiopi — source : fiche « Information du public » du 19/10/2026
    # et synthèse de satisfaction de la formation en sous-traitance du 25/10/2026
    ("qualiopi", "bilans terminés depuis 2023", "Qualiopi : volume des bilans en direct (14 depuis 2023)"),
    ("qualiopi", "<b>14</b>", "Qualiopi : 14 bilans en direct"),
    ("qualiopi", "de bilans menés à terme", "Qualiopi : indicateur d'abandon"),
    ("qualiopi", "<b>94 %</b>", "Qualiopi : atteinte des objectifs des bilans à 94 %"),
    ("qualiopi", "10 répondants", "Qualiopi : répondants satisfaction bilans"),
    ("qualiopi", "9 répondants", "Qualiopi : répondants atteinte des objectifs bilans"),
    ("qualiopi", "hors prestations en sous-traitance", "Qualiopi : périmètre des indicateurs bilan en direct"),
    ("qualiopi", "Mis à jour le 19 octobre 2026", "Qualiopi : date des indicateurs bilan"),
    ("qualiopi", "Dernière mise à jour : octobre 2026", "Qualiopi : date de mise à jour de la page"),
    ("qualiopi", "bilans terminés / bilans démarrés", "Qualiopi : méthode de calcul des bilans en direct"),
    ("qualiopi", "<b>283</b>", "Qualiopi : 283 bilans en sous-traitance"),
    ("qualiopi", "<b>83 %</b>", "Qualiopi : recommandation des bilans en sous-traitance"),
    ("qualiopi", "opérateur national de bilans de compétences", "Qualiopi : sous-traitance bilans sans nommer la plateforme"),
    ("qualiopi", "142 réponses", "Qualiopi : base de la note de recommandation"),
    ("qualiopi", "Techniques du conseil", "Qualiopi : indicateurs formation rattachés aux Techniques du conseil"),
    ("qualiopi", "personnes formées depuis 2023", "Qualiopi : indicateurs formations en direct"),
    ("qualiopi", "Mis à jour le 6 octobre 2026", "Qualiopi : date des indicateurs formations en direct"),
    ("qualiopi", "<b>201</b>", "Qualiopi : 201 personnes formées en sous-traitance"),
    ("qualiopi", "75 réponses", "Qualiopi : base de la satisfaction formation en sous-traitance"),
    ("qualiopi", "Mis à jour le 25 octobre 2026", "Qualiopi : date des indicateurs formation en sous-traitance"),
    ("qualiopi", "Prévention des violences, du harcèlement et des discriminations", "Qualiopi : rubrique prévention des violences"),
    ("qualiopi", "votre signalement est pris en compte sous 48 heures", "Qualiopi : prévention alignée sur le programme du bilan"),
    ("transition", "bilans terminés depuis 2023", "Transition : volume des bilans en direct"),
    ("transition", "<b>94 %</b>", "Transition : atteinte des objectifs à 94 %"),
    ("transition", "10 répondants", "Transition : répondants satisfaction"),
    ("transition", "de bilans menés à terme", "Transition : indicateur d'abandon"),
    ("transition", "hors prestations en sous-traitance", "Transition : périmètre des indicateurs bilan"),
    ("transition", "Mis à jour le 19 octobre 2026", "Transition : date des indicateurs bilan"),
    # Revue Qualiopi du 25/10/2026, indicateur 1
    ("offres", "Chaque formation est conçue sur mesure : le programme détaillé (objectifs, prérequis, déroulé, modalités d'évaluation) est établi après l'analyse de votre besoin et vous est remis avec la proposition, avant toute contractualisation.", "Offres : programme des formations établi sur mesure"),
    ("equipe", "Chaque formation est conçue sur mesure : le programme détaillé (objectifs, prérequis, déroulé, modalités d'évaluation) est établi après l'analyse de votre besoin et vous est remis avec la proposition, avant toute contractualisation.", "Équipe : programme des formations établi sur mesure"),
    ("qualiopi", "Méthode de calcul : moyenne des taux d'atteinte des objectifs et de satisfaction déclarés par les stagiaires dans le questionnaire de fin de formation, sessions 2024 et 2025 (34 répondants) ; session 2023 non mesurée.", "Qualiopi : méthode de calcul des indicateurs formation"),
    ("qualiopi", "Les locaux d'ACC à Nanterre ne sont pas aménagés pour l'accueil du public : en cas de mobilité réduite, l'accompagnement est proposé à distance ou dans un lieu accessible. Pour les formations, la salle est mise à disposition par l'entreprise cliente, qui en vérifie l'accessibilité.", "Qualiopi : accessibilité des locaux"),
    ("transition", "Les locaux d'ACC ne sont pas aménagés pour l'accueil du public : en cas de mobilité réduite, le bilan est proposé à distance ou dans un lieu accessible.", "Transition : accessibilité des locaux"),
    ("transition", "Une convocation vous est envoyée par e-mail entre 15 et 7 jours avant la première séance.", "Transition : délai de convocation"),
    ("equipe", "Mis à jour le 6 octobre 2026", "Équipe : date des indicateurs formations en direct"),
    ("equipe", "<b>201</b>", "Équipe : formation au management en sous-traitance"),
    ("equipe", "Mis à jour le 25 octobre 2026", "Équipe : date des indicateurs en sous-traitance"),
]

# Documents téléchargeables : (fichier, sources dans le dossier Qualiopi de Christophe)
DOCUMENTS = {
    "acc-programme-bilan-de-competences.pdf": "20.Bilan de compétences/10.Programme de bilan de compétences/ACC-Bilan de compétences-Programme.pdf",
    "acc-livret-accueil-bilan-de-competences.pdf": "20.Bilan de compétences/40.Convocation et livret d'accueil/ACC-Bilan de compétences-Livret d'accueil.pdf",
    "acc-cgv-bilan-de-competences.pdf": "20.Bilan de compétences/30.Contrat et CGV/ACC-Bilan de compétences-CGV.pdf",
    "acc-cgv-formations.pdf": "30.Formation/30.Convocation/ACC-Formation-CGV.pdf",
    "acc-reglement-interieur.pdf": "10.Transverse/40.Règlement intérieur-Suivi personnalisé-Abandon/ACC-Règlement intérieur.pdf",
    "acc-charte-deontologie-formateur.pdf": "10.Transverse/50.Adéquation des moyens pédagogiques et techniques/ACC-Déontologie du formateur et du consultant.pdf",
    "acc-certificat-qualiopi.pdf": "40.Audits Certifopac/60.Certificat Qualiopi/Certificat Qualiopi - Mise à jour le 24.06.2024.pdf",
}
# Vocabulaire proscrit dans le texte des PDF publiés : (motif, documents concernés ou None pour tous, décision)
INTERDITS_DOCUMENTS = [
    (r"CoachHub|EZRA|LHH|Click ?& ?Coach|\bChance\b|Opale", None, "Marque ACC seule, sans plateformes ni donneurs d'ordre"),
    (r"\bZoom\b", None, "Visioconférence sur Google Meet uniquement"),
]
# Auteurs admis dans les métadonnées des PDF publiés (aucun nom de tiers)
AUTEURS_ADMIS = {"", "ACC", "Christophe Andreu", "Christophe ANDREU"}

# Ordre des secteurs sur la page Références
SECTEURS = ["Banque, assurance, investissement", "Conseil et cabinets d'avocats", "Tech, digital, télécoms",
            "Luxe, consommation, distribution", "Énergie, industrie, construction", "Services, santé, éducation"]

# Écarts admis : signalés en ALERTE sans bloquer.
# Clé : début de l'intitulé de la règle. Valeur : (décision datée, environnements où l'écart est admis).
# Un écart admis seulement en préprod bloque la mise en production tant que Christophe n'a pas tranché.
ECARTS_ADMIS = {}
