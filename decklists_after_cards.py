import os

from mtgdc_aggregator import Aggregator
from mtgdc_clustering import KMeansACP
from mtgdc_decklists import CompareLists, ImportDecks

CARDS = ["Underworld Breach", "Stitcher's Supplier"]

if __name__ == "__main__":
    path = "output/" + "".join(filter(str.isalpha, "".join(CARDS).lower()))

    if not os.path.isdir("output"):
        os.mkdir("output")
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))

    print(".", "Loading decks")
    liste_decks = ImportDecks.from_directory("./mtgdc_decklists/decklists")
    liste_decks.load_decks(cards=CARDS)
    print("\t", f"{len(liste_decks.decklists)} decks loaded")

    print(".", "PCA analysis and KMeans clustering")
    kmeans_with_pca = KMeansACP(liste_decks.decklists, max_clusters=5 + 1)
    kmeans_with_pca.plot(output=f"{path}/result_plot.pdf")
    print("\t", f"KMeans: {kmeans_with_pca.nb_clusters} clusters")

    """
    # Still needs to be able to handle card types
    print(".", "Closest cards")
    card_name = str(input("\t Quelle carte? "))
    depth = int(input("\t Combien de cartes? "))
    print(kmeans_with_pca.get_closest_cards(card_name, depth))
    """

    print(".", "Decks per cluster and default decklist")
    for k in sorted(list(set(kmeans_with_pca.labels))):
        decks_label = [deck for deck, _ in kmeans_with_pca.decks_by_label(k)]
        aggregate = Aggregator(decks_label)
        aggregate.aggregate(action=f"Cluster {k+1}")
        aggregate.export(f"{path}/kmeans_cluster_{k+1}.txt", title=f"Cluster {k+1}")

    print(".", "Comparison table")
    liste_decks = CompareLists.load_decks(path)
    liste_decks.export(f"{path}/comparison_table.html")
