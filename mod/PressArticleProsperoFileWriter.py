from mod.file_utils import name_file, create_txt_content, create_ctx_content, clean_content, write_file
from utils.supportpublimanager import SupportPubliManager


class PressArticleProsperoFileWriter(object):
    def __init__(self, article, destination, databaseName="unknown", cleaning_required=True):
        self.destination = destination

        prefix, source, source_type = fetch_publication_infos(article['source'])
        if not prefix:
            prefix = databaseName

        self.filename = name_file(article['date'], prefix, self.destination)

        txt_content = create_txt_content(article)
        ctx_content = create_ctx_content(article, source, source_type)

        self.cleaned_ctx_content, self.cleaned_txt_content = clean_content(cleaning_required,
                                                                           ctx_content,
                                                                           txt_content)

    def write(self):
        write_file(self.destination, self.filename, ".txt", self.cleaned_txt_content)
        write_file(self.destination, self.filename, ".ctx", self.cleaned_ctx_content)

    @property
    def get_filename(self):
        return self.filename


def fetch_publication_infos(publication):
    publication_index = SupportPubliManager()

    if publication not in publication_index.codex.keys():
        return None, publication, "unknown source"

    prefix = publication_index.codex[publication]['abr']
    source = publication_index.codex[publication]['source']
    source_type = publication_index.codex[publication]['type']

    return prefix, source, source_type
