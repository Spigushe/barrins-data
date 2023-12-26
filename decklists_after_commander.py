import glob
import os

from mtgdc_aggregator import Aggregator
from mtgdc_decklists import CompareLists, ImportDecks
from mtgdc_clustering import KMeansACP

if __name__ == "__main__":
    for file in glob.glob(os.path.join(".", "*_cluster_*")):
        os.remove(file)

    print(".", "Loading decks")
    liste_decks = ImportDecks.from_directory("./mtgdc_decklists/decklists")
    liste_decks.load_decks(commander=["ertai resurrected"])
    print("\t", f"{len(liste_decks.decklists)} decks loaded")

    print(".", "PCA analysis and KMeans clustering")
    kmeans_with_pca = KMeansACP(liste_decks.decklists, max_clusters=5+1)
    kmeans_with_pca.plot(output="result_plot.pdf")
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
        aggregate.export(f"kmeans_cluster_{k+1}.txt", title=f"Cluster {k+1}")

    print(".", "Comparison table")
    liste_decks = CompareLists.load_decks()
    liste_decks.export("comparison_table.html")
