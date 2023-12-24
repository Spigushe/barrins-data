"""
Module to generate JSON and HTML files of the current banlist.
"""
import argparse
import sys

from mtgdc_banlist import BanlistCompiler

parser = argparse.ArgumentParser(
    prog="create_banlist.py",
    description=(
        "Le fichier permet de compiler les banlists "
        + "présentes dans le dossier `./banlists`"
    ),
    epilog=(
        "Il est possible de contribuer au projet sur GitHub: "
        + "https://github.com/barrins-codex/mtgdc-banlist"
    ),
)

parser.add_argument(
    "--compile-json",
    action="store_true",
    help="Génère la version actuelle de la banlist au format JSON",
)

parser.add_argument(
    "--compile-html",
    action="store_true",
    help="Génère l'historique de la banlist au format HTML",
)

parser.add_argument(
    "--compile-both", action="store_true", help="Génère les fichiers JSON et HTML"
)

parser.add_argument(
    "-o",
    "--output",
    help="Permet d'indiquer le fichier de sortie",
    nargs="?",
    default="",
)


def main(args):
    """
    Procédure pricipale qui gère le retour du parser.

    La procédure appelle la classe ``BanlistCompiler`` pour récupérer
    les informations demandées : soit le fichier JSON, soit le fichier
    HTML, soit les deux.

    Les fichiers sont ensuite créés/modifiés selon le chemin fourni.

    :param args list: Liste des arguments à parser
    """
    args = parser.parse_args(args)

    if not any([args.compile_json, args.compile_html, args.compile_both]):
        parser.print_help()

    banlist = BanlistCompiler()

    if any([args.compile_json, args.compile_both]):
        banlist.get_json_banlist(args.output)

    if any([args.compile_html, args.compile_both]):
        banlist.compile_to_html(args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
