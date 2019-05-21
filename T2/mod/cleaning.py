# Author Josquin Debaz
# GPL 3
import os
import re
import html


def list_files(rep='.', exts=['.txt', '.TXT'],
               recursive=True, slash=True, repl=[]):
    L = []
    for roots, dirs, files in os.walk('%s'%rep):
        L.extend([os.path.join(roots, f) for f in files \
            if (os.path.splitext(f)[1] in exts)] )
        if recursive == False:
            break
        
    if (repl):
        L = list(map(lambda x: x.replace(repl[0], repl[1]), L))
    if (slash):
        L = list(map(lambda x: x.replace("/", "\\"), L))
        
    return L

class Cleaner(object):
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
        try:
            self.content.decode('utf-8')
        except UnicodeDecodeError:     
            return False
        else:
            return True

    def utf_to_latin(self):
        txt_unicode = self.content.decode('utf-8')
        self.content = txt_unicode.encode('latin-1', 'xmlcharrefreplace')

    def replace_ascii(self):
        """{unknown ascii code: correct form,}"""
        D = { 12: "\n",
              133: "..." ,
              145: "'" ,
              146: "'" ,
              147: '"' ,
              148: '"' ,
              149: "-" ,
              150: "-" ,
              151: "-" ,
              160: " ",
              171:'" ' ,
              173: "-" ,
              180: "'" ,
              183: "-",
              186: '"' ,
              187: ' "' ,
              96: "'" ,
              156: "oe" ,
              }
        total = 0
        for code, cor in D.items():
            n = self.content.count(chr(code))
            if n:
                total += n
                self.content = self.content.replace(chr(code), cor)    
        return total  

    def char_replace(self):
        """{ "correct": ["incorrect 1,", "incorrect 2",],}"""
        D = {
            "": ["&#65279;",],
            "'": ["&rsquo;",
                  '&#8217;',
                  '&#8216;',
                  "&lsquo;"],
            ' " ': ["&laquo;",
                    "&raquo;",
                    "&#8220;",
                    "&#8221;",
                   "&#171;" ,
                    "&#187;" ,
                    "&quot;",
                    "&lt;",
                    "&gt;",
                   "«",
                    '»'],
            '... ': ["&hellip;",
                     "&#8230;",
                     "&#x2026;"
                     ]  ,
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
            "\r\n- " : ["<li>",
                        "<ol>"],
            ' - ' : ['&#8212;',
                     "&ndash;"],
            " ": ["&nbsp;",
                  '&#xd;',
                  '#xd;',
                  "&#160;",
                  "&#176;",
                  "&#8201;",
                  "&#8203;",
                  "&#8239;",
                  "\xc2"],
            "oe": ["&oelig;",
                   "&#156;",
                   "&#339;",
                   "&#338;" ],
            "euros": ["&#8364;",
                      "&euro;" ,
                      "&#8364"], 
            "e": ["&#7497;"],
            }
        

        n = 0 
        for correcte, incorrectes in D.items() :
            for i in incorrectes:
                cherche = self.content.count(i)
                if cherche:
                    self.content = self.content.replace(i, correcte)
                    n += cherche
        self.content =  html.unescape(self.content)
        
        return n

    def splitted_numbers(self):
        """strip splitted numbers"""
        n = len(re.findall("\d[ \.]\d{3}", self.content))
        if n:
            self.content = re.sub("(\d)[ \.](\d{3})", "\\1\\2", self.content)
        return n

    def dash_with_punctuation(self):
        """spacing dashes"""
        after = re.compile("-([\.,;!\?:'\(\)\[\]])")
        nafter = len(after.findall(self.content))
        if nafter:
            self.content = after.sub(" - \\1", self.content)
            
        before = re.compile("([,;!\?:'\(\)\[\]])-")
        # .- is not processed because of firstname abrev like J.-P.
        nbefore = len(before.findall(self.content))
        if nbefore:
            self.content = before.sub("\\1 - ", self.content)
       
        return nbefore + nafter

    def hyphens(self):
        """Strip hyphenations"""
        m = re.compile("-\s*[\r\n]{1,}")
        n = len(m.findall(self.content))
        if n:
            self.content = m.sub("", self.content)
        return n

    def html_tags(self):
        """Delete html tags"""
        tags = [ '<i>','</i>', '<em>', '</em>',
              '<strong>','</strong>',
              '</tr>', '<td>', '</td>',
              '&lt;i&gt;','&lt;/i&gt;',
              '&lt;/strong&gt;', '&lt;strong&gt;',
              "<div>", "</div>", "<ul>", "</ul>",
              "<p>",  "<span>", "</span>",
              "<b>", "</b>",
              "<p align='center'>", '<p align="CENTER">',
                 '<center>', '</center>',
                 
              ]
        n = 0
        for tag in tags:
            t = self.content.count(tag)
            if t:
                self.content = self.content.replace(tag, "")
                n += t
        return n

    def parity_marks(self):
        """Separate parity marks -e-s or (e)"""
        #not i.e.
        m = re.compile("([a-zé](?<!i))(\.e|-e|\(e\)|-ne|-rice|-euse)(\s|\.|-)")
        n = len(m.findall(self.content))
        if n:
            self.content = m.sub("\\1 \\2\\3", self.content) 
        return n
    
    def footnotes(self):
        m = re.compile('([A-Za-zé]{2,})(\d{1,})(\.|\(|,) ')
        n = len(m.findall(self.content))
        if n:
            self.content = m.sub("\\1 \\2 \\3 ", self.content)
        return n
        
    
if __name__ == '__main__':
    list_TXT = list_files(os.getcwd())
    for txt in list_TXT:
        print( txt)
        with open(txt, 'rb') as f:
            buf = f.read()
        C = Cleaner(buf, "uasdhtpcf")
        print (C.log)
        buf = bytes(C.content, 'latin-1')       
        with open(txt, 'wb') as f:
            f.write(buf)
        


