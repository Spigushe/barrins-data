import os

from mtgdc_aggregator import Aggregator
from mtgdc_clustering import KMeansACP
from mtgdc_decklists import ImportDecks

COMMANDER = "Golos, Tireless Pilgrim"
CARDS = ["Solitude", "White Plume Adventurer"]

if __name__ == "__main__":
    str_joined = ("".join(filter(str.isalpha, COMMANDER + "".join(CARDS)))).lower()
    path = "output/" + str_joined

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
    liste_decks.load_decks(commander=[COMMANDER], cards=CARDS)
    print("\t", f"{len(liste_decks.decklists)} decks loaded")

    print(".", "Aggregating loaded decklists")
    aggregate = Aggregator(liste_decks.decklists, order=3)
    aggregate.aggregate()
    aggregate.export(f"{path}/{str_joined}.txt")

    print(".", "PCA analysis and KMeans clustering")
    kmeans_with_pca = KMeansACP(liste_decks.decklists, max_clusters=3 + 1)
    kmeans_with_pca.plot(output=f"{path}/result_plot.pdf")
    print("\t", f"KMeans: {kmeans_with_pca.nb_clusters} clusters")

    print(".", "Decks per cluster and default decklist")
    for k in sorted(list(set(kmeans_with_pca.labels))):
        decks_label = [deck for deck, _ in kmeans_with_pca.decks_by_label(k)]
        aggregate = Aggregator(decks_label, ordre=3)
        aggregate.aggregate(action=f"Cluster {k+1}")
        aggregate.export(f"{path}/kmeans_cluster_{k+1}.txt", title=f"Cluster {k+1}")
