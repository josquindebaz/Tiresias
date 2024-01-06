import re
from dataclasses import asdict

from mod.QpData import QpData


def parse_assemblee_legislature(html):
    patterns = [
        r'<NLEG>(?P<m2>\d+)</NLEG>',
        r'<header class="question_legislature">(?P<m3>\d+)',
        r'<td class="tdstyleh1">(?P<m4>\d+)'
    ]

    pattern_combined = re.compile('|'.join(patterns))
    match = pattern_combined.search(html)

    return match.group(match.lastgroup)


def parse_assemblee_question_number(html, qp_data):
    question_number = ""
    question_nature = ""

    motif_type_1 = re.compile('<NUM>(.*)</NUM>')
    motif_type_2 = re.compile('question_col10">(.*)</div>')
    motif_type_3 = re.compile(r"Question\s*N.*\s*:\s*<b>(\d*)</b>")

    if motif_type_1.search(html):
        natures = {
            'QE': 'Question écrite',
            'QG': 'Question au Gouvernement',
            'QOSD': 'Question orale sans débat',
        }

        nat = re.search('<NAT>(.*)</NAT>', html).group(1)
        question_nature = natures[nat]

        question_number = motif_type_1.search(html).group(1)

    elif motif_type_2.search(html):
        m2_occurrences = motif_type_2.findall(html)
        question_number = re.search(r' Question N\S* (\d*)', m2_occurrences[0]).group(1)
        question_nature = m2_occurrences[1]

    elif motif_type_3.search(html):
        question_number = motif_type_3.search(html).group(1)
        question_nature = re.search(r'<td class="tdstyleh3">\s*<b>(.*)</b>', html).group(1)

    qp_data.num = question_number
    qp_data.set_question_nature(question_nature)

    return qp_data


def parse_assemblee_author(html, qp_data):
    aut = ""
    groupe = ""
    dept = ""

    m1 = re.compile('<AUT>(.*) (.*)</AUT>')
    m2 = re.compile(r'<div id="question_col80"> de.*>(.*)</a>.*\((.*) - <span>(.*)</span>')
    m3 = re.compile('<td class="tdstyleh3">de(.*)')

    if m1.search(html):
        aut = m1.search(html).group(1)
        groupe = re.search('<GROUPE>(.*)</GROUPE>', html).group(1)
        dept = re.search('<DEPT>(.*)</DEPT>', html).group(1)
    elif m2.search(html):
        aut, groupe, dept = m2.search(html).group(1, 2, 3)
    elif m3.search(html):
        depute = m3.search(html).group(1)
        aut, groupe, dept = re.search(r"<b>(.*)</b> \(\s*(.*) - (.*).\)",
                                      depute).group(1, 2, 3)

    aut = re.sub(r"^(M\.|Mme) ", "", aut)

    qp_data.aut = aut
    qp_data.groupe = groupe
    qp_data.dept = dept

    return qp_data


def parse_assemblee_ministere(html):
    m1 = re.compile('<MINA>(.*)</MINA>')
    m2 = re.compile('Ministère attributaire > </span>(.*)')
    m3 = re.compile('Minist.*re attributaire &gt; <span class="contenu">(.*)</span>')
    if m1.search(html):
        return m1.search(html).group(1)
    elif m2.search(html):
        return m2.search(html).group(1).strip()
    elif m3.search(html):
        return m3.search(html).group(1)

    return ""


def parse_assemblee_title(html):
    m1 = re.compile('<TANA>(.*)</TANA>')
    m2 = re.compile('Titre > </span>(.*)</p>')
    m3 = re.compile('>Analyse &gt; <span class="contenu">(.*)</span>')

    if m1.search(html):
        return m1.search(html).group(1)
    elif m2.search(html):
        return m2.search(html).group(1)
    elif m3.search(html):
        return m3.search(html).group(1)

    return ""


def parse_assemblee_publication(html):
    m1 = re.compile('<DPQ>(.*)</DPQ>')
    m2 = re.compile(r"Question publi\S* au JO le")
    if m1.search(html):
        dpq = m1.search(html).group(1)
        pgq = re.search('<PGQ>(.*)</PGQ>', html).group(1)
        return dpq, pgq
    elif m2.search(html):
        spl = re.split("</div>", m2.split(html)[1])[0]
        dpq = re.search(r"(\d{2}/\d{2}/\d{4})", spl).group(1)
        m_pgq = re.compile(r'page.*>(\d+)<')
        if m_pgq.search(spl):
            pgq = m_pgq.search(spl).group(1)
        else:
            pgq = ""
        return dpq, pgq
    else:
        return "", ""


def parse_assemblee_publication_response(html):
    m1 = re.compile(r'<DPR>(\d{2}/\d{2}/\d{4})</DPR>')
    m2 = re.compile("Réponse publiée au JO le")
    if m1.search(html):
        dpq = m1.search(html).group(1)
        pgq = re.search('<PGREP>(.*)</PGREP>', html).group(1)
        return dpq, pgq
    elif m2.search(html):
        spl = re.split("</div>", m2.split(html)[1])[0]
        dpr = re.search(r"(\d{2}/\d{2}/\d{4})", spl).group(1)
        m_pgr = re.compile(r'page.*>(\d+)<')
        if m_pgr.search(spl):
            pgr = m_pgr.search(spl).group(1)
        else:
            pgr = ""
        return dpr, pgr

    return "", ""


def parse_assemblee_question_text(html):
    m1 = re.compile('<QUEST>')
    m2 = re.compile(r'<h3>Texte de la question</h3>\s*<p>')
    m3 = re.compile(r'<h2> Texte de la question</h2>\s*.*<div class="contenutexte">\s*')
    if m1.search(html):
        question = m1.split(html)
        return re.split('</QUEST>', question[1])[0].strip()
    elif m2.search(html):
        question = m2.split(html)
        return re.split('</p>', question[1])[0].strip()
    elif m3.search(html):
        question = m3.split(html)
        return re.split('</div>', question[1])[0].strip()


def parse_assemblee_response(html):
    m1 = re.compile('<REP>')
    m2 = re.compile('<div class="(reponse_contenu|contenutexte)">')
    m3 = re.compile(r'<\S><\S>(DEBAT|Texte de la REPONSE) : </\S></\S>')
    if m1.search(html):
        reponse = m1.split(html)
        return re.split('</REP>', reponse[1])[0].strip()
    elif m2.search(html):
        reponse = m2.split(html)
        return re.split('</div>', reponse[2])[0].strip()
    elif m3.search(html):
        reponse = m3.split(html)
        content = re.split('</TEXTES>', reponse[2])[0].strip()
        return re.sub("\r\n", "\n", content)

    return ""


def parse_assemblee_infos(html):
    qp_data = QpData()
    qp_data.leg = parse_assemblee_legislature(html)
    qp_data = parse_assemblee_question_number(html, qp_data)
    qp_data = parse_assemblee_author(html, qp_data)
    qp_data.ministere = parse_assemblee_ministere(html)
    qp_data.title = parse_assemblee_title(html)
    qp_data.dpq, qp_data.pgq = parse_assemblee_publication(html)

    if qp_data.nature == "Question au Gouvernement":
        qp_data.ASREP = qp_data.nature
        qp_data.question = parse_assemblee_response(html)
        qp_data.dpr, qp_data.pgr = parse_assemblee_publication_response(html)
        qp_data.pgq = qp_data.pgr
    else:
        qp_data.question = parse_assemblee_question_text(html)
        qp_data.dpr, qp_data.pgr = parse_assemblee_publication_response(html)
        if qp_data.dpr:
            qp_data.ASREP = "Avec réponse"
            qp_data.reponse = parse_assemblee_response(html)

            if qp_data.nature == 'Question orale sans débat':
                m = re.compile(r'<p align="CENTER">\s*(.*)\s*<a.*</p>')
                if m.search(qp_data.reponse):
                    qp_data.title = m.search(qp_data.reponse).group(1)
                    qp_data.reponse = re.sub(r'<p align="CENTER">\s*.*\s*<a.*</p>',
                                             qp_data.title, qp_data.reponse)
        else:
            qp_data.ASREP = "Sans réponse"

    return qp_data


class AssembleeParser:
    def __init__(self, html):
        qp_data = parse_assemblee_infos(html)

        self.data = asdict(qp_data)
