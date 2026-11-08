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
    (r"conserve la faculté de recourir", "Médiateur de la consommation nommé : CM2C (adhésion du 31/10/2026)"),
    (r"Sur le site définitif", "Mention provisoire de la page Contact retirée (01/11/2026)"),
    (r"Pour l'assistance technique à distance", "Assistance technique et pédagogique, réponse sous 2 jours ouvrés (01/11/2026)"),
    (r"feuilles de présence et une évaluation à chaud", "Suivi du bilan : questionnaire à 6 mois ajouté (02/11/2026)"),
    # (?#class=) : commentaire d'expression qui fait porter le contrôle sur le HTML complet, métadonnées comprises
    (r"(?#class=)cycle de vie|temps du cycle", "« Les temps forts du dirigeant » remplace « cycle de vie » (08/11/2026)"),
    (r"\bERAFP\b|\bNomura\b|Eversheds|Addleshaw|Coblence|\bEPAM\b|Rydge|Oh my cream|GRTgaz|\bGlady\b",
     "Références retirées ou renommées le 08/11/2026 (NaTran, Pluxee)"),
    (r"McKinsey|HM Clause|Galileo", "Références retirées le 08/11/2026 (McKinsey remplacé par BearingPoint sur l'accueil)"),
    (r"Ashurst", "Ashurst Perkins Coie : à ajouter aux références vers mars-avril 2027, mission en cours"),
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
    ("offres", "24 heures sur 12 à 16 semaines, en présentiel ou 100 % à distance ; éligible CPF, 100 % à distance", "Bilan : modalités dans le catalogue (CPF 100 % à distance)"),
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
    ("qualiopi", "Dernière mise à jour : novembre 2026", "Qualiopi : date de mise à jour de la page"),
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
    # Médiateur de la consommation — adhésion CM2C du 31/10/2026
    ("mentions", "Médiation de la consommation", "Mentions légales : rubrique Médiation de la consommation"),
    ("mentions", "CM2C, Centre de la Médiation de la Consommation de Conciliateurs de Justice, 49 rue de Ponthieu, 75008 Paris", "Mentions légales : identité et adresse du médiateur"),
    ("mentions", "01 89 47 00 14", "Mentions légales : téléphone du médiateur"),
    ("mentions", "mailto:cm2c@cm2c.net", "Mentions légales : courriel du médiateur cliquable"),
    ("mentions", "https://www.cm2c.net", "Mentions légales : site du médiateur cliquable"),
    ("mentions", "dans un délai d'un an à compter de celle-ci", "Mentions légales : délai de saisine"),
    ("cgu", "Un consommateur peut recourir gratuitement au médiateur de la consommation dont relève ACC : CM2C", "CGU : médiateur nommé"),
    ("cgu", 'CM2C (coordonnées dans les <a href="/mentions-legales">mentions légales</a>).', "CGU : renvoi vers les coordonnées du médiateur"),
    ("mentions", "Dernière mise à jour : octobre 2026", "Mentions légales : date de mise à jour de la page"),
    ("cgu", "Dernière mise à jour : octobre 2026", "CGU : date de mise à jour de la page"),
    ("qualiopi", "Si vous agissez en qualité de consommateur, notamment pour un bilan de compétences financé à titre personnel ou par le compte personnel de formation, et que la réponse ne vous satisfait pas, vous pouvez saisir gratuitement le médiateur de la consommation CM2C", "Qualiopi : médiateur réservé aux consommateurs (01/11/2026)"),
    ("qualiopi", "Les formations, conclues avec des entreprises, relèvent des relations entre professionnels.", "Qualiopi : formations hors médiation de la consommation"),
    ("qualiopi", "Le référent qui recueille les signalements est formé à la prévention des violences sexistes et sexuelles.", "Qualiopi : formation du référent violences"),
    ("contact", "Le questionnaire s'ouvre dans un nouvel onglet.", "Contact : ouverture du questionnaire signalée"),
    # Indicateur 1 et distanciel — brief du 01/11/2026 (guide de lecture Qualiopi V10)
    ("transition", "avec un certificat de réalisation : le bilan est une prestation non certifiante", "Transition : type de reconnaissance du bilan"),
    ("transition", "Cadre légal : le bilan de compétences est régi par les articles L.6313-1, L.6313-4 et R.6313-4 à R.6313-8 du Code du travail", "Transition : cadre légal du bilan"),
    ("transition", "Un bilan financé par le CPF se déroule exclusivement à distance.", "Transition : bilan CPF 100 % à distance"),
    ("transition", "Il comprend 12 heures de séances synchrones (8 séances d'1h30, en présentiel ou en visioconférence) et environ 12 heures de travail personnel à distance", "Transition : quantification des temps synchrones et asynchrones"),
    ("transition", "Pour l'assistance technique et pédagogique, écrivez à", "Transition : assistance technique et pédagogique"),
    ("transition", "réponse sous 2 jours ouvrés.", "Transition : délai de réponse de l'assistance"),
    ("transition", "<dd>8 séances d'1h30 (synchrones) et 12 heures de travail personnel à distance</dd>", "Transition : fiche, séances"),
    ("transition", "<dd>Finançable par le CPF (bilan alors 100 % à distance)</dd>", "Transition : fiche, financement"),
    ("transition", "<dt>Reconnaissance</dt><dd>Prestation non certifiante : synthèse et certificat de réalisation</dd>", "Transition : fiche, reconnaissance"),
    ("equipe", "en présentiel ou, sur demande, en classe virtuelle synchrone ; présentiel exigé pour l'intelligence émotionnelle", "Équipe : fiche, modalités"),
    ("equipe", "<dt>Reconnaissance</dt><dd>Formation non certifiante : certificat de réalisation remis à chaque stagiaire</dd>", "Équipe : fiche, reconnaissance"),
    ("equipe", "peuvent être animées à distance en classe virtuelle synchrone", "Équipe : classe virtuelle synchrone"),
    ("equipe", "Assistance technique et pédagogique : <a href=\"mailto:christophe.andreu@acc-coaching.fr\">christophe.andreu@acc-coaching.fr</a>, réponse sous 2 jours ouvrés.", "Équipe : assistance technique et pédagogique"),
    # Affiche de la politique d'accessibilité — brief du 02/11/2026
    ("qualiopi", 'href="documents/acc-affiche-politique-accessibilite.pdf" target="_blank" rel="noopener">Affiche de notre politique d\'accessibilité <span>PDF</span>', "Qualiopi : affiche dans la liste des documents"),
    ("qualiopi", "ACC est engagé dans la démarche de progrès de la Ressource Handicap Formation Île-de-France.", "Qualiopi : démarche RHF"),
    ("qualiopi", "affiche de politique d'accessibilité (PDF)</a>", "Qualiopi : lien vers l'affiche dans la rubrique accessibilité"),
    # Questionnaire de suivi à 6 mois du bilan — brief du 02/11/2026 (indicateur 30)
    ("transition", "Le suivi repose sur les feuilles de présence, une évaluation à chaud par questionnaire de satisfaction à l'issue de la dernière séance, puis un questionnaire de suivi 6 mois après la fin du bilan, sur la mise en œuvre de votre projet.", "Transition : questionnaire de suivi à 6 mois"),
    # Proposition de valeur — accueil validé le 08/11/2026
    ("accueil", "Executive Coach &amp; Strategic Mentor", "Accueil : bandeau Executive Coach & Strategic Mentor"),
    ("accueil", "Quand les enjeux stratégiques, humains et systémiques s'entremêlent, j'accompagne les dirigeants et leurs équipes à décider et à passer à l'action. En sparring-partner, j'allie l'écoute exigeante du coach et la rigueur du consultant.", "Accueil : paragraphe d'accroche"),
    ("accueil", "Les temps forts du dirigeant</h2>", "Accueil : titre Les temps forts du dirigeant"),
    ("accueil", "À chaque temps fort, ses enjeux : mes accompagnements les suivent.", "Accueil : sous-titre des temps forts"),
    ("offres", "<h1>Les offres, à chaque temps fort du dirigeant</h1>", "Offres : titre de page"),
    ("offres", "le catalogue ACC, rangé selon les temps forts du dirigeant.\">", "Offres : description Google"),
    ("drh", "qui suivent les temps forts d'un dirigeant", "DRH : temps forts du dirigeant"),
    ("approche", "Les quatre temps forts du dirigeant</h2>", "Approche : titre des quatre temps forts"),
    ("approche", "Executive Coach &amp; Strategic Mentor : un sparring-partner pour vos décisions", "Approche : rubrique sparring-partner"),
    ("approche", "Je vous dis toujours quelle casquette je porte", "Approche : transparence sur la posture (ICF)"),
    ("approche", "Je ne décide pas à votre place.", "Approche : pas de décision à la place du client"),
    ("references", "LGH &amp; Associés · Ooslo · BearingPoint", "Références : Ooslo en dernier des cabinets d'avocats"),
    ("accueil", "PwC · A&amp;O Shearman · Google", "Accueil : ordre des références conseil"),
    ("references", '<h2 style="margin-bottom: 28px;">Références par secteur</h2>', "Références : espace sous le titre des secteurs"),
    ("references", "Certaines références sont issues de mes vingt ans de conseil en stratégie.", "Références : mention des références de conseil"),
    ("accueil", '<a class="btn btn-contour" href="/references">Voir toutes les références</a>', "Accueil : renvoi vers toutes les références"),
    ("accueil", "Et plus de 100 autres organisations.", "Accueil : mention des autres organisations"),
    ("equipe", "Mis à jour le 6 octobre 2026", "Équipe : date des indicateurs formations en direct"),
    ("equipe", "<b>201</b>", "Équipe : formation au management en sous-traitance"),
    ("equipe", "Mis à jour le 25 octobre 2026", "Équipe : date des indicateurs en sous-traitance"),
]

# Documents téléchargeables : (fichier, sources dans le dossier Qualiopi de Christophe)
DOCUMENTS = {
    "acc-programme-bilan-de-competences.pdf": "20.Bilan de compétences/10.Programme de bilan de compétences/ACC-Bilan de compétences-Programme.pdf",
    "acc-livret-accueil-bilan-de-competences.pdf": "20.Bilan de compétences/40.Convocation et livret d'accueil/ACC-Bilan de compétences-Livret d’accueil.pdf",
    "acc-cgv-bilan-de-competences.pdf": "20.Bilan de compétences/30.Contrat et CGV/ACC-Bilan de compétences-CGV.pdf",
    "acc-cgv-formations.pdf": "30.Formation/30.Convocation/ACC-Formation-CGV.pdf",
    "acc-reglement-interieur.pdf": "10.Transverse/30.Procédures et règlement intérieur/Règlement intérieur-I9/ACC-Règlement intérieur.pdf",
    "acc-charte-deontologie-formateur.pdf": "10.Transverse/30.Procédures et règlement intérieur/Déontologie-I17/ACC-Déontologie du formateur et du consultant.pdf",
    "acc-affiche-politique-accessibilite.pdf": "10.Transverse/70.Situation de handicap/30.RHF-Politique accessibilité-I1-I26/202611 RHF Politique accessibilité/20261102-ACC-RHF-Affiche politique accessibilité.pdf",
    "acc-certificat-qualiopi.pdf": "40.Audits Certifopac/60.Certificat Qualiopi/Certificat Qualiopi - Mise à jour le 24.06.2024.pdf",
}
# Vocabulaire proscrit dans le texte des PDF publiés : (motif, documents concernés ou None pour tous, décision)
INTERDITS_DOCUMENTS = [
    (r"CoachHub|EZRA|LHH|Click ?& ?Coach|\bChance\b|Opale", None, "Marque ACC seule, sans plateformes ni donneurs d'ordre"),
    (r"\bZoom\b", None, "Visioconférence sur Google Meet uniquement"),
]
# Contenus attendus dans le texte des PDF publiés : (document, texte, intitulé)
FAITS_DOCUMENTS = [
    ("acc-affiche-politique-accessibilite.pdf", "est engagé dans la démarche d'accessibilité", "Affiche accessibilité : engagement RHF"),
    ("acc-affiche-politique-accessibilite.pdf", "Contactez notre référent handicap : Christophe Andreu", "Affiche accessibilité : référent handicap"),
    ("acc-programme-bilan-de-competences.pdf", "Version 20261102", "Programme du bilan : version du 02/11/2026"),
    ("acc-programme-bilan-de-competences.pdf", "questionnaire de suivi 6 mois après la fin du bilan", "Programme du bilan : questionnaire de suivi à 6 mois"),
    ("acc-programme-bilan-de-competences.pdf", "non certifiante", "Programme du bilan : type de reconnaissance"),
    ("acc-cgv-formations.pdf", "Version 20261101", "CGV formations : version du 01/11/2026"),
    ("acc-cgv-formations.pdf", "relatives à la médiation de la consommation (articles L.612-1 et suivants) ne s’appliquent pas", "CGV formations : médiation de la consommation non applicable aux professionnels"),
    ("acc-cgv-bilan-de-competences.pdf", "Version 20261031", "CGV du bilan : version du 31/10/2026"),
    ("acc-cgv-bilan-de-competences.pdf", "CM2C", "CGV du bilan : médiateur CM2C"),
    ("acc-livret-accueil-bilan-de-competences.pdf", "Version 20261102", "Livret d'accueil : version du 02/11/2026"),
    ("acc-livret-accueil-bilan-de-competences.pdf", "questionnaire de suivi", "Livret d'accueil : questionnaire de suivi à 6 mois"),
    ("acc-livret-accueil-bilan-de-competences.pdf", "CM2C", "Livret d'accueil : médiateur CM2C"),
]

# Auteurs admis dans les métadonnées des PDF publiés (aucun nom de tiers)
AUTEURS_ADMIS = {"", "ACC", "Christophe Andreu", "Christophe ANDREU"}

# Ordre des secteurs sur la page Références
SECTEURS = ["Banque, assurance, investissement", "Conseil et cabinets d'avocats", "Tech, digital, télécoms, médias",
            "Luxe, consommation, distribution", "Énergie, industrie, construction", "Services, transport, santé, éducation"]

# Références validées le 08/11/2026 : (secteur, nombre de noms, premier nom, dernier nom)
REFERENCES = [
    ("Banque, assurance, investissement", 21, "AXA", "SPE Capital"),
    ("Conseil et cabinets d'avocats", 14, "A&amp;O Shearman", "Scalian"),
    ("Tech, digital, télécoms, médias", 23, "Amazon", "Mediarithmics"),
    ("Luxe, consommation, distribution", 26, "LVMH", "JJA"),
    ("Énergie, industrie, construction", 33, "TotalEnergies", "EIT Manufacturing"),
    ("Services, transport, santé, éducation", 18, "Accor", "Ministère de la Défense"),
]
REFERENCES_ACCUEIL = 30

# Écarts admis : signalés en ALERTE sans bloquer.
# Clé : début de l'intitulé de la règle. Valeur : (décision datée, environnements où l'écart est admis).
# Un écart admis seulement en préprod bloque la mise en production tant que Christophe n'a pas tranché.
ECARTS_ADMIS = {}
