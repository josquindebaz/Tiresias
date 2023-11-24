"""Author Josquin Debaz
GPL 3
"""
import os
import re


def count_item(item, text):
    # punctuation Before or after
    beforeafter = r"[\s\.,;!\?\"']"
    index = r"(^|(%s))(%s)((%s)|$)" % (beforeafter, item,
                                       beforeafter)
    index = re.compile(index)

    return len(index.findall(text))


class PrcFilter:
    """Only files with score and dep"""

    def __init__(self):
        self.list_txt = []
        self.theme = []
        self.score = 0
        self.dep = 0
        self.corpus = {}
        self.anticorpus = {}
        self.prc_param = []

    def openprc(self, path):
        """read a .prc"""
        with open(path, 'r') as handle:
            buf = handle.readlines()
        self.list_txt = [txt[:-1] for txt in buf[6:-1]]
        self.prc_param = buf[1:6]

    def eval_corpus(self):
        """eval a corpus for score and dep"""
        for txt in self.list_txt:
            if os.path.isfile(txt):
                with open(txt, "r") as handle:
                    content = handle.read()
                evaluation = self.eval_theme(content)
                if (evaluation[1][0] >= self.score) and (evaluation[1][1] >= self.dep):
                    self.corpus[txt] = evaluation
                else:
                    self.anticorpus[txt] = evaluation
            else:
                self.anticorpus[txt] = False

    def eval_theme(self, text):
        """give score and dep of a theme"""
        if len(self.theme) > 1:
            tests = []
            testsresults = ""

            for item in self.theme:
                number = count_item(item, text)
                if number > 0:
                    testsresults += "[%s:%d]" % (item, number)
                    tests.append(number)

            evaluation = [sum(tests), sum(1 for x in tests if x > 0)]
            return testsresults, evaluation
        return False, False

    def save_prc(self, path, txts):
        """save txt list to path prc"""
        lines = ["projet0005\n"]
        lines.extend(self.prc_param)
        lines.extend([txt + "\n" for txt in txts])
        lines.append("ENDFILE")
        with open(path, "w") as handle:
            handle.writelines(lines)


if __name__ == '__main__':
    content = """No Palácio do Planalto, a saída de Sérgio Machado da Transpetro é tratada como definitiva. A 
    "licença" foi acertada com Renan Calheiros e José Sarney, padrinhos do ex-presidente da empresa, subsidiária da 
    Petrobras. Quando a PricewaterhouseCoopers exigiu sua saída para prosseguir a auditoria na empresa, 
    Machado procurou apoio na cúpula do PMDB e disse à presidente da Petrobras, Graça Foster, que não aceitava ser 
    demitido. A partir daí, foi costurada a saída honrosa para ele. presidentes palácio"""

    result = count_item("saída", content)
    print("Can count item", result == 3)

    result = count_item("presidente", content)
    print("Does not count subwords", result == 1)

    result = count_item("definitiva", content)
    print("Does count words with punctuation", result == 1)

    result = count_item("Palácio", content)
    print("Is case sensitive", result == 1)



