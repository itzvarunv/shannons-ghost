"""Small Wikipedia API helpers for the fencer (plain HTTPS, no extra packages)."""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "Relations/0.1 (personal research project; github.com/itzvarunv)"
MATH = re.compile(r"<math[^>]*>(.*?)</math>", re.S)


_last = [0.0]
MIN_GAP = 1.0            # seconds between requests, to stay polite


def api(params):
    params = dict(params, format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(5):
        wait = _last[0] + MIN_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 10 * (attempt + 1))
        except urllib.error.URLError:
            if attempt == 4:
                raise
            time.sleep(5)


def category_pages(category, limit=200):
    """Article titles directly in a category (no subcategories)."""
    titles, cont = [], {}
    while len(titles) < limit:
        r = api({"action": "query", "list": "categorymembers", "cmtitle": f"Category:{category}",
                 "cmtype": "page", "cmnamespace": "0", "cmlimit": "max", **cont})
        titles += [m["title"] for m in r.get("query", {}).get("categorymembers", [])]
        if "continue" not in r:
            break
        cont = r["continue"]
    return titles[:limit]


def wikitext(titles):
    """{title: wikitext} for up to 50 titles in one request (redirects followed)."""
    r = api({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
             "redirects": "1", "titles": "|".join(titles)})
    out = {}
    for page in r.get("query", {}).get("pages", []):
        revs = page.get("revisions") or []
        if revs:
            out[page["title"]] = revs[0]["slots"]["main"].get("content", "")
    for redirect in r.get("query", {}).get("redirects", []):
        if redirect["to"] in out:
            out[redirect["from"]] = out[redirect["to"]]
    return out


def clean(text):
    """Strip references, templates, files and link markup; keep <math> blocks."""
    text = re.sub(r"<ref[^>]*/>", "", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    prev = None
    while prev != text:                       # nested templates, innermost first
        prev = text
        text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[(?:File|Image):[^\]]*(?:\[\[[^\]]*\]\][^\]]*)*\]\]", "", text)
    text = re.sub(r"\[\[([^\]|]*)\|([^\]]*)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"'{2,}", "", text)
    text = re.sub(r"\{\|.*?\|\}", "", text, flags=re.S)     # tables
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def excerpt(raw, max_lead=700, max_equations=6, context=140):
    """Lead paragraph + up to 6 equations with the sentence before each.
    Returns (excerpt_text, number_of_equations_on_the_page)."""
    text = clean(raw)
    lead = text.split("\n==", 1)[0].strip()
    equations = [m for m in MATH.finditer(text) if "=" in m.group(1) and len(m.group(1).strip()) > 3]
    parts = [lead[:max_lead]]
    for m in equations[:max_equations]:
        before = text[max(0, m.start() - context):m.start()].replace("\n", " ")
        parts.append(f"... {before.strip()} [EQUATION] {m.group(1).strip()}")
    return "\n".join(parts), len(equations)
