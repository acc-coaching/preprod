# Site ACC — process de mise à jour

Référence du circuit de publication de acc-coaching.fr. Mis à jour le 25 octobre 2026.

## Les deux environnements

| Environnement | Dépôt GitHub | Adresse | Indexation |
| --- | --- | --- | --- |
| Préprod | `acc-coaching/preprod` | https://preprod.acc-coaching.fr | Interdite (balise `noindex` sur chaque page, `robots.txt` en `Disallow`) |
| Prod | `acc-coaching/prod` | https://acc-coaching.fr | Autorisée |

Adresse officielle : **acc-coaching.fr**, sans www. Les canoniques, le sitemap et les
partages sociaux pointent tous vers elle, y compris depuis la préprod.

Hébergement : GitHub Pages, publication depuis la branche `main`, HTTPS forcé.
DNS chez Squarespace : quatre `A` et quatre `AAAA` GitHub sur l'apex, `CNAME` `www` et
`preprod` vers `acc-coaching.github.io`. **Les enregistrements MX, SPF et DKIM portent
la messagerie Google Workspace : on n'y touche jamais.**

La préprod est la seule source. On ne modifie jamais la prod directement : elle est
reconstruite à chaque promotion à partir de la préprod validée.

## Les six étapes d'une mise à jour

| Étape | Qui | Ce qui est vérifié |
| --- | --- | --- |
| 1. Brief | Christophe et Claude | Contenu, pièces, pages visées. Repérage des données personnelles dans les documents fournis |
| 2. Modification en préprod | Claude | Les règles éditoriales de la mise à jour sont ajoutées à `regles.py` **avant** la modification |
| 3. Tests puis publication en préprod | Claude | `verifier.py --env preprod` sans échec, puis contrôle en ligne dans Chrome |
| 4. Validation préprod | Christophe | Récapitulatif page par page fourni par Claude. Feu vert explicite : « go prod » |
| 5. Promotion vers la prod | Claude | `promouvoir.py` : répétition à blanc, puis publication si tous les tests passent en mode prod |
| 6. Contrôle de la prod | Claude puis Christophe | Contrôle en ligne dans Chrome, puis validation finale |

## Les outils (dossier `_outils/` du dépôt préprod)

Le dossier commence par un tiret bas : GitHub Pages ne le publie pas, et il n'est jamais
recopié en prod.

`config.py` décrit les deux environnements. C'est la seule source de vérité pour le
domaine, le `CNAME` et le `robots.txt` de chaque environnement.

`regles.py` contient les règles éditoriales : vocabulaire proscrit, contenus attendus,
écarts admis. Chaque décision de Christophe y devient une règle. C'est le seul fichier
qui évolue d'une mise à jour à l'autre.

`verifier.py` exécute les contrôles : environnement (indexation, domaine, sitemap),
contenu, liens, documents téléchargeables, et rendu de chaque page dans un navigateur à
390, 760, 1100 et 1440 px. Un échec bloque la publication. Un écart admis par Christophe
apparaît en alerte sans bloquer.

`promouvoir.py` reconstruit la prod depuis la préprod validée : il refuse de partir si la
préprod locale diffère de celle en ligne, retire la balise `noindex`, régénère le `CNAME`
et le `robots.txt` de prod, puis relance tous les tests en mode prod. Sans l'option
`--publier`, il s'arrête avant l'envoi.

`controle-en-ligne.js` contrôle un environnement en ligne depuis Chrome : chaque page du
sitemap répond, indexation conforme à l'environnement, canonique correcte, documents
téléchargeables présents, outils internes non exposés.

`journal.md` trace chaque mise à jour : date, contenu, commits préprod et prod, résultats
des tests.

## Retour arrière

Si la prod pose problème après publication : `git revert` du dernier commit de prod,
puis envoi. Le site revient à la version précédente en une à deux minutes.

## Points ouverts

**Documents réglementaires.** Les liens des pages Qualité et Réussir sa transition
renvoient vers sept PDF absents du dossier `documents/`. Écart admis le 25/10/2026, à
résoudre par la mise à jour des bilans de compétences.

**Données structurées `schema.org`.** Absentes du dépôt, à porter dans une passe dédiée.

**Redirection de www.** `www.acc-coaching.fr` doit rediriger vers `acc-coaching.fr`. Le
DNS est en place ; à vérifier une fois le certificat HTTPS émis par GitHub.

**Médiateur de la consommation, accords de sous-traitance, numéro de TVA** : voir la
procédure du 9 octobre 2026.
