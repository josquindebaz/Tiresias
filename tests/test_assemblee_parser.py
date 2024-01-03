import os

from mod.AssembleeParser import AssembleeParser


def test_parse_ass_7_qe_without_response():
    file_path = "qp/assemblee_leg_07-qe_sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Couste',
                'dept': 'Rhône',
                'dpq': '31/03/1986',
                'dpr': '',
                'groupe': 'Rassemblement pour la République',
                'leg': '7',
                'ministere': 'affaires sociales et emploi',
                'nature': 'Question écrite',
                'num': '80900',
                'pgq': '1145',
                'pgr': '',
                'question': '',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Biologie'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_7_qg():
    file_path = "qp/assemblee_leg_07-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Goeuriot',
                'dept': 'Meurthe-et-Moselle',
                'dpq': '19/12/1985',
                'dpr': '19/12/1985',
                'groupe': 'Communiste',
                'leg': '7',
                'ministere': 'énergie',
                'nature': 'Question au Gouvernement',
                'num': '1510',
                'pgq': '6342',
                'pgr': '6342',
                'question': '',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Entreprises: Meurthe-et-Moselle'}
    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_7_qosd():
    file_path = "qp/assemblee_leg_07-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Douyère',
                'dept': 'Sarthe',
                'dpq': '18/12/1985',
                'dpr': '21/12/1985',
                'groupe': 'Socialiste',
                'leg': '7',
                'ministere': 'budget et consommation',
                'nature': 'Question orale sans débat',
                'num': '954',
                'pgq': '6323',
                'pgr': '6516',
                'question': '',
                'reponse': '',
                'support': 'Journal officiel',
                'title': "Taxe d'habitation et taxes foncieres"}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_8_qe_without_response():
    file_path = "qp/assemblee_leg_08-qe_sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Hardy',
                'dept': 'Charente',
                'dpq': '14/05/1988',
                'dpr': '',
                'groupe': 'Rassemblement pour la République',
                'leg': '8',
                'ministere': 'budget',
                'nature': 'Question écrite',
                'num': '39989',
                'pgq': '2089',
                'pgr': '',
                'question': "M Francis Hardy attire l'attention de M le ministre d'Etat, "
                            "ministre de l'economie, des finances et du budget, sur "
                            "l'interpretation restrictive qui est faite par les services des "
                            'impots de la circulaire LC 210/CD 410 du 7 fevrier 1980. Cette '
                            "circulaire stipule que « le paiement exige des debiteurs d'impot "
                            "de l'Etat, qui disposent par ailleurs d'une creance certaine et "
                            "exigible non reglee par l'Etat, fera systematiquement l'objet de "
                            "facilites de reglement jusqu'a la date du paiement attendu de "
                            "l'Etat ». Certains membres de SCP d'analyses medicales, qui "
                            'avaient beneficie ces dernieres annees de facilites de '
                            'reglement, se les sont vu refuser recemment au motif que la '
                            "circulaire fait reference aux creances de l'Etat stricto sensu "
                            'et non sur des etablissements publics administratifs, tels que '
                            'les hopitaux publics. Cette mutation, qui aboutit a une double '
                            "penalisation du contribuable de bonne foi, est d'autant plus "
                            'genante que les sommes dues depassent dans certains cas tres '
                            'sensiblement le montant des impots exigibles. Il lui demande, '
                            "dans ces conditions, s'il compte donner des directives pour "
                            'rendre la circulaire susvisee applicable aux creances non '
                            'reglees par les etablissements publics administratifs. ',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Paiement'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_8_qe_with_response():
    file_path = "qp/assemblee_leg_08-qe_ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Delehedde',
                'dept': 'Pas-de-Calais',
                'dpq': '25/04/1988',
                'dpr': '09/05/1988',
                'groupe': 'Socialiste',
                'leg': '8',
                'ministere': 'éducation nationale',
                'nature': 'Question écrite',
                'num': '39461',
                'pgq': '1723',
                'pgr': '2043',
                'question': "M Andre Delehedde appelle l'attention de M le ministre de "
                            "l'education nationale sur la maniere dont sont effectuees les "
                            "mutations des enseignants de l'education physique et sportive. "
                            "D'une part, bon nombre de postes vacants n'ont pas ete mis au "
                            "mouvement, d'autre part, des postes ont ete mis a la disposition "
                            'des recteurs en dehors de toute consultation des commissions '
                            'paritaires. Il lui demande de bien vouloir verifier que les '
                            "regles normales de mutations des enseignants de l'education "
                            "physique et sportive soient respectees, a savoir : qu'il n'y ait "
                            'pas de postes bloques ; que soit applique strictement le decret '
                            "no 87-161 du 5 mars 1987 fixant l'attribution et le retrait du "
                            "statut d'athlete de haut niveau. ",
                'reponse': 'Reponse. - disciplines, le mouvement national des enseignants '
                           "fait l'objet d'une etude prealable visant, d'une part a "
                           "equilibrer la repartition des enseignants sur l'ensemble du "
                           "territoire, d'autre part, a eliminer les surnombres qui ont pu "
                           'etre constates dans certaines academies. Est ainsi notamment '
                           "prise en compte la necessite d'eviter que les academies "
                           "deficitaires du Nord ne perdent pas plus d'enseignants qu'elles "
                           "n'en recoivent ainsi que la necessite de conserver dans chaque "
                           'academie suffisamment de postes pour les enseignants qui sont en '
                           "attente d'une affectation definitive. Des dispositions "
                           'particulieres ont ainsi du etre prises lors du mouvement realise '
                           'au titre de la rentree 1987 pour assurer une repartition '
                           "equilibree des enseignants d'education physique et sportive sur "
                           'le territoire. Toutefois, afin de regler certaines situations '
                           'familiales particulierement difficiles, quelques mises a '
                           'disposition des recteurs ont ete effectuees apres le mouvement, '
                           'en nombre extremement reduit, en tenant compte de la situation '
                           "des academies d'accueil et de depart, pour ne pas reintroduire de "
                           'desequilibre. Quelques mises a disposition ont ete egalement '
                           "accordees a des sportifs de haut niveau afin qu'ils soient places "
                           'dans les meilleures conditions possibles pour exercer leur '
                           'activite. En toute hypothese, ces decisions ne constituent '
                           "nullement des mutations au sens defini par l'article 60, de la "
                           'loi no 84-16 du 11 janvier 1984 portant dispositions statutaires '
                           "relatives a la fonction publique de l'Etat. En effet, il s'agit "
                           "exclusivement d'affectations provisoires dont la duree est "
                           'limitee a une annee scolaire et qui se trouvent automatiquement '
                           "remises en cause a l'issue de cette periode. ",
                'support': 'Journal officiel',
                'title': 'Personnel'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_8_qg():
    file_path = "qp/assemblee_leg_08-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Cassaing',
                'dept': 'Corrèze',
                'dpq': '05/06/1986',
                'dpr': '05/06/1986',
                'groupe': 'Socialiste',
                'leg': '8',
                'ministere': 'recherche',
                'nature': 'Question au Gouvernement',
                'num': '110',
                'pgq': '1684',
                'pgr': '1684',
                'question': '</TD><TD colspan=2 align=left>\n<COMPREP></COMPREP>',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Etablissements'}
    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_8_qosd():
    file_path = "qp/assemblee_leg_08-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Royer',
                'dept': 'Indre-et-Loire',
                'dpq': '17/12/1986',
                'dpr': '20/12/1986',
                'groupe': 'Non-Inscrit',
                'leg': '8',
                'ministere': 'fonction publique et plan',
                'nature': 'Question orale sans débat',
                'num': '172',
                'pgq': '7696',
                'pgr': '7841',
                'question': '',
                'reponse': '</TD><TD colspan=2 align=left>\n<COMPREP></COMPREP>',
                'support': 'Journal officiel',
                'title': 'Plans'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_8_qosd_retracted():
    file_path = "qp/assemblee_leg_08-qosd-ret.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Jacquot',
                'dept': 'Vosges',
                'dpq': '03/04/1987',
                'dpr': '',
                'groupe': 'Rassemblement pour la République',
                'leg': '8',
                'ministere': 'santé et famille',
                'nature': 'Question orale sans débat',
                'num': '176',
                'pgq': '12',
                'pgr': '',
                'question': '',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Frais de cure'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_9_qe_with_response():
    file_path = "qp/assemblee_leg_09-qe_ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Ligot',
                'dept': 'Maine-et-Loire',
                'dpq': '15/03/1993',
                'dpr': '29/03/1993',
                'groupe': 'Union pour la démocratie française',
                'leg': '9',
                'ministere': 'affaires sociales et intégration',
                'nature': 'Question écrite',
                'num': '67760',
                'pgq': '891',
                'pgr': '1098',
                'question': "M Maurice Ligot appelle l'attention de M le ministre des "
                            "affaires sociales et de l'integration sur l'aide forfaitaire en "
                            'faveur de la vie autonome a domicile des personnes handicapees '
                            'creee par arrete du 29 janvier 1993. Il a ete prevu que cette '
                            "aide soit accordee aux seuls titulaires de l'allocation aux "
                            'adultes handicapes. Une distorsion est ainsi etablie entre les '
                            'handicapes et les personnes agees, aux depens de ces dernieres, '
                            'alors meme que celles-ci vivent dans une grande majorite de '
                            "facon autonome a leur domicile. Il lui demande d'etendre le "
                            "benefice de l'aide en faveur de la vie autonome a domicile aux "
                            "titulaires de l'allocation supplementaire du Fonds national de "
                            'solidarite. ',
                'reponse': "Reponse. - L'allocation aux adultes handicapes (AAH), prestation "
                           'non contributive, est un revenu minimum garanti par la '
                           'collectivite nationale a toute personne reconnue handicapee par '
                           "la COTOREP. De ce fait, elle n'est attribuee que lorsque la "
                           'personne handicapee ne peut pretendre a un avantage de vieillesse '
                           "ou d'invalidite d'un montant au moins egal a ladite allocation, "
                           'soit 3 130 francs au 1er janvier 1993. Le caractere subsidiaire '
                           "de l'AAH a ete confirme sans ambiguite par l'article 98 de la loi "
                           "de finances pour 1983 qui a modifie l'article 35 de la loi no "
                           "75-534 du 30 juin 1975 d'orientation en faveur des personnes "
                           "handicapees (devenu l'article L 821-1 du code de la securite "
                           "sociale). Par ailleurs, une aide forfaitaire d'un montant de 501 "
                           'francs, en faveur de la vie autonome a domicile des personnes '
                           'adultes handicapees a ete creee par arrete du 29 janvier 1993 (JO '
                           'du 31 janvier 1993). Peuvent pretendre a cette aide, les '
                           'personnes handicapees qui remplissent simultanement les '
                           "conditions suivantes : 1) presenter un taux d'incapacite ouvrant "
                           "droit au benefice a l'allocation aux adultes handicapes instituee "
                           "par l'article L 821-1 du code de la securite sociale ; 2) "
                           "percevoir l'allocation aux adultes handicapes mentionnee "
                           "ci-dessus a taux plein, ou en complement d'un avantage de la "
                           "vieillesse ou d'invalidite ou d'une rente d'accident du travail ; "
                           "3) beneficier d'une aide personnelle au logement ; 4) disposer "
                           "d'un logement independant et y vivre, seul ou en couple. Il n'est "
                           "pas prevu a l'heure actuelle d'etendre le benefice de cette aide "
                           "a d'autres categories de personnes. Par ailleurs, l'Assemblee "
                           'nationale a adopte en premiere lecture un projet de loi prevoyant '
                           'une prise en charge des personnes agees dependantes. Dans ce '
                           "cadre il est prevu l'instauration d'une allocation autonomie et "
                           'dependance qui portera le minimum de leurs ressources, en '
                           'incluant le minimum vieillesse, a 7 200 francs par mois. ',
                'support': 'Journal officiel',
                'title': 'Allocations et ressources'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_9_qg():
    file_path = "qp/assemblee_leg_09-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Dosière',
                'dept': 'Aisne',
                'dpq': '17/12/1992',
                'dpr': '17/12/1992',
                'groupe': 'Socialiste',
                'leg': '9',
                'ministere': 'enseignement technique',
                'nature': 'Question au Gouvernement',
                'num': '1480',
                'pgq': '7311',
                'pgr': '7311',
                'question': '</TD><TD colspan=2 align=left>\n<COMPREP></COMPREP>',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Baccalaureat'}
    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_9_qosd():
    file_path = "qp/assemblee_leg_09-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Raoult',
                'dept': 'Seine-Saint-Denis',
                'dpq': '13/05/1992',
                'dpr': '16/05/1992',
                'groupe': 'Rassemblement pour la République',
                'leg': '9',
                'ministere': 'environnement',
                'nature': 'Question orale sans débat',
                'num': '560',
                'pgq': '1130',
                'pgr': '1262',
                'question': '',
                'reponse': '</TD><TD colspan=2 align=left>\n<COMPREP></COMPREP>',
                'support': 'Journal officiel',
                'title': 'Lutte et prevention : Seine-Saint-Denis'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_10_qe_with_response():
    file_path = "qp/assemblee_leg_10-qe_ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Marlin',
                'dept': 'Essonne',
                'dpq': '31/03/1997',
                'dpr': '21/04/1997',
                'groupe': 'Rassemblement pour la République',
                'leg': '10',
                'ministere': 'éducation nationale, enseignement supérieur et recherche',
                'nature': 'Question écrite',
                'num': '50237',
                'pgq': '1601',
                'pgr': '2094',
                'question': "M. Franck Marlin souhaite attirer l'attention de M. le ministre "
                            "de l'education nationale, de l'enseignement superieur et de la "
                            'recherche sur la situation et la prise en compte des problemes '
                            'specifiques des enfants dysphasiques et dyslexiques. Certains '
                            "parents, desireux d'inculquer a leurs enfants le savoir minimum "
                            "pour lire, ecrire et compter, denoncent l'absence prejudiciable "
                            'de structures educatives adaptees. De nombreux cas ont demontre '
                            "que ce type d'enfant en difficulte pouvait ne pas rester "
                            'illettre. Aussi lui demande-t-il de bien vouloir lui indiquer '
                            "les differentes mesures qu'il entend mettre en oeuvre pour "
                            'remedier a cette lacune. ',
                'reponse': "Le ministre de l'education nationale, de l'enseignement superieur "
                           'et de la recherche reserve une attention toute particuliere a la '
                           "situation des enfants eprouvant des difficultes d'apprentissage "
                           'du langage oral et ecrit. La note de service no 90-23 du 25 '
                           'janvier 1990 adressee aux autorites academiques preconise un '
                           'certain nombre de mesures en faveur de ces eleves, et plus '
                           'particulierement une sensibilisation des enseignants aux '
                           'problemes des enfants dyslexiques. Ce texte insiste notamment sur '
                           "la necessite « d'un depistage precoce des elements revelateurs "
                           'des troubles des apprentissages necessitant un diagnostic et '
                           "d'une pedagogie differenciee adaptee aux besoins de ces eleves ». "
                           'En matiere de formation des enseignants, deux options du '
                           "certificat d'aptitude aux actions pedagogiques specialisees "
                           "d'adaptation et d'integration scolaires (CAPSAIS) comprennent "
                           "dans leur programme, l'une la problematique des apprentissages "
                           "(option E : enseignants specialises charges de l'enseignement et "
                           "de l'aide pedagogique aupres des enfants en difficultes a l'ecole "
                           "preelementaire et elementaire), et l'autre des informations sur "
                           'le dysfonctionnement du langage oral et ecrit, notamment sur le '
                           'probleme des dyslexies-dysorthographies (option G : enseignants '
                           'specialises charges de reeducation). Les centres nationaux '
                           "d'etudes et de formation de Beaumont-sur-Oise et de Suresnes "
                           'organisent regulierement des stages de formation destines aux '
                           'personnels concernes par la situation de ces enfants. Enfin, un '
                           "groupe de travail sur les troubles du langage vient d'etre "
                           "constitue dans le cadre du Centre technique national d'etudes et "
                           'de recherches sur les handicaps et inadaptations (CTNERHI). Le '
                           "ministre de l'education nationale, de l'enseignement superieur et "
                           'de la recherche attend avec interet le resultat des travaux de ce '
                           "groupe d'experts. ",
                'support': 'Journal officiel',
                'title': 'Dyslexie et dysphasie'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_10_qosd():
    file_path = "qp/assemblee_leg_10-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Cova',
                'dept': 'Seine-et-Marne',
                'dpq': '19/02/1997',
                'dpr': '19/02/1997',
                'groupe': 'Rassemblement pour la République',
                'leg': '10',
                'ministere': 'environnement',
                'nature': 'Question orale sans débat',
                'num': '1340',
                'pgq': '1091',
                'pgr': '1035',
                'question': "M. Charles Cova souhaite attirer l'attention de Mme le ministre "
                            "de l'environnement sur la situation que connait le nord de la "
                            'Seine-et-Marne et plus particulierement sa 7e circonscription. '
                            "Avec une carriere d'extraction de gypse, un centre "
                            "d'enfouissement technique, d'importantes lignes a haute tension, "
                            'les habitants de cette region, ainsi que leurs elus, ont de quoi '
                            "s'inquieter. A propos du centre d'enfouissement de Villeparisis, "
                            "la loi du 13 juillet 1992 prevoit et assure le financement d'une "
                            "nouvelle politique d'elimination de dechets menagers. "
                            'Malheureusement, ce texte est inapplicable. Puisque ce systeme '
                            'est impossible a mettre en oeuvre, il conviendrait soit de '
                            'modifier la loi, soit de trouver un nouveau mecanisme '
                            "susceptible, lui, d'etre applicable. En ce qui concerne les "
                            "lignes a haute tension, il s'agit d'un projet visant a regrouper "
                            'des lignes electriques qui preoccupe les riverains de la commune '
                            "de Pomponne et auquel il est important d'apporter une solution "
                            'satisfaisante. Cette solution pourrait etre envisagee par la '
                            "realisation d'un nouveau trace. Financierement et techniquement, "
                            'ce contournement ne pose de difficultes majeures. Le seul '
                            "obstacle concerne l'eventuel declassement d'une partie du site "
                            'inscrit. Sur ces deux dossiers, dont il est deja saisi, il '
                            'souhaiterait connaitre son sentiment et ses intentions. ',
                'reponse': 'Mme le president. M. Charles Cova a presente une question no '
                           '1340. <BR>  La parole est a M. Charles Cova, pour exposer sa '
                           "question. <BR>  M. Charles Cova. Je souhaite attirer l'attention "
                           "de Mme le ministre de l'environnement sur la situation de "
                           'communes de ma circonscription, Villeparisis et Pomponne. <BR>  '
                           "La premiere beneficie, si l'on peut dire, de la presence sur son "
                           "territoire d'un centre d'enfouissement technique charge de "
                           'stocker des dechets industriels. Une telle installation suscite '
                           "de legitimes preoccupations. Outre les nuisances qu'elle genere "
                           'et qui sont prejudiciables aux riverains, des evenements survenus '
                           'recemment sont inquietants. <BR>  Dans ce centre, le 17 septembre '
                           "1996, un incendie s'est declare, detruisant un stock important "
                           "d'amiante. Meme si cet incendie a ete maitrise par le personnel "
                           "du centre, on ne peut que s'en alarmer. <BR>  Il semblerait "
                           'egalement que des produits contenant du plomb aient ete enfouis '
                           'sans precaution a moins de cinquante metres de la Dhuis qui '
                           'constitue, vous le savez, une canalisation essentielle pour '
                           "l'alimentation en eau potable de Paris. <BR>  Ces elements sont "
                           "d'autant plus inquietants que, le 22 octobre 1996, lors d'une "
                           "visite, l'inspecteur des installations classees de la DRIRE, la "
                           "direction regionale de l'industrie, de la recherche et de "
                           "l'environnement, a constate que certaines prescriptions de "
                           "l'arrete du 20 juillet 1992 n'etaient pas respectees et a propose "
                           "au prefet de Seine-et-Marne de mettre l'exploitant en demeure de "
                           "s'y conformer. <BR>  Je sais que l'arrete du prefet a ete signe, "
                           'mais je pense que ces signaux sont suffisamment forts pour que '
                           "meme le ministere de l'environnement prenne conscience de la "
                           "situation. <BR>  Toujours en ce qui concerne l'elimination des "
                           'dechets et, surtout, son financement, je renouvelle mon regret de '
                           'voir sans suite le dispositif prevu par la loi du 13 juillet '
                           '1993, qui prevoyait de creer des fonds de solidarite au profit '
                           'des communes sur le territoire desquelles est situee une '
                           'installation de stockage de dechets industriels. <BR>  A ce jour, '
                           "l'interet de cette reglementation n'est toujours pas concretise. "
                           '<BR>  Le second point sur lequel je tenais a sensibiliser le '
                           'ministre concerne les lignes a haute tension qui traversent la '
                           "commune de Pomponne. Il s'agit de lignes qui ont ete construites "
                           "a la fin des annees 50. <BR>  Le projet d'EDF consiste a "
                           'regrouper ces lignes electriques sur des pylones communs, mais '
                           "elles passeraient toujours au-dessus d'habitations. Profitant de "
                           'cette operation de regroupement, on pourrait etudier le '
                           "deplacement de ce couloir de lignes pour l'eloigner de la zone "
                           'habitee. <BR>  Une hypothese a ete soumise a M. le prefet de '
                           'Seine-et-Marne. Elle comprendrait un trace longeant le parc du '
                           'chateau de Pomponne qui est, il est vrai, un site inscrit. <BR>  '
                           "Malgre cela, il me semble essentiel d'etudier ce projet de "
                           "nouveau trace en concertation avec l'architecte des Batiments de "
                           'France. <BR>  Vous comprendrez a quel point ma circonscription '
                           "est affectee sur le plan de l'environnement lorsque vous saurez "
                           'que nous avons a deplorer en sus le bruit genere par '
                           "l'agrandissement de Roissy, l'elargissement de l'A 104, le "
                           'passage du TGV-Est, sans compter celui provenant de '
                           "l'exploitation du gypse a ciel ouvert. <BR>  Dans quelle mesure "
                           'le Gouvernement pourra-t-il, sur les deux points que je viens '
                           "d'evoquer, apporter sa contribution et son soutien, avec le souci "
                           'permanent de venir en aide aux populations concernees ? <BR>  Mme '
                           'le president. La parole est a M. le ministre des relations avec '
                           'le Parlement. <BR>  M. Roger Romani, ministre des relations avec '
                           "le Parlement.  Monsieur le depute, Mme Corinne Lepage m'a prie de "
                           'vous repondre sur les deux points que vous avez evoques: le '
                           "centre d'enfouissement de Villeparisis et le projet de "
                           "regroupement des lignes electriques a Pomponne. <BR>  S'agissant "
                           "du premier point, le centre d'enfouissement de Villeparisis, "
                           'exploite par la societe France Dechets, est dedie au stockage de '
                           'dechets industriels speciaux. Une alveole de ce centre continue '
                           'cependant a recevoir, a titre gracieux, les dechets menagers de '
                           'Villeparisis et de deux communes limitrophes. Cette alveole '
                           "arrive a saturation et l'exploitant n'envisage pas d'en ouvrir "
                           'une nouvelle. Il a donc propose des solutions de remplacement aux '
                           'communes concernees. Ces solutions conduisent inevitablement a '
                           'une charge nouvelle pour ces communes, compte tenu des conditions '
                           "particulieres actuelles d'elimination, a savoir la gratuite. "
                           '<BR>  Le produit de la taxe instauree par la loi du 13 juillet '
                           "1992 n'est pas destine a subventionner le cout de ce service. En "
                           'revanche, si les communes concernees decidaient de mettre en '
                           'place des equipements permettant de reduire le flux de dechets a '
                           'stocker par la collecte selective, les centres de tri, les '
                           'dechetteries ou tout autre equipement, elles pourraient '
                           "beneficier d'aides sur le produit de cette taxe et du concours "
                           "d'organismes come Eco-Emballages et Adelphie. <BR>  Sur le second "
                           'point, concernant le regroupement de lignes electriques a '
                           'Pomponne, les travaux de reconstruction des lignes de 400 et de '
                           '225 kilovolts de Morebras a Villevaude et de la ligne de 225 '
                           'kilovolts de Vaires a Villaude ont ete soumis a enquete publique '
                           'et ont donne lieu a un avis favorable du commissaire-enqueteur le '
                           '26 aout 1996. <BR>  La concertation entre EDF et les differentes '
                           'parties interessees au projet, notamment les habitants du '
                           "quartier de la Pomponnette, s'est toutefois poursuivie. Les "
                           "riverains proposent un nouveau trace qui permettrait d'eviter les "
                           'zones baties. Si cette solution est interessante du point de vue '
                           "de l'environnement, elle a toutefois l'inconvenient d'imposer un "
                           "passage d'une largeur de 120 metres sur 1,5 kilometre dans le "
                           "site inscrit du parc du chateau de Pomponne. <BR>  L'instruction "
                           'du dossier est toujours en cours car les implications juridiques '
                           "d'une eventuelle procedure de desinscription de l'espace protege "
                           'est delicate a mettre en oeuvre. Si ce trace est retenu, il '
                           'conviendra de proceder a une nouvelle enquete publique. <BR>  '
                           'Tels sont, monsieur le depute, les elements de reponse que Mme le '
                           "ministre de l'environnement est a ce jour en mesure de vous "
                           'donner sur ces dossiers. <BR>  Mme le president. La parole est a '
                           'M. Charles Cova. <BR>  M. Charles Cova. Je vous remercie, '
                           "monsieur le ministre, de vous etre fait l'interprete de Mme "
                           "Corinne Lepage et de m'avoir communique tous ces elements de "
                           "reponse eminemment administratifs. Il n'empeche: le probleme de "
                           'Villeparisis reste pendant et, sous le pretexte de donner a cette '
                           'commune et a une ou deux communes environnantes la possibilite de '
                           "deverser des detritus d'origine alimentaire dans cette decharge, "
                           'on y enfouit des dechets de classe 1 prejudiciables a la sante '
                           "des riverains. J'exprime ici la volonte des habitants de ces "
                           "communes d'etre vigilants a l'avenir. ",
                'support': 'Journal officiel',
                'title': 'Protection'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_10_qosd_without_response():
    file_path = "qp/assemblee_leg_10-qosd-sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Brard',
                'dept': 'Seine-Saint-Denis',
                'dpq': '16/04/1997',
                'dpr': '',
                'groupe': 'Communiste',
                'leg': '10',
                'ministere': 'santé et sécurité sociale',
                'nature': 'Question orale sans débat',
                'num': '1472',
                'pgq': '2505',
                'pgr': '',
                'question': "M. Jean-Pierre Brard attire l'attention de M. le secretaire "
                            "d'Etat a la sante et a la securite sociale sur la situation des "
                            'hopitaux publics de Seine-Saint-Denis qui devient tres '
                            'preoccupante du fait notamment des reductions des dotations '
                            'financieres. A Montreuil, le centre hospitalier intercommunal '
                            'Andre-Gregoire est ponctionne de trois manieres differentes. '
                            "Tout d'abord par le redeploiement national des credits : ce "
                            "dispositif ampute de 260 millions de francs l'enveloppe de la "
                            'region Ile-de-France. Le departement y participe a hauteur de 24 '
                            'millions de francs, il ampute le budget du centre hospitalier '
                            'intercommunal Andre-Gregoire de 3,2 millions de francs. Il est '
                            'ensuite touche par le redeploiement au niveau regional de '
                            'credits du secteur sanitaire sur le secteur medico-social au '
                            'titre de la politique du handicap adulte : ce redeploiement '
                            "s'exerce a hauteur de 0,1 % de l'enveloppe, soit, pour le "
                            'departement de la Seine-Saint-Denis, 2,8 millions de francs. Il '
                            'est enfin concerne par la suppression des marges de manoeuvre '
                            'regionales et departementales qui a conduit la region '
                            'Ile-de-France a creer un fonds de compensation finance par les '
                            'hopitaux eux-memes, ce qui represente un prelevement de 2 '
                            'millions de francs pour le centre hospitalier intercommunal '
                            "Andre-Gregoire. Cette accumulation d'amputations budgetaires "
                            'menace la continuite des soins et la mission de service public, '
                            'cela en totale opposition avec la volonte affirmee de resorber '
                            'la fracture sociale. Il lui demande en consequence quels '
                            'correctifs sont envisages pour maintenir en francs constants la '
                            'dotation du centre hospitalier intercommunal Andre Gregoire. ',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Centres hospitaliers'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_10_qg():
    file_path = "qp/assemblee_leg_10-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Meylan',
                'dept': 'Haute-Savoie',
                'dpq': '17/04/1997',
                'dpr': '17/04/1997',
                'groupe': 'Union pour la démocratie française et du Centre',
                'leg': '10',
                'ministere': 'éducation nationale, enseignement supérieur et recherche',
                'nature': 'Question au Gouvernement',
                'num': '2412',
                'pgq': '2552',
                'pgr': '2552',
                'question': 'M. le president. La parole est a M. Michel Meylan. <BR>  M. '
                            "Michel Meylan. Ma question s'adresse a M. le ministre de "
                            "l'education nationale, de l'enseignement superieur et de la "
                            "recherche; elle porte sur la diffusion aupres d'etablissements "
                            "scolaires d'une brochure intitulee Education, alphabetisation et "
                            "civilisation emanant de l'Eglise de scientologie, mouvement "
                            'reconnu comme sectaire. <BR>  Cette plaquette invite les '
                            'enseignants a prendre connaissance des methodes mises au point '
                            "par cette secte pour lutter contre l'echec scolaire. Cette "
                            "methode d'infiltration presente un tres grave danger pour notre "
                            'jeunesse, car ces documents risquent de se retrouver en libre '
                            'acces dans les centres de documentation de nos colleges et de '
                            'nos lycees. Cette campagne semble cibler les etablissements ou '
                            "la proportion d'eleves en difficulte est importante. <BR>  Nous "
                            "ne pouvons tolerer, monsieur le ministre, qu'une telle "
                            'propagande puisse se developper impunement au sein de notre '
                            'systeme educatif et je vous demande quelles mesures vous comptez '
                            'mettre en oeuvre pour faire cesser cette campagne, mais aussi '
                            'pour sensibiliser nos jeunes aux dangers que representent les '
                            'sectes. (Applaudissements sur plusieurs bancs du groupe de '
                            "l'Union pour la democratie francaise et du Centre et du groupe "
                            'du Rassemblement pour la Republique.)  <BR>  M. le president. La '
                            "parole est a M. le ministre de l'education nationale, de "
                            "l'enseignement superieur et de la recherche. <BR>  M. Francois "
                            "Bayrou, ministre de l'education nationale, de l'enseignement "
                            'superieur et de la recherche.  Monsieur Meylan, je suis '
                            "convaincu, comme vous, qu'il est de la responsabilite de "
                            "l'education nationale - et c'est l'une de ses premieres "
                            'responsabilites - de lutter contre la proliferation des sectes, '
                            "contre leur penetration et contre la progression de l'esprit "
                            'sectaire dans la societe francaise et en particulier chez les '
                            'enfants. <BR>  M. Jean-Pierre Brard et M. Jean Tardito. Tres '
                            "bien ! <BR>  M. le ministre de l'education nationale, de "
                            "l'enseignement superieur et de la recherche. La semaine "
                            "derniere, des que j'ai ete informe, en particulier par vos "
                            "soins, de l'envoi de cette brochure, j'ai indique a tous les "
                            "directeurs et a tous les chefs d'etablissement qu'il convenait "
                            'immediatement de la reperer, de la supprimer et, naturellement '
                            'de la mettre hors de portee des eleves et des enseignants. '
                            '<BR>   Plus largement, pour lutter contre les sectes, le '
                            "controle de l'obligation de scolarite, issu de la loi de 1882, "
                            'et eventuellement son amelioration... <BR>  M. Jean-Pierre '
                            "Brard. Tres bien ! <BR>  M. le ministre de l'education "
                            "nationale, de l'enseignement superieur et de la recherche. ... "
                            'me semblent etre une arme tout a fait essentielle. <BR>  Je suis '
                            "attache, comme vous l'etes, a l'idee que l'education nationale "
                            "ne doit montrer aucune complaisance et aucun laxisme a l'egard "
                            "des sectes. (Applaudissements sur les bancs du groupe de l'Union "
                            'pour la democratie francaise et du Centre et du groupe du '
                            'Rassemblement pour la Republique et sur quelques bancs du groupe '
                            'communiste.) ',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Etablissements'}
    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_11_qosd():
    file_path = "qp/assemblee_leg_11-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Bricq',
                'dept': 'Seine-et-Marne',
                'dpq': '01/10/1997',
                'dpr': '08/10/1997',
                'groupe': 'Socialiste',
                'leg': '11',
                'ministere': 'éducation nationale, recherche et technologie',
                'nature': 'Question orale sans débat',
                'num': '7',
                'pgq': '3556',
                'pgr': '3647',
                'question': "<html>Mme Nicole Bricq attire l'attention de M. le ministre de "
                            "l'éducation nationale, de la recherche et de la technologie sur "
                            'le problème des maîtres auxiliaires dont les conditions de '
                            'réemploi ont été définies par la circulaire du 18 juillet '
                            'dernier. Tous les maîtres auxiliaires, qui ont été employés en '
                            "1996-1997 ou qui n'ont pas obtenu de poste cette année-là, alors "
                            "qu'ils étaient en poste en 1995-1996, devaient être recrutés "
                            'quelle que soit leur ancienneté. Cette décision, dont elle se '
                            'félicite, met fin à une situation intolérable de précarité des '
                            'maîtres auxiliaires. Cet effort considérable conduit néanmoins à '
                            'un effet pervers dans la réalité. En effet, les rectorats ont '
                            'reçu la directive de réemployer les maîtres auxiliaires. Mais '
                            "quand ceux-ci n'existent pas dans certaines disciplines, les "
                            "chefs d'établissement ne peuvent faire appel à des contractuels. "
                            "C'est ainsi que pour des enseignements très spécifiques, "
                            'notamment dans des lycées professionnels, comme la céramique au '
                            'lycée du Gué-à-Tresmes à Congis-sur-Thérouanne ou des '
                            "enseignements comme celui de l'espagnol, il n'y a pas, en regard "
                            'des besoins, les ressources en maîtres auxiliaires. Ainsi, ces '
                            'deux disciplines ne peuvent-elles être assurées. De nombreux cas '
                            'de ce type existent en Seine-et-Marne. Il est bien '
                            "compréhensible qu'après avoir réemployé tous les maîtres "
                            'auxiliaires, on ne puisse réamorcer le système. Cependant, elle '
                            "lui demande les dispositions qu'il envisage de prendre pour que, "
                            "dans ces disciplines très précises, l'enseignement puisse être "
                            'assuré aux élèves.</html> ',
                'reponse': '<html>M. le président. Mme Nicole Bricq a présenté une question, '
                           "n° 7, ainsi rédigée: <BR>  «Mme Nicole Bricq attire l'attention "
                           "de M. le ministre de l'éducation nationale, de la recherche et de "
                           'la technologie sur le problème des maîtres auxiliaires, dont les '
                           'conditions de réemploi ont été définies par la circulaire du 18 '
                           'juillet dernier. Tous les maîtres auxiliaires qui ont été '
                           "employés en 1996-1997, ou qui n'ont pas obtenu de poste cette "
                           "année-là alors qu'ils étaient en poste en 1995-1996, devaient "
                           'être recrutés quelle que soit leur ancienneté. Cette décision, '
                           'dont elle se félicite, met fin à une situation intolérable de '
                           'précarité des maîtres auxiliaires. Cet effort considérable '
                           'conduit néanmoins à un effet pervers dans la réalité. En effet, '
                           'les rectorats ont reçu la directive de réemployer les maîtres '
                           "auxiliaires. Mais quand ceux-ci n'existent pas dans certaines "
                           "disciplines, les chefs d'établissement ne peuvent faire appel à "
                           "des contractuels. C'est ainsi que, pour des enseignements très "
                           'spécifiques, notamment dans les lycées professionnels, comme la '
                           'céramique au lycée du Gué-à-Tresmes, à Congis-sur-Thérouanne, ou '
                           "des enseignements comme celui de l'espagnol, il n'y a pas, au "
                           'regard des besoins, les ressources en maîtres auxiliaires. Ainsi '
                           'ces deux disciplines ne peuvent-elles être assurées. De nombreux '
                           'cas de ce type existent en Seine-et-Marne. Il est bien '
                           "compréhensible qu'après avoir réemployé tous les maîtres "
                           'auxiliaires on ne puisse réamorcer le système. Cependant, elle '
                           "lui demande les dispositions qu'il envisage de prendre pour que, "
                           "dans ces disciplines très précises, l'enseignement puisse être "
                           'assuré aux élèves.» <BR>  La parole est à Mme Nicole Bricq, pour '
                           'exposer sa question. <BR>  Mme Nicole Bricq. Monsieur le ministre '
                           "de l'éducation nationale, de la recherche et de la technologie, "
                           'vous avez, par la circulaire du 18 juillet dernier, décidé des '
                           "conditoins de réemploi des maîtres auxiliaires. C'est ainsi que "
                           'tous les maîtres auxiliaires employés en 1996-1997 ou, à défaut, '
                           "l'année précédente, ont pu, quelle que soit leur ancienneté, "
                           'retrouver un poste à la rentrée. On ne peut que se féliciter de '
                           'cette mesure qui met fin à une situation de précarité '
                           "intolérable. <BR>  Toutefois, comme toujours lorsqu'il s'agit de "
                           "mesures générales, l'application de cette circulaire a donné lieu "
                           'à des effets pervers, qui se font sentir quelques semaines après '
                           "la rentrée. Les rectorats ont bien reçu l'instruction de "
                           "réemploi, mais il se trouve qu'il n'existait pas de postes de "
                           'maîtres auxiliaires dans certaines disciplines très spécifiques '
                           'et même pour certains enseignements généraux. Or les chefs '
                           "d'établissement ne peuvent faire appel à des contractuels. C'est "
                           'ainsi que, dans ma circonscription, au lycée professionnel du '
                           "Gué-à-Tresmes, l'enseignement de la céramique ne peut "
                           "actuellement être assuré. Il en va de même pour l'enseignement de "
                           "l'espagnol dans un certain nombre d'établissements, et le cas de "
                           "la Seine-et-Marne n'est certainement pas unique. Dans ces "
                           'disciplines, les ressources en maîtres auxiliaires, ne '
                           "correspondent pas aux besoins. <BR>  Je comprends bien qu'après "
                           'avoir réemployé tous les maîtres auxiliaires, on ne puisse pas, '
                           'en quelque sorte, réamorcer la pompe, car on se retrouverait, '
                           'dans quelques années, face à une situation comparable à celle que '
                           'vous avez voulu résorber, avec notre appui. Mais dans les '
                           'disciplines très spécifiques ou les enseignements généraux que '
                           "j'ai cités, quelles dispositions envisagez-vous de prendre pour "
                           "que l'enseignement soit assuré aux élèves dans de bonnes "
                           'conditions ? <BR>  M. le président. La parole est à M. le '
                           "ministre de l'éducation nationale, de la recherche et de la "
                           "technologie. <BR>  M. Claude Allègre, ministre de l'éducation "
                           'nationale, de la recherche et de la technologie.  Madame le '
                           'député, nous avons effectivement pris la décision de réemployer '
                           "28 000 maîtres auxiliaires, effort d'autant plus considérable que "
                           "nous sommes restés à l'intérieur de l'enveloppe de l'éducation "
                           'nationale, sans prévoir de dotations supplémentaires à cette fin. '
                           'Nous considérions en effet que ces personnels avaient été traités '
                           "d'une manière un peu brutale, si ce n'est cavalière. <BR>  En "
                           'contrepartie, nous avons décidé de ne plus créer de postes de '
                           "maîtres auxiliaires afin d'éviter que cette situation ne se "
                           "reproduise. Mais, naturellement, entre ce qu'est la décision et "
                           "la manière dont l'institution y répond, il y a, dirons-nous, une "
                           'certaine flexibilité. Il est très difficile de modifier en un '
                           'seul jour un système qui donnait de grandes commodités aux '
                           'recteurs puisque ceux-ci engageaient les maîtres auxiliaires dont '
                           "ils avaient besoin et laissaient l'Etat se débrouiller pour les "
                           'payer et ensuite, le cas échéant, pour les licencier. <BR>  Je '
                           "connais les difficultés que vous signalez. J'observe simplement "
                           "que nous avons créé cette année 360 000 heures d'enseignement "
                           'supplémentaires à effectifs constants. Cela veut dire que '
                           "l'effort est considérable, qu'il s'agisse du réemploi de maîtres "
                           'auxiliaires ou du taux plus élevé de réussite aux concours de '
                           'recrutement. <BR>  Où, malgré cet effort, subsiste-t-il des '
                           "difficultés ? <BR>  D'abord, dans les disciplines pointues des "
                           'lycées professionnels. A cet égard, nous avons donné aux recteurs '
                           "l'autorisation de recruter non pas des maîtres auxiliaires, mais "
                           'des contractuels, afin de ne pas produire du personnel en '
                           "surnombre. <BR>  S'agissant des enseignements généraux, nous "
                           "sommes en train d'étudier avec les recteurs, que j'ai rencontrés "
                           "ce matin même, les moyens d'améliorer un système de remplacement "
                           "que, je vous le dis franchement, peu d'organisations "
                           'toléreraient. Il aboutit, en effet, à ce que des enseignants ne '
                           "soient pas employés à tel endroit, tandis qu'ailleurs, certains "
                           'établissements manquent de professeurs. Nous sommes en train '
                           "d'ajuster les choses, mais céder à la tentation de «fabriquer» à "
                           'nouveau des maîtres auxiliaires ne serait pas une bonne solution. '
                           '<BR>  Je connais les disciplines générales où des problèmes se '
                           "posent, en particulier la biologie-géologie et l'espagnol. Nous "
                           'allons essayer de les résoudre. Je sais bien que, pour ceux qui '
                           'les subissent, la situation est intolérable, mais je vous demande '
                           'un tout petit peu de patience, en attendant que le nouveau '
                           "système se mette en place. <BR>  Vous savez d'ailleurs que nous "
                           'avons ouvert une table ronde sur le thème «zéro défaut». Je '
                           "souhaite en effet que, dans le futur, il n'y ait plus d'élèves "
                           'sans classe ou sans professeur, et je pense que nous pouvons y '
                           'arriver. Mais cela demande un changement de mentalité, y compris '
                           "dans l'administration de l'éducation nationale, qui s'est parfois "
                           'satisfaite de solutions de facilité et qui montre une certaine '
                           "résistance à l'évolution. Je viens de le dire avec une certaine "
                           'vigueur aux recteurs. <BR>  Je vous remercie, madame le député, '
                           'de cette question, car le problème que vous avez posé me '
                           'préoccupe énormément. <BR>  M. le président. La parole est à Mme '
                           'Nicole Bricq. <BR>  Mme Nicole Bricq. Monsieur le ministre, je '
                           "vous remercie de cette réponse très complète. J'aimerais "
                           'simplement obtenir une petite précision. Si je vous ai bien '
                           "compris, vous faites un distinguo entre l'enseignement "
                           "professionnel et l'enseignement général. Pour l'enseignement "
                           'professionnel, les directives aux recteurs que vous avez évoquées '
                           "ont-elles déjà été données ou vont-elles l'être ? <BR>  M. le "
                           'président. La parole est à M. le ministre. <BR>  M. le ministre '
                           "de l'éducation nationale, de la recherche et de la technologie. "
                           'Ces instructions ont déjà été données. Mais je reconnais que, '
                           'dans un certain nombre de cas, il y a eu un léger retard dans '
                           "l'application. Je regrette que ce soit, hélas ! une pratique "
                           'assez courante dans ce ministère. <BR>  On ne peut pas me '
                           'demander de remédier en quatre mois à la désorganisation qui '
                           "s'est progressivement mise en place depuis un certain nombre "
                           "d'années à l'intérieur de cette structure qui ressemble à un "
                           'conglomérat - pardonnez-moi ce terme géologique - de professions '
                           'libérales étatisées ! (Sourire.)</html> ',
                'support': 'Journal officiel',
                'title': 'fonctionnement'}

    buffer = read_file(file_path).decode("latin-1")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_14_qe_with_response():
    file_path = "qp/assemblee_leg_14-qe-ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Jean-Paul Bacquet',
                'dept': 'Puy-de-Dôme',
                'dpq': '16/05/2017',
                'dpr': '13/06/2017',
                'groupe': 'Socialiste, écologiste et républicain',
                'leg': '14',
                'ministere': 'Agriculture et alimentation',
                'nature': 'Question écrite',
                'num': '104002',
                'pgq': '3391',
                'pgr': '3777',
                'question': "M. Jean-Paul Bacquet attire l'attention de M. le ministre de "
                            "l'agriculture, de l'agroalimentaire et de la forêt, porte-parole "
                            'du Gouvernement sur une question spécifique concernant la '
                            'pérennité de la filière de valorisation agricole des boues, par '
                            "épandage, de station d'épuration urbaines, face à la volonté "
                            "croissante de certaines coopératives agricoles d'imposer à leurs "
                            "exploitants l'interdiction d'utilisation de ces dernières par le "
                            "biais de charte de qualité. À ce jour l'épandage des boues "
                            'urbaines reste le procédé le plus écologique et économique de '
                            'gestion de ces matières. Les boues constituent par ailleurs un '
                            'apport agronomique de grande valeur répondant à une '
                            'réglementation précise et une traçabilité importante. Ainsi, les '
                            'investissements importants engagés par les collectivités, pour '
                            'répondre aux exigences afférentes à cette filière, pourraient se '
                            'voir anéantis par la simple application unilatérale de ces '
                            "chartes dont l'objectif de qualité ne repose sur aucune base "
                            'scientifique avérée. Ainsi, il souhaite connaître les '
                            'dispositions législatives permettant aux collectivités de '
                            'préserver et pérenniser la filière de valorisation des boues '
                            'urbaines par épandage agricole ou les mesures envisagées pour '
                            'protéger ces dernières dans ce domaine face aux interdictions '
                            'imposées par certaines coopératives agricoles.',
                'reponse': 'Le maintien de la qualité des sols et des productions '
                           'alimentaires qui en sont issues représente un enjeu important, '
                           'intégré dans les politiques publiques gérées par le ministère de '
                           "l'agriculture et de l'alimentation (MAA). Le MAA veille en "
                           'particulier à la maîtrise des risques sanitaires et de la valeur '
                           'agronomique liés aux matières apportées aux sols, à travers la '
                           'mise en application de normes relatives aux produits organiques '
                           "et à leurs modalités d'application. L'utilisation de ces produits "
                           "reste quant à elle du libre choix de l'agriculteur. Des "
                           "prescriptions techniques et des règles particulières s'appliquent "
                           "pour l'épandage des boues issues de stations d'épuration urbaine. "
                           "Ces dernières sont définies au sein d'une réglementation qui "
                           'relève de la compétence du ministère de la transition écologique '
                           'et solidaire. Par ailleurs, le MAA soutient la transition du '
                           "secteur agricole, agroalimentaire et forestier vers l'économie "
                           'circulaire, dont les objectifs consistent notamment à réduire la '
                           'pression sur les ressources naturelles en tirant la valeur '
                           'ajoutée maximale des produits et déchets. La valorisation de '
                           "l'azote organique issu des effluents d'élevage en substitution à "
                           "l'azote minéral est privilégiée, notamment à travers le plan « "
                           "énergie, méthanisation, autonomie azote ». Il s'agit également "
                           "d'encourager l'utilisation des engrais organiques et à base de "
                           'biodéchets triés à la source et traités dans des filières '
                           'vertueuses, par exemple les déchets alimentaires des ménages et '
                           "les biodéchets des gros producteurs faisant l'objet de collecte "
                           'séparée puis méthanisés et/ou compostés et valorisés sur les sols '
                           'agricoles.',
                'support': 'Journal officiel',
                'title': ''}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_14_qe_without_response():
    file_path = "qp/assemblee_leg_14-qe-sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Patrice Martin-Lalande',
                'dept': 'Loir-et-Cher',
                'dpq': '20/06/2017',
                'dpr': '',
                'groupe': 'Non inscrit',
                'leg': '14',
                'ministere': 'Agriculture et alimentation',
                'nature': 'Question écrite',
                'num': '104137',
                'pgq': '',
                'pgr': '',
                'question': 'M. Patrice Martin-Lalande interroge M. le ministre de '
                            "l'agriculture et de l'alimentation sur la lutte contre les "
                            'catastrophes naturelles qui touchent le vignoble français. Le '
                            "vignoble est un atout majeur du pays, en termes d'emplois (il y "
                            'a plus de 68 000 exploitations), de balance commerciale, '
                            "d'aménagement du territoire et d'art de vivre. Les pertes "
                            "d'exploitation viticole enregistrées ces dernières années au "
                            'niveau national résultent principalement du gel, de la grêle, de '
                            "l'esca et de la flavescence dorée. Les phases de gel et la grêle "
                            'ont, pour la deuxième année consécutive, fait perdre une part '
                            "importante des récoltes. Selon les chiffres de l'Organisation "
                            'mondiale de la vigne et du vin (OIV), la production est en recul '
                            'et la France a durablement perdu sa place de premier producteur '
                            "par rapport à l'Italie et, si cette tendance continue, elle "
                            "perdra également son rang par rapport à l'Espagne. Il convient "
                            'donc de mobiliser tous les moyens possibles pour enrayer la '
                            "dégradation du vignoble et la baisse de la production. C'est "
                            'pourquoi il apparaît indispensable de compléter et de coordonner '
                            "au niveau législatif l'ensemble des dispositifs destinés à "
                            "favoriser l'implantation d'équipements de protection et à faire "
                            'face aux pertes de productions dues au gel et à la grêle. Comme '
                            "l'auteur de cette question l'avait proposé dans ses "
                            'interventions antérieures, plusieurs mesures peuvent être '
                            'envisagées à cette fin : généraliser la mise en place des '
                            "volumes complémentaires individuels, permettre l'instauration "
                            "d'une réserve de précaution ouvrant droit à déductibilité des "
                            "bénéfices agricoles et, dans le cadre d'opérations "
                            'territorialement coordonnées et cohérentes, encourager '
                            "fiscalement l'achat de réseaux de lutte antigel, notamment des "
                            'tours antigel. Il lui demande quelles mesures le Gouvernement '
                            'compte prendre, et suivant quel calendrier, pour améliorer cette '
                            'lutte contre le gel et la grêle et leurs effets qui impactent '
                            'gravement le vignoble français.',
                'reponse': '',
                'support': 'Journal officiel',
                'title': ''}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_14_qg():
    file_path = "qp/assemblee_leg_14-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Rémi Pauvros',
                'dept': 'Nord',
                'dpq': '22/02/2017',
                'dpr': '22/02/2017',
                'groupe': 'Socialiste, écologiste et républicain',
                'leg': '14',
                'ministere': 'Industrie',
                'nature': 'Question au Gouvernement',
                'num': '4698',
                'pgq': '',
                'pgr': '1088',
                'question': '</p><p align="CENTER"> BILAN DU QUINQUENNAT EN MATIÈRE D\'EMPLOI '
                            'INDUSTRIEL <a name=PG10></a> </p><br><strong>M.\xa0le président. '
                            '</strong>La parole est à M.\xa0Rémi Pauvros, pour le groupe '
                            'socialiste, écologiste et républicain.<br><br><strong>M.\xa0Rémi '
                            "Pauvros. </strong>Monsieur le secrétaire d'État chargé de "
                            "l'industrie, en novembre\xa02012, le rapport Gallois dressait un "
                            'diagnostic précis de notre industrie, faisant état de nos atouts '
                            "–\xa0la qualité des produits, une main-d'œuvre qualifiée et "
                            "performante, l'émergence de PME innovantes\xa0– mais "
                            'stigmatisait la situation catastrophique dans laquelle se '
                            'trouvait notre industrie\xa0: 750\xa0000\xa0emplois industriels '
                            'perdus entre 2002 et 2012, un solde de la balance commerciale '
                            'qui passe de 3,5\xa0milliards à un déficit de 71\xa0milliards en '
                            "2011, la part de l'industrie qui passe de 18\xa0% en 2000 à un "
                            'peu plus de 12,5\xa0% en 2011, la délocalisation massive des '
                            'outils de production.<br><br>Cette situation est le résultat '
                            "d'un abandon, celui de l'industrie, au profit du secteur "
                            'marchand et du capitalisme financier. Nous en connaissons les '
                            'conséquences douloureuses dans le territoire que je représente, '
                            'le Sambre-Avesnois. Les salariés de Sambre-et-Meuse –\xa0Akers, '
                            'Vallourec\xa0– en sont les dernières victimes.<br><br>Depuis '
                            '2012, nous menons une stratégie de reconquête industrielle car '
                            "il ne peut y avoir d'économie forte sans industrie forte. Nous "
                            'avons concentré des moyens sans précédent –\xa0trois plans '
                            "d'investissements, soit 57\xa0milliards d'euros sur dix ans\xa0– "
                            'pour la recherche numérique et la transition '
                            'énergétique.<br><br>Dans mon territoire, la relance de '
                            "l'automobile permet à MCA –\xa0Maubeuge construction "
                            "automobile\xa0– de créer des emplois. L'accord avec les "
                            'Britanniques pour la construction du double réacteur de '
                            "<i>Hinkley Point </i>apportera 60\xa0% de l'activité du site "
                            "d'Areva Jeumont et la réouverture d'un float à AGC Boussois "
                            "répond à une reprise du logement et de l'automobile. La "
                            "construction de douze sous-marins pour l'Australie assure le "
                            'carnet de commandes de Jeumont Electric.<br><br>Monsieur le '
                            "secrétaire d'État, quelles mesures prenez-vous pour conforter "
                            'deux secteurs fragiles, la métallurgie et le ferroviaire\xa0? '
                            'Comment intensifier encore notre politique pour redonner à la '
                            'France un outil de production compétitif et moderne et rendre '
                            'leur fierté aux ouvriers de notre pays\xa0? <i>(Applaudissements '
                            'sur plusieurs bancs du groupe socialiste, écologiste et '
                            'républicain.)</i><br><br><strong>M.\xa0le président. </strong>La '
                            "parole est à M.\xa0le secrétaire d'État chargé de "
                            "l'industrie.<br><br><strong>M.\xa0Christophe "
                            "Sirugue,</strong><i> secrétaire d'État chargé de l'industrie. "
                            "</i>Monsieur le député, vous l'avez souligné, des efforts "
                            'importants ont été engagés par le Gouvernement, avec un premier '
                            'objectif consistant à rétablir la compétitivité de nos '
                            "entreprises. Avec le CICE –\xa0crédit d'impôt pour la "
                            "compétitivité et l'emploi\xa0–, avec le pacte de responsabilité, "
                            'avec les efforts faits sur les cotisations au titre des '
                            'allocations familiales et en matière de sur-amortissement, des '
                            'résultats importants ont été obtenus.<br><br>Parmi ces '
                            'résultats, je veux souligner le rétablissement des marges de nos '
                            "entreprises au niveau de ce qu'elles étaient avant la crise. Je "
                            "veux souligner l'augmentation importante du nombre de créations "
                            "d'entreprises, qui est un élément significatif. Je veux "
                            "souligner le retour de l'investissement dans les entreprises "
                            "puisque celui-ci est aujourd'hui en hausse de près de 5\xa0%, ce "
                            'qui montre bien que tous ces éléments ont été productifs en '
                            'termes de soutien.<br><br>Mais nous avons encore du travail et '
                            "vous l'avez mentionné, monsieur le député, pour accompagner "
                            'certaines filières. Sachez que nous travaillerons dans ce sens '
                            "jusqu'à la fin du quinquennat.<br><br>Des contrats de filière "
                            'sont signés très régulièrement. Nous en signerons un dans '
                            'quelques instants avec Mme la ministre Audrey\xa0Azoulay pour la '
                            'filière communication et nous le ferons jeudi pour la filière '
                            "des services à la personne avec Mmes les secrétaires d'État "
                            'Pascale\xa0Boistard et Ségolène\xa0Neuville. Nous soutenons bien '
                            'évidemment la métallurgie et le secteur ferroviaire par le biais '
                            "de contrats de filière suffisamment puissants.<br><br>L'État a "
                            'également pris ses responsabilités dans le secteur ferroviaire, '
                            "dans le secteur naval et dans le secteur de l'automobile, parce "
                            "qu'il est important pour nous de montrer quel accompagnement "
                            'nous voulons mettre en place dans ces secteurs qui représentent '
                            "un nombre d'emplois considérable.<br><br>Mais nous avons aussi "
                            "besoin de les accompagner pour qu'ils s'engagent dans ces "
                            'transitions essentielles que sont la transition écologique et la '
                            "transition numérique. L'industrie du futur doit s'adresser à "
                            "tous les secteurs industriels parce qu'elle donnera de l'emploi "
                            "au plus grand nombre. Voilà l'objectif qui a été fixé et suivi "
                            'par le Gouvernement. <i>(Applaudissements sur plusieurs bancs du '
                            'groupe socialiste, écologiste et républicain.)</i><br> <p>',
                'reponse': '',
                'support': 'Journal officiel',
                'title': ''}
    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_14_qosd():
    file_path = "qp/assemblee_leg_14-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Brigitte Allain',
                'dept': 'Dordogne',
                'dpq': '07/02/2017',
                'dpr': '15/02/2017',
                'groupe': 'Non inscrit',
                'leg': '14',
                'ministere': 'Transports, mer et pêche',
                'nature': 'Question orale sans débat',
                'num': '1682',
                'pgq': '',
                'pgr': '961',
                'question': "Mme Brigitte Allain appelle l'attention de M. le secrétaire "
                            "d'État, auprès de la ministre de l'environnement, de l'énergie "
                            'et de la mer, chargée des relations internationales sur le '
                            'climat, chargé des transports, de la mer et de la pêche sur la '
                            'modernisation de la ligne de train '
                            'Bordeaux-Libourne-Bergerac-Sarlat. Cette ligne dont la '
                            'fréquentation est en hausse demeure en mauvais état sur la '
                            "section Libourne-Bergerac. Sa vétusté a d'ailleurs conduit SNCF "
                            "Réseau à mettre en place des ralentissements. D'importants "
                            'investissements ont été faits lors des derniers contrats de plan '
                            'État-région, entre 2000 et 2013 pour démarrer la modernisation '
                            'entre Libourne et Bergerac et rénover la section Bergerac '
                            '-Sarlat. Une étude a été menée par SNCF Réseau sur les '
                            "possibilités d'amélioration de l'accessibilité du bassin de vie "
                            'de Bergerac avec comme objectif : 1h pour Bergerac-Bordeaux et '
                            '3h pour Bergerac-Paris. Objectif qui mobilise tous les acteurs ! '
                            "C'est une nécessité absolue pour le désenclavement, le "
                            "développement économique et l'attractivité du Grand Bergeracois. "
                            "Un projet global en 2 phases, estimé à 74 millions d'euros a été "
                            'validé par le comité de pilotage en janvier 2015. Mais la '
                            "première phase de 45 millions d'euros qui permet de répondre aux "
                            'objectifs de désenclavement et de temps de parcours est pour le '
                            'moment bloquée. Elle a pourtant été inscrite au contrat de plan '
                            "État-région 2015-2020. Le cofinancement prévu implique l'État à "
                            '35 %, la région Nouvelle-Aquitaine à 35 %, SNCF Réseau à 15 % et '
                            'les collectivités locales à 15 %. À la demande du comité des '
                            'financeurs, SNCF réseau a été sollicitée pour fournir des '
                            'détails sur les coûts de cette opération et pour augmenter sa '
                            "contribution car c'est une infrastructure majeure du réseau "
                            'ferré. Des précisions ont bien été données, mais pour un montant '
                            "de 55,5 millions d'euros soit 10 millions d'euros de plus que "
                            "prévu ! Peu d'éléments permettent d'expliciter réellement cet "
                            'écart. En décembre 2014, elle était reçue avec une délégation '
                            "d'élus du bergeracois à ce sujet. Il soutenait alors ce projet "
                            "afin de profiter de l'arrivée de la LGV à Bordeaux en 2017, pour "
                            'désenclaver le bergeracois. En tant que partenaire financier du '
                            "CPER, en tant que membre du Gouvernement, elle lui demande s'il "
                            "compte intervenir pour que ce projet aboutisse rapidement. C'est "
                            'un enjeu primordial pour ce territoire.',
                'reponse': 'LIGNE DE TRAIN BORDEAUX-LIBOURNE-BERGERAC-SARLAT <br '
                           '/><strong>M.\xa0le président. </strong>La parole est à Mme\xa0'
                           'Brigitte Allain, pour exposer sa question, n° \xa01682, relative '
                           'à la ligne de train Bordeaux-Libourne-Bergerac-Sarlat.<br /><br '
                           '/><strong>Mme\xa0Brigitte Allain. </strong>Madame la secrétaire '
                           "d'État, j'appelle votre attention sur la modernisation du Train "
                           "Express Régional Bordeaux-Libourne-Bergerac-Sarlat. J'associe à "
                           'ma question le président de la région Nouvelle-Aquitaine, Alain '
                           'Rousset, qui en partage le contenu. Cette ligne, dont la '
                           'fréquentation est en hausse, demeure en mauvais état. Sa vétusté '
                           "a d'ailleurs amené SNCF\xa0Réseau à mettre en place des "
                           "ralentissements. D'importants investissements ont été réalisés "
                           'entre\xa02000 et\xa02013 dans le cadre des contrats de plan '
                           'État-région – CPER – afin de réduire le temps de trajet entre '
                           'Bordeaux, Bergerac et Sarlat et sécuriser la ligne. Cet objectif '
                           'mobilise tous les acteurs concernés depuis longtemps.<br /><br '
                           '/>La modernisation de la ligne entre Bergerac et Libourne obéit à '
                           "une triple nécessité\xa0: l'attractivité économique et "
                           'touristique du Bergeracois, la mobilité de ceux qui utilisent '
                           "quotidiennement ce TER et ne disposent pas d'autres moyens de "
                           'locomotion et le soutien des modes de transport les plus sobres '
                           "ainsi que le désengorgement d'un réseau routier public déjà "
                           "saturé. En décembre\xa02014, le secrétaire d'État chargé des "
                           "transports, M.\xa0Vidalies, a reçu une délégation d'élus "
                           'territoriaux et soutenu ce projet permettant de profiter de la '
                           'mise en service de la LGV – ligne à grande vitesse – à Bordeaux '
                           'en 2017.<br /><br />Afin de moderniser la ligne dans le cadre '
                           "d'un projet dont le montant global s'élève à 74\xa0millions "
                           "d'euros, une première phase de travaux d'un coût de 45\xa0"
                           "millions d'euros a été inscrite dans le contrat de plan "
                           'État-région et validée par le comité de ligne en janvier\xa02015. '
                           "Deux ans après, rien n'a bougé\xa0! À la demande du comité des "
                           'financeurs, SNCF Réseau a été sollicitée pour fournir des détails '
                           'sur le coût de cette opération et augmenter sa contribution, car '
                           "il s'agit d'une infrastructure majeure du réseau ferré.<br /><br "
                           "/>Les précisions fournies font état d'un montant de 55,5\xa0"
                           "millions d'euros, soit dix de plus que prévu, sans que rien "
                           "n'explique vraiment cet écart. Quant aux usagers, ils continuent "
                           'de subir les retards à répétition et les trains supprimés et il '
                           'faut toujours 2\xa0h\xa050 pour parcourir les 168\xa0km séparant '
                           'Sarlat de Bordeaux\xa0! Ma question est donc simple\xa0: comment '
                           'le Gouvernement compte-t-il faire en sorte que SNCF\xa0Réseau '
                           'augmente sa contribution afin que ce projet aboutisse le plus '
                           'rapidement possible\xa0? Comment les financements perdus par les '
                           "régions en raison de l'abandon de l'écotaxe seront-ils remplacés "
                           'afin de préparer la mobilité de ce siècle\xa0?<br /><br '
                           '/><strong>M.\xa0le président. </strong>La parole est à Mme\xa0la '
                           "secrétaire d'État chargée de la biodiversité.<br /><br "
                           "/><strong>Mme\xa0Barbara Pompili,</strong><i> secrétaire d'État "
                           'chargée de la biodiversité. </i>Madame la députée, vous '
                           'interrogez mon collègue Alain Vidalies, qui ne peut être présent '
                           'ce matin, sur la modernisation de la ligne de train '
                           'Bordeaux-Libourne-Bergerac-Sarlat. Des études ont en effet été '
                           'réalisées préalablement au contrat de plan actuel. Elles portent '
                           "sur la possibilité d'améliorer la desserte de Bergerac et son "
                           'raccordement au réseau à grande vitesse via Libourne et Bordeaux '
                           'dans le cadre de la mise en service cette année de la LGV SEA – '
                           "Sud Europe Atlantique. Elles ont permis d'élaborer plusieurs "
                           'scénarios et de définir les travaux à réaliser en priorité.<br '
                           "/><br />Compte tenu de l'état des voies et des enjeux "
                           "d'aménagement du territoire associés à la desserte de Bergerac, "
                           "l'État et la région ont inscrit au CPER Aquitaine 2015-2020 des "
                           "travaux de régénération de la ligne dont le montant s'élève, "
                           'compte tenu des financements mobilisables, à 45\xa0millions '
                           "d'euros. L'État et la région y contribuent chacun à hauteur de "
                           "15,75\xa0millions d'euros, le reste est financé par SNCF\xa0"
                           'Réseau et les autres collectivités concernées. Un engagement fort '
                           'a donc été pris en faveur de cette ligne. Les travaux prévus sont '
                           'destinés à assurer la pérennité de la ligne Libourne-Bergerac et '
                           'éviter la mise en place de ralentissements importants. '
                           "L'opération prévoit par ailleurs le renouvellement complet de la "
                           "voie, la reprise d'ouvrages d'art et la mise en accessibilité de "
                           "six gares.<br /><br />L'estimation du coût de l'opération par le "
                           "maître d'ouvrage s'élève à environ 55\xa0millions d'euros, "
                           'principalement en raison de problèmes de stabilité du terrain. Il '
                           'a donc été prié de travailler à un scénario compatible avec '
                           "l'enveloppe de 45\xa0millions d'euros inscrite au CPER avant de "
                           "livrer les études d'avant-projet au printemps 2017. Le comité "
                           'technique sera alors immédiatement invité à examiner ses '
                           'propositions. Les études de projet et les travaux entre Libourne '
                           'et Bergerac seront programmés dès que tous les partenaires auront '
                           'mobilisé les crédits nécessaires, conformément aux termes du '
                           "CPER. L'État, SNCF\xa0Réseau et les collectivités locales y "
                           'travaillent.<br /><br /><strong>M.\xa0le président. </strong>La '
                           'parole est à Mme\xa0Brigitte Allain.<br /><br /><strong>Mme\xa0'
                           'Brigitte Allain. </strong>Je vous remercie de votre réponse, '
                           "madame la secrétaire d'État. Si j'ai bien entendu, le coût du "
                           "projet doit bien s'en tenir aux 45,5\xa0millions d'euros "
                           "initialement prévus. Il n'est donc pas question que SNCF\xa0"
                           'Réseau répercute des financements qui lui incombent directement '
                           "sur ce projet conjoint de l'État et de la région. Telle était "
                           "bien l'inquiétude des élus de la région. Je vous remercie de "
                           'cette réponse que je transmettrai aux collectivités territoriales '
                           'concernées.<br />',
                'support': 'Journal officiel',
                'title': 'LIGNE DE TRAIN BORDEAUX-LIBOURNE-BERGERAC-SARLAT '}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_14_qosd_without_response():
    file_path = "qp/assemblee_leg_14-qosd-sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Noël Mamère',
                'dept': 'Gironde',
                'dpq': '17/05/2016',
                'dpr': '',
                'groupe': 'Écologiste',
                'leg': '14',
                'ministere': 'Agriculture, agroalimentaire et forêt',
                'nature': 'Question orale sans débat',
                'num': '1453',
                'pgq': '',
                'pgr': '',
                'question': "M. Noël Mamère alerte M. le ministre de l'agriculture, de "
                            "l'agroalimentaire et de la forêt, porte-parole du Gouvernement "
                            "sur l'utilisation de produits phytosanitaires dangereux lors du "
                            'traitement des vignes de Gironde. Le printemps est arrivé et '
                            "avec lui la saison d'épandage des pesticides sur les zones "
                            'viticoles du bordelais. Si le documentaire <em>Cash '
                            'Investigation</em> a permis une médiatisation plus large des '
                            'méthodes et produits phytopharmaceutiques utilisés, la '
                            "généralisation d'études scientifiques ces dernières années "
                            'concernant les effets néfastes des biocides sur la santé et deux '
                            "événements girondins récents ont conduit les parents d'élèves du "
                            "département à se fédérer davantage chaque jour autour d'une "
                            'inquiétude commune et légitime : la santé de leurs enfants. En '
                            'Gironde, le 5 mai 2014, ce sont vingt-trois enfants et une '
                            "institutrice de l'école de Villeneuve-de-Blaye, établissement "
                            'entouré de vignes, qui sont hospitalisés en urgence après avoir '
                            'ressenti des migraines, nausées et étourdissements. Le matin '
                            'même, les parcelles viticoles environnantes ont été aspergées de '
                            "pesticides. Le 5 août 2015, l'Agence régionale de la santé (ARS) "
                            "et l'Institut de veille sanitaire (Invs) publient un rapport sur "
                            "l'excès constaté de cas de cancers pédiatriques sur la commune "
                            'de Preignac, toujours en Gironde. Quatre cas sont en effet '
                            'recensés entre 1999 et 2012 sur cette commune qui ne totalise '
                            'que deux mille habitants. Si ce rapport ne peut démontrer le '
                            'lien entre cancers et pesticides sur un effectif si réduit, il '
                            'estime toutefois que le facteur de risque est connu. Ces deux '
                            'événements médiatisés ne peuvent être considérés comme des '
                            'épiphénomènes. Depuis les années 1980 en effet, les enquêtes '
                            "épidémiologiques évoquant l'implication des pesticides dans "
                            'plusieurs pathologies chez des personnes exposées '
                            'professionnellement à ces substances (cancers, troubles de la '
                            "fertilité, etc.) sont légion et aujourd'hui, des recherches "
                            'récentes tendent à prouver que la généralisation de maladies '
                            "neurologiques comme Alzheimer et l'autisme pourrait être "
                            "favorisée par l'utilisation des biocides. Certes, le préfet de "
                            'la région Aquitaine, par arrêté du 22 avril 2016, interdit '
                            "l'application de produits phytopharmaceutiques à proximité des "
                            'établissements scolaires pendant les 20 minutes qui précèdent et '
                            'suivent le début et la fin des activités scolaires et '
                            'périscolaires, lors des récréations et des activités se '
                            'déroulant en plein air. Mais lorsque ces produits sont appliqués '
                            'ne serait-ce que quelques heures avant le passage des enfants, '
                            'ces derniers pénètrent dans une zone toujours imprégnée de '
                            'résidus de pesticides... Par ailleurs, les témoignages se '
                            'multiplient sur les réseaux sociaux pour dénoncer le non-respect '
                            'de cet arrêté et le problème reste donc entier. La seule '
                            "solution efficace aujourd'hui est une décision gouvernementale : "
                            "celle d'appliquer le principe de précaution en interdisant "
                            "immédiatement l'utilisation phytopharmaceutique des substances "
                            'chimiques, seules ou en mélange, classées CMR (cancérogènes '
                            'mutagènes ou reprotoxiques) selon la directive européenne '
                            '67/548/CE, substances reconnues comme étant les plus dangereuses '
                            "pour la santé humaine, animale et l'environnement. Il lui "
                            'demande donc sa position sur le sujet.',
                'reponse': '',
                'support': 'Journal officiel',
                'title': ''}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_15_qe_without_response():
    file_path = "qp/assemblee_leg_15-qe-sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Thibault Bazin',
                'dept': 'Meurthe-et-Moselle',
                'dpq': '21/06/2022',
                'dpr': '',
                'groupe': 'Non inscrit',
                'leg': '15',
                'ministere': 'Santé et prévention',
                'nature': 'Question écrite',
                'num': '45666',
                'pgq': '3353',
                'pgr': '',
                'question': "M. Thibault Bazin appelle l'attention de Mme la ministre de la "
                            'santé et de la prévention sur le non-remboursement de certaines '
                            'analyses médicales par la sécurité sociale. Dans certaines '
                            'maladies, ces analyses sont pourtant indispensables au '
                            "diagnostic, au suivi de leur évolution et à l'appréciation de "
                            "l'efficacité de leur traitement. Tel est le cas du dosage des "
                            "chaînes légères libres vis-à-vis des pathologies de l'amylose "
                            'primitive. Cette analyse, qui ne figure pas à la table nationale '
                            'de biologie, est inscrite sur la liste des analyses non '
                            "remboursées par la sécurité sociale alors qu'elle représente "
                            'pour le patient un coût de quatre-vingt-huit euros par dosage. '
                            "Ce dosage devant se faire régulièrement, il affecte d'autant la "
                            'situation financière des patients. Il lui demande donc si le '
                            "Gouvernement prévoit le remboursement par l'assurance maladie de "
                            "cette analyse en cas d'amylose sachant que, depuis le 1er juin "
                            '2021, le remboursement du dosage de chaînes légères libres kappa '
                            'et lambda dans le sang est possible pour le diagnostic et le '
                            "suivi de patients atteints d'un myélome multiple.",
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Amylose - remboursement des analyses médicales'}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_15_qe_with_response():
    file_path = "qp/assemblee_leg_15-qe-ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Gérard Leseul',
                'dept': 'Seine-Maritime',
                'dpq': '26/04/2022',
                'dpr': '17/05/2022',
                'groupe': 'Socialistes et apparentés',
                'leg': '15',
                'ministere': 'Culture',
                'nature': 'Question écrite',
                'num': '45373',
                'pgq': '2623',
                'pgr': '3199',
                'question': "M. Gérard Leseul appelle l'attention de Mme la ministre de la "
                            'culture sur les attentes des aveugles de France au sujet de leur '
                            'accès au monde du livre. Cet accès dépend de la facilitation de '
                            'la diffusion du système braille et des moyens financiers qui '
                            "sont alloués. On constate aujourd'hui encore une très faible "
                            'part des ouvrages existants sur le marché disponibles en '
                            "braille. Ce manque compromet l'accès à la culture pour les "
                            'aveugles et particulièrement pour les jeunes qui éprouvent des '
                            'difficultés dans leurs études. Il est également à noter que les '
                            'prix de ces ouvrages sont beaucoup plus élevés que les autres, '
                            'ce qui constitue une véritable inégalité en défaveur des '
                            'déficients visuels. M. le député rappelle que la Fédération des '
                            "aveugles et amblyopes de France a d'ailleurs déjà formulé "
                            'plusieurs pistes pour améliorer la situation actuelle. Il '
                            "l'interroge afin de prendre connaissance des mesures que le "
                            'Gouvernement envisage de mettre en œuvre dans ce contexte pour '
                            "améliorer l'accès aux livres pour les aveugles.",
                'reponse': 'Le Gouvernement &#339;uvre depuis de longues années pour '
                           "améliorer l'accès au livre et à la lecture pour les personnes "
                           "empêchées de lire en raison d'un trouble ou d'un handicap, quel "
                           "qu'il soit. Cette action s'est traduite depuis une quinzaine "
                           "d'années par un premier axe de travail : une exception au droit "
                           "d'auteur en faveur des personnes handicapées a été introduite "
                           'dans le code de la propriété intellectuelle par la loi du 1er '
                           "août\xa02006 relative aux droits d'auteur et aux droits voisins "
                           "dans la société de l'information afin de permettre à des "
                           'organismes habilités de produire et de diffuser des adaptations '
                           "d'&#339;uvres sous droit dans des formats adaptés aux besoins des "
                           'personnes en situation de handicap. La Bibliothèque nationale de '
                           "France (BnF) a reçu la mission d'être l'organisme dépositaire des "
                           'fichiers numériques des éditeurs des &#339;uvres qui ont fait '
                           "l'objet d'une demande par un organisme habilité à en faire "
                           "l'adaptation. Le dispositif est opérationnel depuis juin\xa02010, "
                           "date de l'ouverture de la plateforme Platon gérée par la BnF, qui "
                           'garantit un cadre sécurisé pour la procédure de transmission des '
                           'fichiers des éditeurs et de mutualisation des fichiers numériques '
                           'adaptés entre organismes habilités. La BnF est donc positionnée, '
                           'depuis plus de dix ans, comme tiers de confiance entre les '
                           'éditeurs et les organismes adaptateurs. La loi du 7\xa0juillet\xa0'
                           "2016 relative à la liberté de la création, à l'architecture et au "
                           'patrimoine a amélioré le cadre juridique de cette exception, en '
                           'élargissant les bénéficiaires aux personnes porteuses de troubles '
                           'cognitifs et de troubles des apprentissages (dyslexie, dyspraxie, '
                           'dysphasie, etc.), en demandant aux éditeurs de déposer sur la '
                           'plateforme Platon les fichiers numériques dans un format dont la '
                           'structuration permet de produire facilement et rapidement des '
                           'documents adaptés, en obligeant les éditeurs scolaires à déposer '
                           'les manuels scolaires dès leur parution, ou encore en permettant '
                           "aux bénéficiaires de l'exception d'accéder sur Platon à "
                           "l'ensemble de l'offre adaptée existant sous forme numérique. Ces "
                           'évolutions juridiques ont anticipé la mise en &#339;uvre en droit '
                           "français du Traité de Marrakech, signé par l'Union européenne en "
                           '2014 et inscrit dans le droit communautaire par la directive '
                           '2017/1564 et du règlement 2017/1563 du 13\xa0septembre\xa02017. '
                           "En France, c'est la loi du 5\xa0septembre\xa02018 pour la liberté "
                           'de choisir son avenir professionnel qui a transposé ces textes '
                           "européens. Un décret d'application du 20\xa0décembre\xa02018 est "
                           'venu compléter la transposition de la directive, en apportant des '
                           'simplifications et allégements substantiels pour faciliter les '
                           'habilitations et les activités des organismes, répondant ainsi '
                           'aux attentes des organismes représentatifs des personnes '
                           "handicapées et des bibliothèques publiques. Aujourd'hui, 140 "
                           "organismes sont habilités à bénéficier de l'exception, dont 80 "
                           'sont agréés pour accéder aux fichiers numériques des &#339;uvres '
                           "transmis par les éditeurs. Il s'agit en majorité d'associations "
                           "et d'établissements publics : établissements médico-sociaux en "
                           "charge de l'accompagnement des personnes handicapées, "
                           "établissements d'enseignement, bibliothèques. En fin d'année "
                           '2021, on comptait sur Platon environ 12 000 fichiers adaptés, '
                           'auxquels il faut ajouter les collections constituées de longue '
                           "date par les organismes adaptateurs comme l'association Valentin "
                           "Haüy, l'association BrailleNet ou les établissements "
                           'médico-sociaux. Les documents sont adaptés dans différents '
                           'formats : fichiers numériques en format texte ou PDF, fichiers '
                           'audio au format MP3 ou Daisy (format structuré spécialement conçu '
                           'pour faciliter la lecture par les personnes déficientes '
                           'visuelles), textes en gros caractères, braille numérique, braille '
                           'papier intégral ou abrégé, vidéos en langue des signes française '
                           '(LSF), documents rédigés en Facile à lire et à comprendre (FALC). '
                           "Parallèlement à l'évolution du droit pour faciliter l'adaptation "
                           'des &#339;uvres, une stratégie interministérielle est déployée '
                           'depuis 2018 pour développer une offre numérique nativement '
                           "accessible. C'est le deuxième axe de travail. Cette politique "
                           "s'appuie sur les progrès des technologies numériques qui "
                           "permettent de développer des fonctionnalités d'accessibilité "
                           'intégrées nativement aux fichiers des livres numériques, en '
                           'particulier grâce au format EPUB3, ouvert et interopérable. Le '
                           "ministère de la culture apporte son soutien à l'« European "
                           'Digital Reading Lab » (EDRLab), qui &#339;uvre en Europe pour '
                           'favoriser le développement de ce format. Le Gouvernement, à la '
                           'demande du comité interministériel du handicap (CIH), a lancé en '
                           "2018 un comité de pilotage pour le développement d'une offre de "
                           "livres numériques nativement accessibles, incluant l'ensemble des "
                           'acteurs de la chaine économique du livre, des organismes '
                           'représentant les personnes en situation de handicap, des experts '
                           "de l'accessibilité et les administrations concernées. Ce comité a "
                           'adopté un plan stratégique qui fixe les grandes orientations à '
                           "suivre et présente l'ensemble des enjeux, depuis la formation des "
                           "éditeurs jusqu'à l'initiation des personnes handicapées aux "
                           "pratiques de lecture numérique, en passant par l'accessibilité "
                           'des dispositifs de vente en ligne et de mise à disposition '
                           'distante des bibliothèques publiques. Il sert de feuille de route '
                           "et permet d'effectuer des bilans périodiques des actions engagées "
                           "pour atteindre les objectifs qu'il énonce. Cette stratégie "
                           "s'inscrit dans le cadre de la directive 2019/882 du Parlement "
                           'européen et du Conseil du 17\xa0avril\xa02019 relative aux '
                           "exigences en matière d'accessibilité applicables aux produits et "
                           'services, qui doit être transposée en droit français en juin\xa0'
                           '2022 pour entrer en vigueur à partir de juin\xa02025. Ce texte '
                           'permettra à la majeure partie des catalogues numériques des '
                           "éditeurs français d'être nativement accessible au plus grand "
                           'nombre, dans les mêmes conditions, au même prix et dans la même '
                           "temporalité pour l'ensemble de la population française, auprès de "
                           "tous les libraires et vendeurs de livres ; il s'agit là d'un "
                           'progrès considérable vers une société plus inclusive. Le '
                           'ministère de la culture a lancé une étude sur les effets de la '
                           'directive sur le secteur du livre numérique en France afin de '
                           'préparer au mieux celui-ci à sa mise en &#339;uvre. Les résultats '
                           'de cette étude sont attendus pour mars\xa02022. Après avoir créé '
                           "les conditions juridiques et techniques en faveur de l'adaptation "
                           'des &#339;uvres ou de leur édition sous une forme nativement '
                           "accessible, le Gouvernement s'attache à en développer la "
                           "production et à en faciliter l'accès pour les personnes "
                           'handicapées. Il a lancé au printemps 2021 une étude de '
                           "faisabilité pour la création d'un service national de l'édition "
                           "accessible et la définition d'un plan de production de documents "
                           "adaptés. L'objectif de ce service numérique est de simplifier les "
                           'démarches des personnes handicapées pour repérer et se procurer '
                           "des livres et d'autres documents accessibles, en recherchant une "
                           'meilleure efficience des processus de signalement et de réponse '
                           "aux demandes de livres. Il s'agit également d'augmenter "
                           "significativement l'offre de contenus, non seulement dans le "
                           "cadre de l'exception au droit d'auteur en faveur des personnes "
                           'handicapées, mais aussi dans celui de la stratégie '
                           "interministérielle pour le développement d'une offre commerciale "
                           'numérique nativement accessible. Les nombreux échanges intervenus '
                           "à l'occasion de l'étude montrent que la création de ce service, "
                           "incluant la définition d'un plan de production de l'édition "
                           'adaptée, répond aux attentes des personnes empêchées de lire en '
                           "raison d'un trouble ou d'un handicap et de leurs accompagnants. "
                           'Sur la base des résultats de cette étude, le CIH du 3\xa0février '
                           "dernier a décidé la création de ce portail national de l'édition "
                           "accessible et le lancement d'un plan de production de documents "
                           "adaptés dans le cadre de l'exception handicap au droit d'auteur. "
                           'Cet ambitieux projet interministériel associe, sous la houlette '
                           "du secrétariat général du CIH, le secrétariat d'État aux "
                           'personnes handicapées, les ministères chargés des solidarités, de '
                           "la culture, de l'éducation nationale, de l'enseignement supérieur "
                           'et du travail. Une mission de préfiguration devrait en préciser '
                           'pour juin prochain les contours opérationnels, administratifs et '
                           'financiers.',
                'support': 'Journal officiel',
                'title': 'Accès aux livres'}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_15_qg():
    file_path = "qp/assemblee_leg_15-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Yaël Braun-Pivet',
                'dept': 'Yvelines',
                'dpq': '23/02/2022',
                'dpr': '23/02/2022',
                'groupe': 'La République en Marche',
                'leg': '15',
                'ministere': 'Égalité femmes-hommes, diversité et égalité des chances',
                'nature': 'Question au Gouvernement',
                'num': '4851',
                'pgq': '',
                'pgr': '',
                'question': '</p><p align="CENTER"> POLITIQUE DU GOUVERNEMENT EN FAVEUR DE '
                            "L'ÉGALITÉ <a name=PG26></a> </p><br><strong>M.\xa0le président. "
                            '</strong>La parole est à Mme\xa0Yaël '
                            'Braun-Pivet.<br><br><strong>Mme\xa0Yaël Braun-Pivet. '
                            "</strong>Monsieur le président, mes chers collègues, j'ai "
                            "l'honneur de poser la dernière question au Gouvernement de ce "
                            'mandat <i>(Applaudissements sur les bancs du groupe LaREM ainsi '
                            'que sur plusieurs bancs du groupe Dem)</i>, et je suis heureuse '
                            'que celle-ci porte sur une cause qui nous a tous réunis et qui a '
                            'transcendé les clivages, de sorte que, sur les textes relatifs à '
                            "ce combat, nous avons bien souvent trouvé l'unanimité. Cette "
                            "question, vous l'aurez compris, porte sur la cause que le "
                            'Président de la République a élevée, le 25\xa0novembre 2017, au '
                            'rang de grande cause du quinquennat\xa0: le combat, qui devait '
                            "être le combat de la nation toute entière, pour l'égalité entre "
                            'les femmes et les hommes. (Mêmes mouvements.)<br><br>Le bilan '
                            'que nous allons décrire est notre bilan à tous. Il est '
                            "incontestable et je crois qu'il est exemplaire. Madame la "
                            "ministre déléguée Elisabeth Moreno, c'est vous que je souhaite "
                            'bien sûr interroger sur ce sujet et sur la lutte contre les '
                            'discriminations dont vous avez la charge. <br><br>Comment ne pas '
                            "parler d'égalité en politique, lorsqu'on voit les visages de "
                            "cette assemblée\xa0? Nous avons souhaité qu'il en soit ainsi "
                            'également dans toutes les communes en adoptant la proposition de '
                            'loi visant à renforcer la parité dans les fonctions électives et '
                            'exécutives du bloc communal défendue par notre collègue Élodie '
                            'Jacquier-Laforge.<i> (Mêmes mouvements.)</i> Sans attendre, nous '
                            "avons facilité l'engagement de tous, notamment grâce à la prise "
                            'en charge des frais de garde dans la loi «\xa0engagement et '
                            'proximité\xa0». (Applaudissements sur quelques bancs du groupe '
                            'LaREM.)<br><br>Nous avons également souhaité protéger toutes les '
                            'femmes contre les violences qui les visent. Quatre textes ont '
                            'été adoptés pour mieux réprimer les violences sexuelles, les '
                            'outrages sexistes, le cyberharcèlement. Nous avons allongé les '
                            'délais de prescription, généralisé les bracelets '
                            "antirapprochement, accéléré le prononcé d'ordonnances de "
                            'protection. Nous avons travaillé sur la lutte contre les '
                            'mariages forcés et la polygamie, des mesures soutenues avec '
                            'force par la ministre déléguée Marlène Schiappa. Nous avons '
                            "donné au Gouvernement les moyens d'agir en la matière, et fait "
                            "tant d'autres choses, madame la ministre déléguée, que vous "
                            "allez pouvoir nous rappeler, afin de lutter pour l'égalité\xa0! "
                            '<i>(Applaudissements sur plusieurs bancs du groupe LaREM, ainsi '
                            'que sur quelques bancs du groupe Dem.)</i><br><br><strong>M.\xa0'
                            'le président. </strong>La parole est à Mme\xa0la ministre '
                            "déléguée chargée de l'égalité entre les femmes et les hommes, de "
                            "la diversité et de l'égalité des chances.<br><br><strong>Mme\xa0"
                            'Elisabeth Moreno,</strong><i> ministre déléguée chargée de '
                            "l'égalité entre les femmes et les hommes, de la diversité et de "
                            "l'égalité des chances. </i>Monsieur le président, mesdames et "
                            'messieurs les députés, madame la députée Yaël Braun-Pivet, '
                            "j'éprouve autant d'émotion à répondre à cette dernière question "
                            'que le jour où je suis entrée pour la première fois dans cet '
                            "hémicycle. Je vous remercie de m'offrir l'occasion de rendre "
                            'hommage au travail parfois complexe de la représentation '
                            'nationale.<br><br>La lutte contre les discriminations, les '
                            "inégalités, le refus d'une citoyenneté de seconde zone et de "
                            "l'assignation à résidence qui gâchent tant de vies, ont été au "
                            'cœur de nos actions, et les nombreuses lois que vous avez votées '
                            'pour mieux protéger et accompagner les victimes de violences '
                            'conjugales et leurs enfants démontrent que vous avez été à la '
                            'hauteur de cette grande cause du quinquennat. Parce que sans '
                            "égalité économique, l'égalité réelle ne saurait advenir, nous "
                            "avons redoublé d'efforts pour briser les plafonds de verre qui "
                            "empêchent encore trop de femmes de s'accomplir "
                            'professionnellement.<br><br>Ce quinquennat est aussi celui de '
                            'nombreuses actions qui ont permis de lutter contre le racisme, '
                            "l'antisémitisme, l'homophobie, la transphobie, la xénophobie, "
                            'qui sévissent encore dans notre pays. La plateforme de lutte '
                            "contre les discriminations\xa0: nous l'avons faite. "
                            '<i>(Applaudissements sur plusieurs bancs du groupe LaREM. –\xa0'
                            "M.\xa0Erwan Balanant applaudit également.)</i> L'index de "
                            "l'égalité professionnelle\xa0: nous l'avons fait. Imposer les "
                            "femmes dans les instances de direction\xa0: nous l'avons fait. "
                            'La PMA –\xa0procréation médicalement assistée\xa0– pour toutes '
                            "les femmes, certains l'ont ardemment combattu, d'autres l'ont "
                            "fait miroiter\xa0; nous l'avons faite. Doubler le congé "
                            'paternité, rendre la contraception gratuite pour les jeunes '
                            'femmes de 18 à 25\xa0ans, mais aussi lutter contre la précarité '
                            'menstruelle, impulser des mesures sans précédent pour lutter '
                            "contre l'endométriose, nous l'avons fait, vous l'avez fait, "
                            'mesdames et messieurs les députés. (Applaudissements sur '
                            'plusieurs bancs du groupe LaREM.) Permettre aux femmes et aux '
                            "hommes d'être recrutés pour leurs compétences et leurs talents, "
                            'indépendamment de leur origine sociale ou culturelle\xa0: nous '
                            "l'avons engagé. (Applaudissements sur quelques bancs du groupe "
                            "LaREM.)<br><br>Agir pour l'égalité des droits humains est une "
                            'tâche immense qui nous honore et nous oblige, indépendamment de '
                            "nos familles politiques. J'ai rencontré dans cet hémicycle des "
                            'députés et des parlementaires pleinement engagés. Je vous en '
                            "remercie et je ne l'oublierai jamais. <i>(De nombreux députés du "
                            'groupe LaREM et quelques députés du groupe Dem se lèvent et '
                            'applaudissent.)</i><br>',
                'reponse': '',
                'support': 'Journal officiel',
                'title': "Politique du Gouvernement en faveur de l'égalité"}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_15_qosd():
    file_path = "qp/assemblee_leg_15-qosd.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Jean Lassalle',
                'dept': 'Pyrénées-Atlantiques',
                'dpq': '15/02/2022',
                'dpr': '23/02/2022',
                'groupe': 'Libertés et Territoires',
                'leg': '15',
                'ministere': 'Solidarités et santé',
                'nature': 'Question orale sans débat',
                'num': '1704',
                'pgq': '',
                'pgr': '',
                'question': 'M. Jean Lassalle alerte M. le ministre des solidarités et de la '
                            'santé sur la situation intolérable des praticiens du service des '
                            "urgences du Centre hospitalier d'Oloron-Sainte-Marie dans sa "
                            'circonscription. En effet, soumis de façon récurrente à la '
                            'problématique des effectifs médicaux et ce depuis plus de deux '
                            "ans, au manque de titulaires, d'internes et enfin "
                            "d'intérimaires, ces praticiens alertent sans cesse et en vain "
                            "les services compétents de l'État, à savoir le ministère des "
                            "solidarités et de la santé, la préfecture et l'agence régionale "
                            'de santé. Dès le 11 juin 2020 par courrier, ils ont tenté '
                            "d'appeler leur attention sur la problématique des effectifs à "
                            "venir et conséquemment, sur la nécessité urgente d'un "
                            'recrutement de nouveaux praticiens hospitaliers dans leur '
                            'service, tout en expliquant une difficulté particulière de ce '
                            "recrutement et des axes d'amélioration possibles. Faute "
                            "d'actions, dès octobre 2020, leur service s'est retrouvé dans "
                            "une situation extrêmement compliquée, génératrice d'un risque "
                            'important, y compris sur le plan sanitaire au détriment des '
                            "usagers, du fait d'un manque de médecins pour garantir "
                            'correctement le service (4,3 employés temps plein pour un besoin '
                            'à 12 ETP). De surcroît, en novembre 2020, ils ont été assignés '
                            'pour pallier le manque de médecins, alors que ces assignations '
                            "visaient les praticiens titulaires, c'est-à-dire six "
                            'professionnels, lesquels exercent déjà leur fonction conforme à '
                            "leur temps de travail avec nécessité d'un repos, au respect de "
                            'leur vie privée et de leur propre santé, mais également à la '
                            'prise en charge des patients dans des conditions optimales de '
                            'soin et de sécurité. Suite à cette situation, différentes '
                            'instances et acteurs de la vie politique, entre autres le '
                            "sous-préfet des Pyrénées-Atlantiques et l'ARS 64 et 33, ont été "
                            'une fois de plus alertés, mais vainement puisque aucune réponse '
                            "n'a jamais été apportée. Une telle organisation très précaire et "
                            'fragile, sans les moyens financiers nécessaires à fidéliser les '
                            "médecins vacataires, s'aggravait. Dans les mois qui ont suivi, "
                            "leurs difficultés ont été accrues par le manque d'internes. "
                            "Ainsi, à ce sujet, un courrier adressé à la direction de l'ARS "
                            'en date de janvier 2021 est resté sans réponse. Par la suite, la '
                            'menace de la loi Rist est venue renforcer cette fragilité et a '
                            "mis parfaitement en lumière l'impossibilité pour cette équipe de "
                            'continuer à fonctionner de la sorte en comptant uniquement sur '
                            'leur dévouement et grâce à leur propre appel aux intervenants '
                            'majoritairement vacataires. Pourtant, depuis le premier '
                            'confinement, ils ont fait en sorte de toujours remplir leur '
                            "mission au détriment d'une organisation régulière et sûre du "
                            'travail des praticiens hospitaliers titulaires, au prix de '
                            'nombreux week-ends et jours fériés travaillés. Selon ces '
                            "praticiens, la direction de l'ARS, de son coté, se contente "
                            "uniquement d'assigner au travail les praticiens hospitaliers "
                            'titulaires. Cela est fait sans aucune prise en compte des '
                            'conditions de leur travail pris en charge antérieurement et '
                            'postérieurement à la période pour laquelle ils sont assignés, du '
                            'niveau de leur aptitude et de leur vigilance dans ce cadre, au '
                            'regard notamment, de la fatigue accumulée. En conséquence, ils '
                            'attendent de la direction de leur hôpital, disposant de la '
                            'prérogative de prendre toute mesure nécessaire à assurer '
                            "l'organisation d'un service minimum garantissant la sécurité "
                            'physique des personnes ainsi que la continuité des soins, de '
                            'pallier une insuffisance récurrente des effectifs. Désormais, '
                            'ils sont déterminés à défendre leurs revendications devant un '
                            'juge administratif et de dénoncer toutes les nouvelles '
                            'assignations qui leur seront délivrées dans le but de les '
                            'contraindre à une prise de poste uniquement pour pallier une '
                            "absence d'effectif suffisant. C'est pourquoi à la suite de sa "
                            'question écrite de 26 octobre 2021 et à ses courriers restants '
                            'sans réponse, il lui demande de lui faire savoir quelles mesures '
                            'il compte prendre pour répondre en urgence et de manière '
                            'efficace à cette situation désastreuse que doivent vivre ces '
                            'praticiens, applaudis par les citoyens, mais bafoués par un '
                            "système en quête uniquement de rentabilité ainsi qu'un Ségur de "
                            'la santé minimaliste.',
                'reponse': "SITUATION DES URGENTISTES DE L'HÔPITAL D'OLORON-SAINTE-MARIE <br "
                           '/><strong>M.\xa0le président. </strong>La parole est à M.\xa0Jean '
                           'Lassalle, pour exposer sa question, n° \xa01704, relative à la '
                           "situation des urgentistes de l'hôpital d'Oloron-Sainte-Marie.<br "
                           '/><br /><strong>M.\xa0Jean Lassalle. </strong>Je souhaite alerter '
                           'M.\xa0le ministre des solidarités et de la santé sur la situation '
                           'intolérable des praticiens du service des urgences du centre '
                           "hospitalier d'Oloron-Sainte-Marie dans ma circonscription. En "
                           'effet, soumis de façon récurrente, depuis plus de deux ans, au '
                           'problème des effectifs médicaux, au manque de titulaires, '
                           "d'internes et d'intérimaires, ces praticiens alertent sans cesse, "
                           "en vain, les services compétents de l'État, que ce soit le "
                           "ministère, la préfecture ou l'agence régionale de santé (ARS).<br "
                           "/><br />Dès le 11\xa0juin 2020, ils ont tenté d'appeler "
                           "l'attention, par courrier, sur les effectifs à venir et sur la "
                           'nécessité urgente de recruter de nouveaux praticiens hospitaliers '
                           'dans leur service, tout en expliquant la difficulté particulière '
                           "de ce recrutement et en proposant des axes d'amélioration "
                           'possibles. Différentes instances et acteurs de la vie publique, '
                           "dont le préfet, le sous-préfet et l'ARS, ont été de nouveau "
                           "alertés, mais aucune réponse n'a jamais été apportée. Ainsi, un "
                           "courrier sur ce sujet adressé à la direction de l'ARS en janvier "
                           '2021 est resté sans réponse.<br /><br />Par la suite, la menace '
                           'de la loi visant à améliorer le système de santé par la confiance '
                           'et la simplification, dite loi Rist, est venue renforcer cette '
                           'situation fragile et a mis parfaitement en lumière '
                           "l'impossibilité pour l'équipe de continuer à fonctionner de la "
                           "sorte, en ne comptant que sur son dévouement et sur l'appel à des "
                           'intervenants majoritairement vacataires. Selon les personnels '
                           "concernés, la direction de l'ARS se contente, de son côté, "
                           "d'assigner au travail les praticiens hospitaliers titulaires.<br "
                           "/><br />C'est pourquoi ils attendent de la direction de "
                           "l'hôpital, qui dispose de la prérogative de prendre toute mesure "
                           "nécessaire permettant d'assurer l'organisation d'un service "
                           'minimum garantissant la sécurité physique des personnes ainsi que '
                           "la continuité des soins, qu'elle pallie l'insuffisance récurrente "
                           'des effectifs.<br /><br />Pour aller droit au but, je souligne '
                           "qu'aucune mesure n'a été prise à ce jour et que le service des "
                           'urgences est fermé. En conséquence, la situation est désastreuse '
                           "pour la commune d'Oloron-Sainte-Marie, qui est au cœur d'un "
                           'bassin de 60\xa0000\xa0patients\xa0: une très grande inquiétude '
                           'règne sur le terrain.<br /><br /><strong>M.\xa0le président. '
                           "</strong>La parole est à Mme\xa0la secrétaire d'État chargée de "
                           'la biodiversité.<br /><br /><strong>Mme\xa0Bérangère '
                           "Abba,</strong><i> secrétaire d'État chargée de la biodiversité. "
                           '</i>La situation du service des urgences du centre hospitalier '
                           "d'Oloron-Sainte-Marie est en effet difficile. Elle se caractérise "
                           "d'abord par un nombre important d'intérimaires qui représentent "
                           "60\xa0% de l'équipe urgentiste, par un fonctionnement interne "
                           'marqué par de nombreuses tensions qui ont conduit à '
                           "l'intervention du directeur général et surtout par une "
                           'collaboration compliquée avec le centre hospitalier de Pau.<br '
                           "/><br />Ces différents facteurs sont à l'origine de la situation "
                           'de tension générale dont les pouvoirs publics sont pleinement '
                           'conscients. Nous parlons depuis 2018 avec les personnels des '
                           'urgences sur le terrain afin de créer cette équipe. Les points de '
                           "vue ont longtemps été très divergents, ce qui explique d'ailleurs "
                           'les tensions. Vous connaissez mieux que tout autre la situation, '
                           'monsieur le député, ainsi que les élus locaux, pour y être '
                           "attentif de longue date. L'ARS de la Nouvelle-Aquitaine est "
                           'pleinement mobilisée également sur ce dossier.<br /><br />Face '
                           'aux tensions rencontrées par le centre hospitalier en 2021 au '
                           "sein de la structure mobile d'urgence et de réanimation (SMUR), "
                           "notamment dans le contexte de l'épidémie de covid-19 et de la "
                           'démographie médicale locale, une assignation durant les fêtes de '
                           "fin d'année de 2021 a effectivement été décidée par le directeur "
                           "du centre hospitalier d'Oloron-Sainte-Marie, à la demande de "
                           "l'ARS, pour les raisons de sécurité que l'on imagine. Une réunion "
                           "a été organisée par la délégation départementale de l'ARS fin "
                           'janvier afin de travailler à une harmonisation des pratiques et '
                           'de rechercher des solutions pérennes. Les protagonistes semblent '
                           "désormais moins fermés et prêts à collaborer dans le cadre d'un "
                           "groupe de travail. Ces éléments attestent de l'engagement "
                           "constant de l'ARS de la Nouvelle-Aquitaine face à cette situation "
                           "particulièrement sensible. L'ensemble des acteurs concernés "
                           "doivent continuer de s'inscrire dans cette dynamique de "
                           "coopération renforcée et, grâce à la médiation de l'ARS, le cadre "
                           "d'un bon fonctionnement des services de soins dans le territoire "
                           'se dessine. Sachez que le ministère des solidarités et de la '
                           'santé y est évidemment très attentif.<br /><br /><strong>M.\xa0le '
                           'président. </strong>La parole est à M.\xa0Jean Lassalle.<br /><br '
                           "/><strong>M.\xa0Jean Lassalle. </strong>Compte tenu de l'état "
                           "d'urgence extrême, tout ce que le ministère pourra faire sera "
                           'bienvenu.<br />',
                'support': 'Journal officiel',
                'title': "SITUATION DES URGENTISTES DE L'HÔPITAL D'OLORON-SAINTE-MARIE "}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_16_qe_sr():
    file_path = "qp/assemblee_leg_16-qe-sr.html"
    expected = {'ASREP': 'Sans réponse',
                'aut': 'Maud Gatel',
                'dept': 'Paris',
                'dpq': '02/01/2024',
                'dpr': '',
                'groupe': 'MoDem et Indépendants)',
                'leg': '16',
                'ministere': 'Transition écologique et cohésion des territoires',
                'nature': 'Question écrite',
                'num': '14248',
                'pgq': '40',
                'pgr': '',
                'question': "Mme Maud Gatel appelle l'attention de M. le ministre de la "
                            'transition écologique et de la cohésion des territoires sur '
                            "l'impact du secteur d'activité de la livraison expresse à "
                            "domicile sur l'empreinte environnementale française. Grâce aux "
                            'dispositions de la loi LOM, les flottes des entreprises se '
                            'verdissent. Le secteur de la livraison expresse à domicile étant '
                            'dominé par des plateformes faisant appel à des travailleurs dits '
                            "indépendants n'est pas concerné par ces obligations. En effet, "
                            'les livreurs indépendants utilisent leur propre véhicule et leur '
                            'statut interroge quant à la possibilité pour les plateformes de '
                            "leur imposer l'usage de véhicules propres. Ainsi, Mme la députée "
                            'souhaite-t-elle interroger M. le ministre de la transition '
                            'écologique et de la cohésion des territoires sur les '
                            'dispositions envisagées afin de mieux intégrer ce secteur aux '
                            'réglementations existantes.',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Verdissement des flottes dans le secteur de livraison expresse à '
                         'domicile'}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_16_qe_ar():
    file_path = "qp/assemblee_leg_16-qe-ar.html"
    expected = {'ASREP': 'Avec réponse',
                'aut': 'Hubert Brigand',
                'dept': "Côte-d'Or",
                'dpq': '12/12/2023',
                'dpr': '02/01/2024',
                'groupe': 'Les Républicains',
                'leg': '16',
                'ministere': 'Enseignement et formation professionnels',
                'nature': 'Question écrite',
                'num': '13641',
                'pgq': '11081',
                'pgr': '90',
                'question': "M. Hubert Brigand attire l'attention de Mme la ministre déléguée "
                            "auprès du ministre du travail, du plein emploi et de l'insertion "
                            "et du ministre de l'éducation nationale et de la jeunesse, "
                            "chargée de l'enseignement et de la formation professionnels, sur "
                            "les conséquences pour le secteur de l'artisanat, et donc pour "
                            "l'économie de proximité, de la baisse moyenne globale de 5 % du "
                            "niveau de prise en charge des contrats d'apprentissage. En "
                            "effet, proposée par l'opérateur France compétences et confirmée "
                            'par un décret ministériel, cette décision pourrait avoir pour '
                            'conséquence de fragiliser fortement la formation par '
                            'apprentissage, notamment dans les centres de formation des '
                            'apprentis (CFA) du réseau des chambres des métiers et de '
                            "l'artisanat (CMA), au point qu'une quinzaine des CAP (boucher, "
                            'boulanger, coiffeur, mécanicien automobile...) auront rapidement '
                            'à connaître une situation très dégradée. Dans ces conditions, '
                            'les CFA ne pourront pas durablement former « à perte » en '
                            'supportant le coût de formations déficitaires et risqueront de '
                            'fermer des sections de formation. Cela signifie très '
                            "concrètement qu'il y aura moins d'apprentis formés dans "
                            "l'artisanat. C'est pourquoi les CMA souhaitent qu'une nouvelle "
                            'méthode de calcul du niveau de prise en charge des contrats '
                            "d'apprentissage puisse être négociée au plus vite, sans attendre "
                            "l'issue de concertations qui doivent prochainement s'ouvrir pour "
                            "l'après 2025. Compte tenu de l'enjeu prioritaire qu'est le "
                            "développement de l'apprentissage en France, il lui demande de "
                            'bien vouloir lui indiquer comment il entend répondre à cette '
                            'demande.',
                'reponse': "L'apprentissage constitue une réponse efficace et concrète aux "
                           'tensions de recrutement que rencontrent de nombreuses entreprises '
                           'partout sur le territoire, y compris dans le secteur de '
                           "l'artisanat, historiquement porté sur cette voie d'entrée dans "
                           'les métiers. Depuis 2018, le Gouvernement a considérablement '
                           'favorisé son développement, en lui consacrant des moyens '
                           "exceptionnels. D'abord pour les jeunes bien sûr, à travers la "
                           "garantie d'une formation gratuite et de qualité, mais également "
                           'pour toutes les entreprises, notamment les très petites '
                           'entreprises - petites et moyennes entreprises, à travers la '
                           "création d'une aide à l'embauche d'alternants, qui permet de "
                           "maintenir une dynamique d'entrée en apprentissage importante dans "
                           'notre pays. Conformément à la loi du 5\xa0septembre\xa02018 pour '
                           "la liberté de choisir son avenir professionnel, l'Etat, grâce à "
                           "son opérateur France compétences, est chargé d'assurer un travail "
                           "de régulation des niveaux de financement de l'apprentissage, afin "
                           "d'en assurer la pérennité et de garantir un usage efficient des "
                           'fonds mutualisés des entreprises. Ce travail de régulation repose '
                           "sur l'analyse annuelle des données de la comptabilité analytique "
                           "des Centres de formation d'apprentis (CFA), qui permet de "
                           "déterminer les coûts réels de formation, afin d'en adapter le "
                           'niveau de financement. A ce titre, il est de la responsabilité '
                           'des pouvoirs publics, et notamment de la mission de régulation de '
                           'France compétences, de garantir un juste niveau de financement au '
                           'regard des coûts réels constatés. La baisse des niveaux de prise '
                           "en charge ne s'inscrit donc pas dans une logique stricte "
                           "d'économie mais bien dans une démarche de fixation du juste prix, "
                           'en responsabilité vis-à-vis de nos finances publiques. De fait, '
                           'la méthode de régulation mise en place lors de cet exercice prend '
                           "en compte les effets de l'inflation (de 5,2\xa0% en 2022 selon "
                           "l'Insee), puisqu'afin de fixer sa valeur maximale recommandée, "
                           "France compétences a appliqué à l'ensemble des coûts moyens de "
                           'formation constatés dans les CFA et par certification, une hausse '
                           "de 10\xa0%. Aucune baisse n'est intervenue en dessous de cette "
                           'valeur. A cette première garantie quant à la préservation des '
                           "équilibres économiques des CFA est venue s'ajouter une seconde "
                           "garantie, puisqu'il a été acté que, pour les niveaux de prise en "
                           "charge définis par les branches, l'Etat n'imposerait aux branches "
                           'aucune baisse au-delà de 10\xa0% pour une formation donnée, et ce '
                           'même si pour certaines formations, les écarts constatés '
                           'excédaient largement ce taux. Dans le respect de ces principes, '
                           'le référentiel de France compétences organise une diminution de '
                           '5% en moyenne des niveaux de prise en charge des contrats '
                           "d'apprentissage conclus à compter du 8\xa0septembre\xa02023. En "
                           'complément, le Gouvernement a souhaité préserver la capacité de '
                           "l'appareil de formation à former des apprentis sur les métiers "
                           'transverses, sur lesquels les branches professionnelles avaient '
                           'été peu nombreuses à proposer des valeurs, et auxquelles étaient '
                           'appliquées les valeurs de carence, dont certaines accusaient des '
                           'baisses importantes. Parce que ces métiers sont essentiels au '
                           'développement économique de nombreuses entreprises [dont celles '
                           "de l'artisanat], le Gouvernement a réhaussé les valeurs de "
                           'carence en limitant la baisse au maximum à 10\xa0% par rapport '
                           'aux valeurs de 2022. Le Gouvernement a conscience de la '
                           "complexité du système de régulation actuel. C'est en ce sens que "
                           'celui-ci est ouvert au dialogue avec les acteurs de '
                           "l'apprentissage dont les réseaux représentants des CFA, et "
                           "notamment les chambres des métiers et d'artisanat, afin "
                           "d'envisager les pistes d'amélioration de ce processus. Une large "
                           "consultation sera organisée en ce sens en début d'année 2024. "
                           'Ainsi, le Gouvernement maintient-il son engagement majeur en '
                           "faveur de l'apprentissage, tout en conduisant des mesures en "
                           'faveur de la rationalisation du fonctionnement des centres de '
                           "formation des apprentis qui participent à l'objectif de "
                           "soutenabilité du système de financement de l'alternance, gage de "
                           "sa pérennité, avec pour objectif d'atteindre un million de "
                           "nouveaux apprentis par an dans notre pays d'ici la fin du "
                           'quinquennat.',
                'support': 'Journal officiel',
                'title': "Baisse du niveau de prise en charge des contrats d'apprentissage"}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def test_parse_ass_16_qg():
    file_path = "qp/assemblee_leg_16-qg.html"
    expected = {'ASREP': 'Question au Gouvernement',
                'aut': 'Mereana Reid Arbelot',
                'dept': 'Polynésie Française',
                'dpq': '30/11/2023',
                'dpr': '30/11/2023',
                'groupe': 'Gauche démocrate et républicaine - NUPES',
                'leg': '16',
                'ministere': 'Enseignement et formation professionnels',
                'nature': 'Question au Gouvernement',
                'num': '1398',
                'pgq': '',
                'pgr': '10679',
                'question': '</p><p align="CENTER"> EXTINCTION DE L\'INDEMNITÉ TEMPORAIRE DE '
                            'RETRAITE <a name=PG10></a> </p><br><strong>Mme\xa0la présidente. '
                            '</strong>La parole est à Mme\xa0Mereana Reid\xa0'
                            'Arbelot.<br><br><strong>Mme\xa0Mereana Reid\xa0Arbelot. '
                            "</strong>Alors qu'on dénonce la paupérisation des retraités "
                            'ultramarins de la fonction publique en Polynésie française, en '
                            'Nouvelle-Calédonie et à Wallis-et-Futuna, la réponse du '
                            "Gouvernement est de s'attaquer au pouvoir d'achat des actifs en "
                            'leur proposant un dispositif de capitalisation sur 100\xa0% de '
                            'la part majorée de leur traitement indiciaire. Pour tout '
                            'fonctionnaire actif, des retenues sont prélevées sur le '
                            "traitement afférent à l'indice hiérarchique détenu dans son "
                            "emploi pour qu'il puisse obtenir une pension civile en rapport "
                            "avec ce traitement indiciaire.<br><br>En application d'un "
                            'article de la loi de finances rectificative de 1974, les '
                            'retenues au titre de la pension civile et de la sécurité sociale '
                            'sont prélevées également sur la part majorée du traitement '
                            'indiciaire des fonctionnaires ultramarins du Pacifique. '
                            "Toutefois, leur pension civile n'était calculée que sur le "
                            'traitement indiciaire de base, sans la part majorée, car '
                            "l'indemnité temporaire de retraite (ITR) venait compenser ce "
                            'manque.<br><br>En 2008, le Gouvernement a souhaité mettre fin à '
                            "l'effet d'aubaine dont profitaient certains fonctionnaires pour "
                            "bénéficier d'une retraite indexée au soleil alors qu'ils "
                            "n'avaient jamais ou très peu exercé en outre-mer. Il a donc "
                            "décidé de programmer l'extinction de l'ITR sur vingt ans, "
                            'promettant de travailler à un dispositif de substitution. Nous y '
                            "sommes\xa0!<br><br>L'amendement no\xa01404 au projet de loi de "
                            'finances pour 2024 impose un dilemme\xa0: un choix de '
                            "capitalisation exclusif, dont l'assiette, de 100\xa0%, n'est pas "
                            'modulable et dont la suspension, même temporaire –\xa0pour '
                            'passer un moment difficile, par exemple\xa0–, est impossible. Le '
                            'fonctionnaire du Pacifique a quelques mois pour prendre une '
                            "décision qui s'appliquera tout au long de sa "
                            'carrière.<br><br>Les 11\xa0500\xa0fonctionnaires du Pacifique se '
                            'voient prélever des retenues au titre de la pension civile sur '
                            "la totalité de leur traitement indiciaire, c'est-à-dire le "
                            'traitement de base et sa part majorée. Pourquoi la pension '
                            'civile des 280\xa0nouveaux retraités annuels du Pacifique ne se '
                            'fonde-t-elle pas sur la totalité de leur traitement '
                            'indiciaire\xa0? <i>(Applaudissements sur les bancs du groupe '
                            'GDR-NUPES.)</i><br><br><strong>M.\xa0Jean-Paul Lecoq.</strong> '
                            "Ça, c'est du concret\xa0!<br><br><strong>Mme\xa0la présidente. "
                            '</strong>La parole est à Mme\xa0la ministre déléguée chargée de '
                            'l’enseignement et de la formation '
                            'professionnels.<br><br><strong>Mme\xa0Carole '
                            'Grandjean,</strong><i> ministre déléguée chargée de '
                            'l’enseignement et de la formation professionnels. </i>Vous '
                            "interrogez le Gouvernement sur les conséquences de l'extinction "
                            "progressive de l'indemnité temporaire de retraite. Je profite de "
                            "votre question pour saluer, au nom du Gouvernement, l'engagement "
                            "des agents publics en Polynésie et dans l'ensemble de nos "
                            "territoires ultramarins.<br><br>L'ITR est un dispositif "
                            "dérogatoire pour les fonctionnaires de l'État qui décideraient "
                            'de prendre leur retraite dans certains territoires ultramarins. '
                            "Ce dispositif comportait de nombreuses limites. C'est pourquoi, "
                            'depuis quinze ans, les gouvernements successifs ont décidé son '
                            'extinction progressive. Nous ne reviendrons pas sur cette '
                            'décision.<br><br>Toutefois, nous sommes bien conscients des '
                            "conséquences de la fin de l'ITR sur le pouvoir d'achat des "
                            "agents. C'est pourquoi le Président de la République a souhaité "
                            "qu'un nouveau dispositif s'y substitue, élaboré en concertation "
                            'avec les élus et les partenaires sociaux. Nous sommes partis '
                            "d'un constat simple\xa0: si les écarts entre le coût de la vie "
                            "dans l'Hexagone et le Pacifique sont bien pris en compte pendant "
                            "la vie active de l'agent, grâce à une indexation de la "
                            "rémunération, tel n'est pas le cas lors de leur départ à la "
                            "retraite.<br><br>C'est pourquoi M.\xa0Guérini, dont je vous prie "
                            "d'excuser l'absence –\xa0il est à l'étranger\xa0–, a proposé un "
                            "dispositif qui permet à un agent de la fonction publique d'État "
                            "ou à un militaire de surcotiser sur l'ensemble des compléments "
                            'de rémunération perçus dans ces territoires au régime de la '
                            "retraite additionnelle de la fonction publique. Pour s'assurer "
                            "que l'adhésion à ce dispositif aura un effet immédiat, un "
                            'montant plancher est prévu\xa0: aucun agent ne pourra percevoir '
                            "moins de 4\xa0000\xa0euros par an.<br><br>Alors qu'aucune "
                            "solution n'avait été définie depuis plus de quinze ans, nous "
                            'agissons concrètement pour déployer des solutions adaptées aux '
                            "retraités ultramarins tout en maintenant les principes d'équité "
                            'et de contributivité qui fondent notre système de retraites.<br>',
                'reponse': '',
                'support': 'Journal officiel',
                'title': 'Extinction de l’indemnité temporaire de retraite'}

    buffer = read_file(file_path).decode("utf-8")
    parser = AssembleeParser(buffer)

    assert parser.data == expected


def read_file(path):
    current_directory = os.getcwd()
    directory_path = "." if os.path.basename(current_directory) == "tests" else "tests"
    path = os.path.join(directory_path, path)
    with open(path, 'rb') as file_pointer:
        buffer = file_pointer.read()

    return buffer
