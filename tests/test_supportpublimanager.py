import os.path

from utils.supportpublimanager import SupportPubliManager, parse_publi


def test_support_publi_manager_init():
    manager = SupportPubliManager()

    path = "../data/support.publi"
    path = path if os.path.isfile(path) else "data/support.publi"

    with open(path, 'rb') as handle:
        buf = handle.readlines()

    assert len(manager.codex) == len(buf)

    expected = {'source': '01Informatique', 'type': 'News et magazines', 'abr': '01INF'}
    assert manager.codex['01Informatique'] == expected

    expected = {'source': 'Libération', 'type': 'Presse nationale', 'abr': 'LIB'}
    assert manager.codex['Écrans (site web)'] == expected

    assert len(manager.sources) == 872

    expected = {'type': 'News et magazines', 'abr': '01INF'}
    assert manager.sources['01Informatique'] == expected

    expected = {'type': 'Presse nationale', 'abr': 'LIB'}
    assert manager.sources['Libération'] == expected


def test_parse_publi():
    content = """nouvelobs.com - Quotidien Permanent; Le Nouvel Observateur; News et magazines; OBS
nouvelobs.com; Le Nouvel Observateur; News et magazines; OBS
"""
    codex, sources = parse_publi(content)

    expected_codex = {'nouvelobs.com - Quotidien Permanent':
                          {'source': 'Le Nouvel Observateur', 'type': 'News et magazines', 'abr': 'OBS'},
                      'nouvelobs.com':
                          {'source': 'Le Nouvel Observateur', 'type': 'News et magazines', 'abr': 'OBS'}
                      }
    assert len(codex) == 2
    assert codex == expected_codex

    expected_sources = {'Le Nouvel Observateur': {'type': 'News et magazines', 'abr': 'OBS'}}
    assert len(sources) == 1
    assert sources == expected_sources


def test_add():
    manager = SupportPubliManager()

    entry = "A Publication on the web"
    source = "A Publication"
    source_type = "Magazine"
    abbr = "PREFIX"

    manager.add(entry, source, source_type, abbr)

    assert entry in manager.codex.keys()
    assert manager.codex[entry] == {'abr': 'PREFIX', 'source': 'A Publication', 'type': 'Magazine'}

    assert source in manager.sources.keys()
    assert manager.sources[source] == {'abr': 'PREFIX', 'type': 'Magazine'}

    new_entry = "Same Publication anywhere else"
    manager.add(new_entry, source, source_type, abbr)
    assert new_entry not in manager.sources.keys()

