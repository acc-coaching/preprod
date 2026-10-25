#!/usr/bin/env python3
"""Promotion de la préprod validée vers la prod.

    python3 _outils/promouvoir.py --prod ../prod "Résumé de la mise à jour"
    python3 _outils/promouvoir.py --prod ../prod "Résumé" --publier

Sans --publier, le script prépare la prod et la teste, sans rien envoyer
(répétition à blanc). Avec --publier, il commite et pousse, seulement si
tous les tests passent.

Ce que fait le script, dans l'ordre :
  1. vérifie que la préprod locale est propre et identique à GitHub,
     pour que la prod reçoive exactement ce que Christophe a relu ;
  2. recopie la préprod dans la prod, sauf .git, _outils, CNAME, robots.txt ;
  3. régénère CNAME et robots.txt de prod depuis config.py ;
  4. retire la balise noindex de chaque page ;
  5. lance tous les tests en mode prod ; au moindre échec, il s'arrête.
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

OUTILS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(OUTILS))
import config  # noqa: E402

PREPROD = OUTILS.parent


def git(depot, *args, capture=True):
    res = subprocess.run(["git", "-C", str(depot), *args], capture_output=capture, text=True)
    if res.returncode != 0:
        sys.exit(f"git {' '.join(args)} a échoué :\n{res.stderr}")
    return (res.stdout or "").strip()


def arreter(message):
    sys.exit(f"\nPROMOTION ARRÊTÉE — {message}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume", help="résumé de la mise à jour, repris dans le commit de prod")
    ap.add_argument("--prod", required=True, help="dossier du dépôt acc-coaching/prod")
    ap.add_argument("--publier", action="store_true", help="commiter et pousser si les tests passent")
    a = ap.parse_args()
    prod = pathlib.Path(a.prod).resolve()

    # 1. La préprod relue = la préprod en ligne
    git(PREPROD, "fetch", "-q", "origin")
    if git(PREPROD, "status", "--porcelain"):
        arreter("la préprod locale contient des modifications non publiées.")
    local, distant = git(PREPROD, "rev-parse", "HEAD"), git(PREPROD, "rev-parse", "origin/main")
    if local != distant:
        arreter(f"la préprod locale ({local[:7]}) diffère de GitHub ({distant[:7]}).")
    git(prod, "fetch", "-q", "origin")
    git(prod, "reset", "-q", "--hard", "origin/main")
    print(f"Préprod de référence : {local[:7]} — {git(PREPROD, 'log', '-1', '--format=%s')}")

    # 2. Recopie
    for element in prod.iterdir():
        if element.name in config.EXCLUS_DE_LA_PROD:
            continue
        shutil.rmtree(element) if element.is_dir() else element.unlink()
    for element in PREPROD.iterdir():
        if element.name in config.EXCLUS_DE_LA_PROD or element.name == "__pycache__":
            continue
        cible = prod / element.name
        shutil.copytree(element, cible) if element.is_dir() else shutil.copy2(element, cible)

    # 3. Fichiers propres à la prod
    p = config.ENVIRONNEMENTS["prod"]
    (prod / "CNAME").write_text(p["domaine"] + "\n")
    (prod / "robots.txt").write_text(p["robots"])

    # 4. Indexation
    retirees = 0
    for page in prod.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        nouveau = re.sub(re.escape(config.BALISE_NOINDEX) + r"(<!--.*?-->)?\n?", "", html)
        if nouveau != html:
            retirees += 1
            page.write_text(nouveau, encoding="utf-8")
    print(f"Balise noindex retirée de {retirees} page(s).")

    # 5. Tests en mode prod
    print("Tests en mode prod…")
    res = subprocess.run([sys.executable, str(OUTILS / "verifier.py"), "--env", "prod", str(prod)])
    if res.returncode != 0:
        git(prod, "reset", "-q", "--hard", "origin/main")
        git(prod, "clean", "-qfd")
        arreter("des tests échouent en mode prod (voir ci-dessus). La prod locale a été remise en l'état.")

    git(prod, "add", "-A")
    changements = git(prod, "diff", "--cached", "--stat")
    if not changements:
        print("\nAucune différence avec la prod en ligne : rien à publier.")
        return
    print("\nChangements à publier en prod :\n" + changements)

    if not a.publier:
        print("\nRépétition à blanc terminée : rien n'a été envoyé. Relancer avec --publier après le feu vert.")
        return

    message = (f"Mise en production : {a.resume}\n\n"
               f"Contenu de acc-coaching/preprod@{local[:7]}, validé par Christophe.\n"
               f"Balise noindex retirée, CNAME et robots.txt propres à la prod.\n\n"
               "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    if os.environ.get("CLAUDE_SESSION"):
        message += f"\nClaude-Session: {os.environ['CLAUDE_SESSION']}"
    git(prod, "commit", "-q", "-m", message)
    git(prod, "push", "-q", "origin", "main", capture=False)
    print(f"\nPublié en prod : {git(prod, 'log', '-1', '--format=%h %s')}")


if __name__ == "__main__":
    main()
