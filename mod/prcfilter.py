"""Author Josquin Debaz
GPL 3
"""
import os
import re


def count_item(item, text):
    before_and_after = r"[\s\.,;!\?\"']"  # punctuation Before or after
    index = r"(^|(%s))(%s)((%s)|$)" % (before_and_after,
                                       item,
                                       before_and_after)
    index = re.compile(index)

    return len(index.findall(text))


def parse_text(theme, text):
    if len(theme) < 2:
        return False

    tests = {}
    for item in theme:
        number = count_item(item, text)
        tests[item] = number

    return tests


def evaluate_tests(tests):
    return {
        "sum": sum(tests.values()),
        "components": sum(1 for x in tests.values() if x > 0)
    }


class PrcFilter:
    """Filter files with score and depth"""

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
        test_theme = parse_text(self.theme, text)
        if not test_theme:
            return False, False

        tests_results = [
            "[%s:%d]" % (item, result) for item,
            result in test_theme.items() if result
        ]
        evaluate = evaluate_tests(test_theme)

        return "".join(tests_results), list(evaluate.values())

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

    theme = ["saída", "presidente", "definitiva", "Palácio", "arsoiten"]

    print(">> count_item")

    result = count_item(theme[0], content)
    print("Can count item", result == 3)

    result = count_item(theme[1], content)
    print("Does not count sub words", result == 1)

    result = count_item(theme[2], content)
    print("Does count words with punctuation", result == 1)

    result = count_item(theme[3], content)
    print("Is case sensitive", result == 1)

    print(">> parse_text")

    result = parse_text([theme[0]], content)
    print("Does not parse theme with less than 2 items", result is False)

    result = parse_text(theme, content)
    print("Does parse every item in a theme", len(result) == len(theme))

    print(">> evaluate_tests")

    evaluate_result = evaluate_tests(result)
    print("Sum the value of all the item test", evaluate_result["sum"] == 6)
    print("Count the number of valid tests", evaluate_result["components"] == 4)

    print(">> PrcFilter().eval_theme")

    test = PrcFilter()
    test.score = 1
    test.dep = 1

    test.theme = [theme[0]]
    result = test.eval_theme(content)
    print("Does not go for theme with less than 2 items", result == (False, False))

    test.theme = theme
    result = test.eval_theme(content)
    print("Returns a string with theme tests", result[0] == "[saída:3][presidente:1][definitiva:1][Palácio:1]")
    print("Returns an array with tests sum and depth", result[1] == [6, 4])
