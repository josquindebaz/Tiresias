from dataclasses import dataclass


@dataclass
class QpData:
    ASREP: str = ''
    aut: str = ''
    dept: str = ''
    dpq: str = ''
    dpr: str = ''
    groupe: str = ''
    leg: str = ''
    ministere: str = ''
    nature: str = ''
    num: str = ''
    pgq: str = ''
    pgr: str = ''
    question: str = ''
    reponse: str = ''
    support: str = "Journal officiel"
    title: str = ''

    def set_question_nature(self, nature):
        if nature in ['Question au gouvernement', 'Question au Gouvernement']:
            self.nature = 'Question au Gouvernement'
        else:
            self.nature = nature
