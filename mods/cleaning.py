""" Clean text files for Prospero
Author Josquin Debaz
GPL 3
"""
import os
import re
import html

def list_files(rep='.', exts=('.txt', '.TXT'),
               recursive=True, slash=False, repl=None):
    """List files with txt or TXT extension"""
    txt_files = []
    for roots, _, files in os.walk('%s'%rep):
        txt_files.extend([os.path.join(roots, f) for f in files \
            if os.path.splitext(f)[1] in exts])
        if not recursive:
            break
    if repl:
        txt_files = list(map(lambda x: x.replace(repl[0], repl[1]), txt_files))
    if slash:
        txt_files = list(map(lambda x: x.replace("/", "\\"), txt_files))
    return txt_files

class Cleaner():
    """Convert bytes and clean string"""
    def __init__(self, content, options="uasdhtpcf"):
        self.content = content
        self.log = {}

        if "u" in options:
            if self.is_utf8():
                self.utf_to_latin()
                self.log['utf'] = 1
            else:
                self.log['utf'] = 0

        self.content = self.content.decode('latin-1') #byte to str

        if "a" in options:
            self.log['ascii'] = self.replace_ascii()
        if "c" in options:
            self.log['chars'] = self.char_replace()
        if "s" in options:
            self.log['splitted numbers'] = self.splitted_numbers()
        if "h" in options:
            self.log['hyphens'] = self.hyphens()
        if "t" in options:
            self.log['html tags'] = self.html_tags()
        if "p" in options:
            self.log['parity marks'] = self.parity_marks()
        if "d" in options:
            self.log['Dashes'] = self.dash_with_punctuation()
        if "f" in options:
            self.log['footnotes'] = self.footnotes()

    def is_utf8(self):
        """Return True if utf-8"""
        try:
            self.content.decode('utf-8')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def utf_to_latin(self):
        """Convert utf to latin"""
        txt_unicode = self.content.decode('utf-8')
        self.content = txt_unicode.encode('latin-1', 'xmlcharrefreplace')

    def replace_ascii(self):
        """{unknown ascii code: correct form,}"""
        asciis = {
            12: "\n",
            133: "...",
            145: "'",
            146: "'",
            147: '"',
            148: '"',
            149: "-",
            150: "-",
            151: "-",
            160: " ",
            171:'" ',
            173: "-",
            180: "'",
            183: "-",
            186: '"',
            187: ' "',
            96: "'",
            156: "oe",
        }
        total = 0
        for code, cor in asciis.items():
            number = self.content.count(chr(code))
            if number:
                total += number
                self.content = self.content.replace(chr(code), cor)
        return total

    def char_replace(self):
        """{ "correct": ["incorrect 1,", "incorrect 2",],}"""
        to_be_replaced = {
            "": ["&#65279;",
                 "&#8206;"],
            "'": ["&rsquo;",
                  '&#8217;',
                  '&#8216;',
                  "&lsquo;"],
            ' " ': ["&laquo;",
                    "&raquo;",
                    "&#8220;",
                    "&#8221;",
                    "&#171;",
                    "&#187;",
                    "&quot;",
                    "&lt;",
                    "&gt;",
                    "«",
                    '»',
                    ],
            '... ': ["&hellip;",
                     "&#8230;",
                     "&#x2026;"
                     ],
            "-": ["&#8211;",
                  "&#8208;",
                  "&sect;",
                  "&bull;",
                  "&#8209;"],
            "\r\n": ["<br>",
                     "<br/>",
                     "<BR>",
                     "<BR/>",
                     '</br>',
                     '<th>',
                     "<BR />",
                     "<br />",
                     '<tr>',
                     "</p>",
                     "</th>",
                     "</ol>",
                     "</li>",
                     "&#8232;",
                     '<p />'],
            "\r\n- ": ["<li>",
                       "<ol>"],
            ' - ': ['&#8212;',
                    "&ndash;",
                    "&#61623;",
                    "&#61662;",
                    "&#8722;"],
            " ": ["&nbsp;",
                  '&#xd;',
                  '#xd;',
                  "&#160;",
                  "&#176;",
                  "&#8201;",
                  "&#8203;",
                  "&#8239;",
                  "\xc2",
                  "&#128073;",
                  "&#8294;",
                  "&#8297;",
                  "&#8202;",
                  "&#8200;"],
            "oe": ["&oelig;",
                   "&#156;",
                   "&#339;",
                   "&#338;"],
            "euros": ["&#8364;",
                      "&euro;",
                      "&#8364"],
            "e": ["&#7497;"],
            "à": ["a&#768;"],
            "À": ["A&#768;"],
            "é": ["e&#769;"],
            "ê": ["e&#770;"],
            "è": ["e&#768;"],
            "â": ["a&#770;"],
            "ô": ["o&#770;"],
            "î": ["i&#770;"],
            "ï": ["i&#776;"],
            "ç": ["c&#807;"],
            "û": ["u&#770;"],
            "y": ["&#947;"],
            "c": ["&#269;"],
            "r": ["&#345;"],
            ":)": ["&#128521;"],
            ":(": ["&#128542;"],
            "µ": ["&#956"],
            "d": ["&#948;"],
            "e": ["&#279;"],
            "@": ["&#8294;"]
            }

        number = 0
        for correcte, incorrectes in to_be_replaced.items():
            for i in incorrectes:
                cherche = self.content.count(i)
                if cherche:
                    self.content = self.content.replace(i, correcte)
                    number += cherche
        self.content = html.unescape(self.content)
        #remove unescape characters not compatible with latin1
        self.content = re.sub("\u2033", '"', self.content)
        self.content = re.sub('\u2219', '.', self.content)
        return number

    def splitted_numbers(self):
        """strip splitted numbers"""
        number = len(re.findall(r"\d[ \.]\d{3}", self.content))
        if number:
            self.content = re.sub(r"(\d)[ \.](\d{3})", "\\1\\2", self.content)
        return number

    def dash_with_punctuation(self):
        """spacing dashes"""
        after = re.compile(r"-([\.,;!\?:'\(\)\[\]])")
        nafter = len(after.findall(self.content))
        if nafter:
            self.content = after.sub(" - \\1", self.content)

        before = re.compile(r"([,;!\?:'\(\)\[\]])-")
        # .- is not processed because of firstname abrev like J.-P.
        nbefore = len(before.findall(self.content))
        if nbefore:
            self.content = before.sub("\\1 - ", self.content)

        return nbefore + nafter

    def hyphens(self):
        """Strip hyphenations"""
        motif = re.compile(r"-\s*[\r\n]{1,}")
        number = len(motif.findall(self.content))
        if number:
            self.content = motif.sub("", self.content)
        return number

    def html_tags(self):
        """Delete html tags"""
        tags = ['<i>', '</i>', '<em>', '</em>',
                '<strong>', '</strong>',
                '</tr>', '<td>', '</td>',
                '&lt;i&gt;', '&lt;/i&gt;',
                '&lt;/strong&gt;', '&lt;strong&gt;',
                "<div>", "</div>", "<ul>", "</ul>",
                "<p>", "<span>", "</span>",
                "<b>", "</b>",
                "<p align='center'>", '<p align="CENTER">',
                '<center>', '</center>',
                ]
        number = 0
        #delete tags from the list
        for tag in tags:
            tag_number = self.content.count(tag)
            if tag_number:
                self.content = self.content.replace(tag, "")
                number += tag_number
        #delete unknown even tags: <balise>bla bla</balise>
        unlisted = re.findall("<([a-z]*)>", self.content)
        if unlisted:
            for balise in unlisted:
                opening = re.findall("<%s>"%balise, self.content)
                closing = re.findall("</%s>"%balise, self.content)
                if len(opening) == len(closing):
                    self.content = re.sub("<%s>"%balise, "", self.content)
                    self.content = re.sub("</%s>"%balise, "", self.content)
                    number += len(opening)
        #delete single tags: <tag something>
        singles = re.findall(r"<[a-z]{1,} \S*>", self.content)
        if singles:
            number += len(singles)
            self.content = re.sub(r"<[a-z]{1,} \S*>", "", self.content)
        #delete links: <a something>keep me</a>
        links = re.findall("<a .*>(.*)</a>", self.content)
        if links:
            number += len(links)
            self.content = re.sub("<a .*>(.*)</a>", "\\1", self.content)

        return number

    def parity_marks(self):
        """Separate parity marks -e-s or (e)"""
        #not i.e.
        motif = re.compile(r"([a-zé](?<!i))(\.e|-e|\(e\)|-ne|-rice|-euse)(\s|\.|-)")
        number = len(motif.findall(self.content))
        if number:
            self.content = motif.sub("\\1 \\2\\3", self.content)
        return number

    def footnotes(self):
        """Separate footnote calls"""
        motif = re.compile(r'([A-Za-zé]{2,})(\d{1,})(\.|\(|,) ')
        number = len(motif.findall(self.content))
        if number:
            self.content = motif.sub("\\1 \\2 \\3 ", self.content)
        return number


if __name__ == '__main__':
    for txt in list_files(os.getcwd()):
        print(txt)
        with open(txt, 'rb') as f:
            buf = f.read()
        C = Cleaner(buf, "uasdhtpcf")
        print(C.log)
        buf = bytes(C.content, 'latin-1')
        with open(txt, 'wb') as f:
            f.write(buf)
