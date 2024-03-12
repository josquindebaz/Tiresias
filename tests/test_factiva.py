import glob
import os

from mod.factiva import ParseHtm
from tests.utils import free_directory, delete_directory


def test_can_parse_htm():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
        support_path = "../data/support.publi"
    else:
        directory_path = "tests"
        support_path = "data/support.publi"

    free_directory(directory_path)

    to_parse = os.path.join(directory_path, "factiva/Factiva.htm")
    parser = ParseHtm(to_parse)

    assert len(parser.content) == 40

    parser.get_supports(support_path)

    assert len(parser.unknowns) == 0

    first_key = list(parser.articles.keys())[0]
    first_article = parser.articles[first_key]
    assert first_article['title'] == "Marine Le Pen ambitionne l'indépendance énergétique"
    assert first_article['date'] == '15/03/2022'
    assert first_article['media'] == 'Le Figaro'
    assert first_article['support'] == 'Le Figaro'
    assert first_article['source_type'] == 'Presse nationale'
    assert first_article['root'] == 'FIG'
    assert first_article['text'] == "Marine Le Pen ambitionne l'indépendance énergétique\r\n.\r\nC'EST une riposte pour le moins hardie. Lors d'une conférence de presse consacrée à ses propositions sur l'énergie et le pouvoir d'achat, Marine Le Pen a répondu à ceux de ses adversaires lui ayant intenté le procès d'entretenir une proximité, voire une dépendance, avec le chef de l'État russe Vladimir Poutine. L'entourage d'Emmanuel Macron en tête. «\xa0Il est révoltant que les mondialistes et les fédéralistes européens qui ont mis nos économies sous la dépendance des matières premières, du gaz et du pétrole russes osent accuser les souverainistes d'avoir eu la moindre complaisance avec Vladimir Poutine alors que ce sont eux, et eux seuls, qui sont responsables du pouvoir de Moscou sur l'Europe.\xa0»À son quartier général de campagne, rue Michel-Ange à Paris, la députée du Pas-de-Calais a présenté la guerre en Ukraine et ses conséquences économiques comme autant de révélateurs des «\xa0errements\xa0» du quinquennat finissant. Façon de remettre en selle son duel avec le chef de l'État, quand tous les sondages la donnent de nouveau qualifiée au second tour de la présidentielle. « Sur l'ensemble des sujets clés de cette campagne, le programme de Marine Le Pen attaque frontalement l'échec d'Emmanuel Macron, assure son directeur adjoint de campagne et référent énergie, Jean-Philippe Tanguy. Même leurs solutions portent des visions du monde totalement différentes.\xa0»Le chef de l'État et la Commission européenne sont ainsi condamnés solidairement pour avoir « interdit toute politique de patriotisme économique\xa0» , avoir mis fin à la «\xa0préférence communautaire\xa0» comme avoir «\xa0imposé le choix allemand mélangeant maintien du charbon, énergies intermittentes et dépendance au gaz importé\xa0» plutôt que d'avoir préservé dans le choix d'une politique d'indépendance énergétique grâce au nucléaire.La guerre ukrainienne vient, surtout, valider a posteriori l'intuition des équipes de Marine Le Pen qui, depuis neuf mois, ont fait du pouvoir d'achat leur axe majeur de campagne. Et voit désormais l'inflation comme le meilleur des carburants électoraux . « Notre civilisation ne se limite pas qu'aux enjeux identitaires ou régaliens\xa0», se permet de tacler Marine Le Pen à ceux de ses adversaires, Éric Zemmour en tête, ayant sous-estimé cette thématique.Outre sa proposition phare d'abaisser la TVA à 5,5\xa0% pour l'essence, l'électricité et le gaz, la tête de proue du RN veut supprimer les augmentations de la TICPE consenties par Emmanuel Macron entre 2015 et 2018, tant que le cours du baril sera supérieur à 100 dollars. Deux mesures qui selon ses calculs, devraient réduire de 32 à 50 centimes le prix du litre d'essence à la pompe. Marine Le Pen propose également un prêt pour couvrir l'installation d'un boîtier de conversion à l'éthanol. Autant de mesures financées grâce à une taxe «\xa0exceptionnelle\xa0» sur les superprofits des énergéticiens tels que Total et Engie. Sur l'électricité, Marine Le Pen entend sortir du marché européen libéralisé de l'électricité et veut supprimer l'accès régulé à l'électricité nucléaire (ARENH) tout en arrêtant les subventions aux énergies intermittentes tel que l'éolien.«\xa0Plan Marie Curie\xa0»Pour ces trente prochaines années, c'est sans surprise sur le nucléaire que parie la candidate nationaliste. Avec un nouveau plan de rénovation et de construction de nouvelles centrales baptisé «\xa0plan Marie Curie\xa0»\xa0: réouverture de Fessenheim, prolongement des réacteurs existants jusqu'à 60 ans, construction de 5 paires d'EPR, 5 paires d'EPR2 et installation de petits réacteurs modulaires (SMR) à partir de 2031. «\xa0À partir de 2040, 1\xa0600 MW de puissance nucléaire moyenne devront être installés par an\xa0», ambitionne Marine Le Pen qui espère par ce degré de détail se parer d'une crédibilité supérieure à celle de 2017.Comme ces dernières semaines, Marine Le Pen a rappelé son opposition aux sanctions économique visant la Russie. «\xa0Emmanuel Macron, ses soutiens mais aussi Valérie Pécresse se sont engagés dans une surenchère de sanctions sans se préoccuper de savoir si leurs conséquences ne seraient pas plus terribles pour l'économie française et le pouvoir d'achat de nos compatriotes que sur la Russie\xa0», oppose-t-elle s ans avancer, pour autant, de moyen de pression alternatif face au Kremlin."

    delete_directory("temp")
    os.mkdir("temp")
    parser.write_prospero_files("temp")

    txt_generated = glob.glob("temp/*.txt")
    assert len(txt_generated) == 40
    assert os.path.isfile("temp/FIG20220315A.txt")
    assert os.path.isfile("temp/FIG20220315A.ctx")

    with open("temp/FIG20220315A.ctx", "r", encoding='cp1252') as ctx_test_file:
        ctx_test = ctx_test_file.readlines()
    assert ctx_test[:11] == ['fileCtx0005\n', "Marine Le Pen ambitionne l'indépendance énergétique\n", 'Le Figaro\n', '\n', '\n', '15/03/2022\n',  'Le Figaro\n', 'Presse nationale\n', '\n', '\n', '\n']

    ctx_generated = glob.glob("temp/*.ctx")
    assert len(ctx_generated) == 40

    free_directory("temp")
    delete_directory("temp")
