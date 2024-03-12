import os

from mod.europresse import format_support_name, EuropresseHtmlParser, EuropresseProsperoFileWriter, \
    strip_tags_with_class, fetch_date, in_tag, create_txt_content, create_ctx_content
from mod.file_utils import name_file
from tests.utils import free_directory, delete_directory


def test_europresse_e2e():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
    else:
        directory_path = "tests"

    free_directory(directory_path)

    to_parse = os.path.join(directory_path, "europresse/pesquet_19-11-21_a_26-10-23.HTML")
    parser = EuropresseHtmlParser(to_parse)
    assert len(parser.articles) == 305
    assert len(parser.parsed_articles) == 292

    EuropresseProsperoFileWriter(parser.parsed_articles[0], directory_path)

    txt_to_compare = os.path.join(directory_path, "europresse/EUROPRESSE20231023A.txt")
    with open(txt_to_compare, "r", encoding='cp1252') as expected:
        expected_txt = expected.read()
    txt_generated = os.path.join(directory_path, "EUROPRESSE20231023A.txt")
    with open(txt_generated, "r", encoding='cp1252') as result:
        generated_txt = result.read()

    assert expected_txt == generated_txt

    ctx_to_compare = os.path.join(directory_path, "europresse/EUROPRESSE20231023A.ctx")
    with open(ctx_to_compare, "r", encoding='cp1252') as expected:
        expected_lines = expected.readlines()
    ctx_generated = os.path.join(directory_path, "EUROPRESSE20231023A.ctx")
    with open(ctx_generated, "r", encoding='cp1252') as result:
        result_lines = result.readlines()

    assert expected_lines[0:10] == result_lines[0:10]

    free_directory(directory_path)


def test_format_support_name():
    support_with_parenthesis = "Le Monde (site web)"
    assert format_support_name(support_with_parenthesis) == "Le Monde"

    support_with_comma = "Le Point.fr, no. 202202"
    assert format_support_name(support_with_comma) == "Le Point.fr"

    support_with_tag = "Ouest-France                <br />Vannes ; Auray ; Ploërmel"
    assert format_support_name(support_with_tag) == "Ouest-France"


def test_strip_tags_with_class():
    result = strip_tags_with_class("<foo class='bar'>something</foo>")
    assert result == "something"


def test_fetch_date():
    result = fetch_date("lundi 16 octobre 2023 - 16:55:20 -0000 1017 mots")
    assert result == "16/10/2023"


def test_in_tag():
    tag = "DocPublicationName"
    html_source = """<span class="DocPublicationName">Le Journal des Femmes (site web)</span>"""
    result = in_tag(html_source, tag)

    assert result == "Le Journal des Femmes (site web)"


def test_parse_article():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
    else:
        directory_path = "tests"
    to_parse = os.path.join(directory_path, "europresse/pesquet_19-11-21_a_26-10-23.HTML")
    parser = EuropresseHtmlParser(to_parse)
    result = parser.parsed_articles[0]
    expected = {'source': 'Le Journal des Femmes',
                'date': '23/10/2023',
                'title': 'Thomas Pesquet, gêné par sa notoriété : "c\'est devenu beaucoup plus compliqué"',
                'narrator': False,
                'subtitle': False,
                'text': '<p><mark>Thomas</mark> <mark>Pesquet</mark>, gêné par sa notoriété\xa0: "c\'est devenu '
                        'beaucoup plus compliqué" </p> <p> Charlotte Gainsbourg "en manque", Pierre Arditi "condamné '
                        'à rester enfermé"... </p> <p> Pause </p> <p><mark> Thomas</mark> <mark>Pesquet</mark> '
                        '©\xa0Zabulon Laurent/ABACARevers de la médaille. Quand il est revenu sur terre en 2017 après '
                        'sa première mission spatiale, <mark>Thomas</mark> <mark>Pesquet</mark> aspirait à retrouver '
                        'une vie normale mais il s\'est rendu compte que sa soudaine célébrité allait changer sa vie. '
                        '"J\'ai toujours mon salaire de l\'Agence spatiale, je prends le train, j\'appelle le '
                        'plombier quand j\'ai un problème, je fais mes courses au supermarché du coin (....) Mais '
                        'c\'est vrai que c\'est devenu beaucoup plus compliqué", a expliqué le spationaute de 45 ans '
                        'à La Tribune Dimanche.\xa0</p>\n\n\n\n\n<p>[Additional Text]: </p> <p> Revers de la '
                        'médaille. Quand il est revenu sur terre en 2017 après sa première mission spatiale, '
                        'Thomas Pesquet aspirait à retrouver une vie normale mais il s\'est rendu compte que sa '
                        'soudaine célébrité allait changer sa vie. "J\'ai toujours mon salaire de l\'Agence spatiale, '
                        'je prends le train, j\'appelle le plombier quand j\'ai un problème, je fais mes courses au '
                        'supermarché du coin (....) Mais c\'est vrai que c\'est devenu beaucoup plus compliqué", '
                        'a expliqué le spationaute de 45 ans à La Tribune Dimanche.\xa0 </p> <p> Bien dans sa peau. '
                        'Agée de 48 ans, Cécile de France n\'a pas du tout l\'intention d\'avoir recours à la '
                        'chirurgie esthétique pour effacer les signes de l\'âge. "Je ne toucherai jamais à mon visage '
                        '(....)\xa0je trouve important de le montrer à toutes les spectatrices pour qu\'elles '
                        'puissent s\'identifier, que mon personnage résonne en elles, qu\'elles se reconnaissent dans '
                        'un vrai être humain qui vieillit normalement, en assumant complètement son âge", a expliqué '
                        'la comédienne sur RTL.\xa0 </p> <p> Liens solides. Séparé du père de son fils Elliot, 8 ans, '
                        'depuis 5 ans, Alex Goude a gardé de très bonnes relations avec lui et avec son nouveau '
                        'compagnon ! "On ne s\'est pas séparés fâchés (...)\xa0On s\'est éloignés mais contrairement '
                        'à ce qui a été dit, il n\'est pas parti avec le jardinier (rires) (....)\xa0Son nouveau mari '
                        's\'appelle Junior, il habite la maison à côté et pour le bien d\'Elliot, on a réussi à '
                        'instaurer une vraie relation d\'amitié", a confié l\'animateur de 48 ans à Public </p> <p> '
                        'Contre mauvaise fortune bon coeur. L\'élection de Miss Monde\xa0devait avoir lieu le '
                        '16\xa0décembre prochain à New Delhi, en Inde mais elle a été reportée au 2\xa0mars '
                        '2024\xa0pour des raisons politiques. Un changement qui ne perturbe pas plus que cela '
                        'Clémence Botino, Miss France 2020, qui représentera la France lors de ce concours. '
                        '"Honnêtement dans ma carrière de Miss j\'ai connu de nombreuses péripéties, je suis plus ou '
                        'moins habituée (...) Parfois j\'ai l\'impression d\'être dans une série Netflix, '
                        'on attend l\'épisode final depuis trop longtemps. Les saisons sont trop longues haha. \'Une '
                        'vie de Miss…\' Vous aimez le titre\xa0?!", a écrit, avec humour, l\'ancienne reine de beauté '
                        'âgée de 26 ans sur Instagram.\xa0 </p> <p> Rupture. Mariée avec\xa0Dom Gummer depuis 45 ans, '
                        'Meryl Streep ne partagerait plus le même toit que le père de ses enfants (Henry, 44 ans,'
                        '\xa0 Mamie, 40 ans, Grace, 37 ans,\xa0 et Louisa, 32 ans). "(Cela fait) six ans que le '
                        'couple vit séparément (....) Même s\'ils tiennent l\'un à l\'autre, ils ont décidé de se '
                        'séparer", a confié un proche à Page Six. </p> <p> Chapitre clos. Après Nicolas Anselmo ('
                        'Eliott), Fabian Wolfrom (Louis), Thomas Da Costa (Axel) ou encore Pola Petrenko (Charlène),'
                        '\xa0Agustin Galiana a annoncé qu\'il quittait la série la série\xa0Ici tout commence où il '
                        'interprétait le rôle de Lisandro depuis trois ans. "Une quotidienne, ça prend beaucoup de '
                        'temps et cela m\'a empêché de prendre part à d\'autres projets. J\'ai passé trois saisons de '
                        'rêve dans la peau de Lisandro, à travailler comme un malade avec les copains. Mais c\'est le '
                        'moment pour moi de m\'envoler et de partir sur de nouveaux projets", a confié le comédien de '
                        '45 ans à\xa0Télé Star. </p> <p> Entre de bonnes mains. Le 18\xa0octobre dernier, '
                        'Salvatore Adamo a dû annuler son concert organisé au Grand Rex en raison d\'un souci de '
                        'santé. Le chanteur de 79 ans a présenté ses excuses à ses fans et a tenu à leur donner des '
                        'explications concernant la cause de ce report. "Je me suis retrouvé avec un problème '
                        'préoccupant qui pouvait mener à un autre plus grave. J\'ai eu la sagesse d\'écouter mes '
                        'proches et mes docteurs, que je remercie de leur dévouement total. J\'ai fait ce qu\'ils '
                        'm\'ont conseillé pour vous revenir en forme", a écrit Salvatore Adamo sur Facebook. </p> <p> '
                        'Disparition. Il y a quelques jours, Cindy Sander a perdu sa mère et peine à surmonter son '
                        'immense tristesse. L\'ancienne candidate de la Nouvelle Star âgée de 45 ans a publié une '
                        'vidéo dans laquelle elle chante la célèbre chanson de Serge Lama "Je suis malade". "Maman, '
                        'donne-moi ta force (....) Chaque nouveau jour est encore plus dur que la veille", '
                        'écrit-elle en légende. </p> <p> Régions mises en avant. Comme son ami le poète Francis '
                        'Sicre, Francis Cabrel regrette le monopole parisien en matière culturelle et aimerait que le '
                        'ministère de la Culture s\'installe "à Toulouse ou à Lyon ou à Lille !". "Pourquoi tout est '
                        'à l\'intérieur du périphérique\xa0?", a ainsi regretté, dans\xa0l\'émission 1h avec sur RFM, '
                        'le chanteur de 69 ans qui vit à Astaffort\xa0dans le département du Lot-et-Garonne. </p> <p> '
                        'Comptes à rendre. Selon Le Parisien,\xa0Vincent Cerutti a été mis en examen le '
                        '6\xa0septembre dernier pour agression sexuelle pour des faits qui remontent à 2015. Une '
                        'ancienne standardiste de Chérie FM accuserait l\'animateur de 41 ans d\'avoir tenu des '
                        'propos déplacés et de l\'avoir mordue au niveau des fesses deux fois ! La jeune femme a '
                        'déposé une plainte en 2017 qui a été classée sans suite puis a de nouveau porté '
                        'plainte\xa0en mai 2020\xa0avec constitution de partie civile, déclenchant l\'ouverture '
                        'd\'une instruction judiciaire. Ces faits sont démentis par Vincent Cerutti qui, par le biais '
                        'de ses avocats, évoque un "jeu stupide mais réciproque". </p> <p> Critiques véhémentes. '
                        'Laura Smet n\'a rien contre la médecine et la chirurgie esthétique mais regrette que '
                        'certaines jeunes filles en abusent. "C\'est utile. Cela donne confiance. Mais quand dans mon '
                        'casting je repère des gamines de 18\xa0ans déjà refaites, cela me désole. Ce n\'est pas que '
                        'c\'est moche, c\'est qu\'elles font dix fois plus âgées. Quel dommage\xa0!", a confié la '
                        'comédienne de 39 ans à Madame Figaro. </p> <p> Risques du métier. Le tournage du '
                        'film\xa03\xa0Jours max n\'a pas été de tout repos pour Tarak Boudali qui s\'est blessé assez '
                        'sérieusement ! "Je\xa0me suis fêlé deux côtes sur ce film et je me suis déboîté le genou", '
                        'a confié,\xa0dans l\'émission Le Bon Dimanche Show sur RTL, le comédien réalisateur de 43 '
                        'ans qui s\'est fait mal lors d\'une scène où il devait être compressé par une machine ! </p> '
                        '<p> Trou noir. En 2002, Britney Spears a très mal vécu la fin de son histoire d\'amour avec '
                        'Justin Timberlake qui aurait, selon une rumeur persistante, rompu avec elle par SMS. "J\'ai '
                        'été dévastée (...)\xa0J\'étais dans le coma en Louisiane et il courait joyeusement à '
                        'Hollywood", écrit la chanteuse de 41 ans\xa0dans son autobiographie The Woman In Me dont des '
                        'extraits ont été révélés dans la presse américaine. </p> <p> Marqué au fer rouge. Le '
                        '8\xa0novembre 2013 a eu lieu une explosion accidentelle pendant les répétitions du spectacle '
                        '1789, les amants de la Bastille qui a provoqué la mort du directeur technique du spectacle., '
                        'Marcus Toledano Une quinzaine de personnes, dont cinq grièvement, ont également été '
                        'blessées. Un drame qui a marqué à jamais Dove Attia, le producteur du spectacle. "Je vous '
                        'avoue que… ça a été terrible… J\'en garde un traumatisme\xa0: je ne l\'oublierai jamais ('
                        '...) C\'est (Marcus Toledano) quelqu\'un qu\'on a fait grandir et… Il est mort avec ma main '
                        'dans la sienne à 5\xa0heures du matin", a raconté l\'ancien membre du jury de La Nouvelle '
                        'Star âgé de 66 ans sur le plateau de C à Vous. </p> <p> Changement d\'identité. Plus Belle '
                        'La Vie fait peau neuve. Diffusée à partir de décembre sur TF1 en lieu et place de France 3, '
                        'la célèbre série marseillaise va aussi changer de nom ! D\'après le journaliste\xa0Clément '
                        'Garin, elle s\'appellera\xa0Mi3stral du nom légèrement modifié du mythique bar du Mistral '
                        'comme le révèlent les CV des acteurs.\xa0 </p> <p> Rôle de composition. Invitée dans '
                        'l\'émission Culture Médias sur Europe 1\xa0\xa0pour évoquer Trash, une série sur les '
                        'coulisses de Loft Story, qui sera diffusée sur Prime Video,\xa0Alexia Laroche-Joubert a '
                        'expliqué qu\'elle y apparaîtra ! "Je dévoile un truc, c\'est que j\'ai demandé à faire un '
                        'rôle symbolique pour moi, donc le rôle symbolique, c\'est au CSA, comme ils m\'ont quand '
                        'même bien emmerdé, je trouvais ça assez drôle d\'être dans le CSA", a confié la productrice '
                        'de 53 ans.</p>\n    \n\n            <a '
                        'href="https://www.journaldesfemmes.fr/people/magazine/2956101-infos-people-france-octobre'
                        '-2023-quatrieme-semaine/2956147-thomas-pesquet" target="_blank"> Cet article est paru dans '
                        'Le Journal des Femmes (site web) - Journal des Femmes</a>\n        <p />'}

    assert result["source"] == expected["source"]
    assert result["date"] == expected["date"]
    assert result["subtitle"] == expected["subtitle"]
    assert result["narrator"] == expected["narrator"]
    assert result["title"] == expected["title"]
    assert result["text"] == expected["text"]


def test_europresse_html_parser():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
    else:
        directory_path = "tests"

    to_parse = os.path.join(directory_path, "europresse/pesquet_19-11-21_a_26-10-23.HTML")
    parser = EuropresseHtmlParser(to_parse)

    assert len(parser.articles) == 305
    assert len(parser.parsed_articles) == 292


def test_create_txt_content():
    article = {"title": 'A title', "subtitle": "A subtitle", "text": "Lorem ipsum"}
    expected = 'A title\r\n.\r\nA subtitle\r\n.\r\nLorem ipsum'
    result = create_txt_content(article)

    assert result == expected


def test_create_ctx_content():
    article = {"title": 'A title', "date": "02/01/2024"}
    source = "The world publication"
    source_type = "Magazine"

    ctx = [
        "fileCtx0005",
        article['title'],
        source,
        "",
        "",
        article['date'],
        source,
        source_type,
        "",
        "",
        "",
        "Processed by Tiresias on ",
        "",
        "n",
        "n",
        ""
    ]

    expected = "\r\n".join(ctx)
    result = create_ctx_content(article, source, source_type)

    assert result[0 - 10] == expected[0 - 10]
    assert result[10].find("Processed by Tiresias on ")


def test_strip_metata_title_field():
    current_directory = os.getcwd()
    if os.path.basename(current_directory) == "tests":
        directory_path = "."
    else:
        directory_path = "tests"

    to_parse = os.path.join(directory_path, "europresse/europresse_with_extra_lines_in_title.HTML")
    parser = EuropresseHtmlParser(to_parse)

    article = parser.parsed_articles[0]

    assert article["title"] == "JO 2022/ Snowboard La médaillée olympique Chloé Trespeuch est de retour à la maison"
