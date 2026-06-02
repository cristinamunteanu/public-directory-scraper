from html.parser import HTMLParser


class _ListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._current_field = None
        self._name_parts = []
        self.url = ""

    def handle_starttag(self, tag, attrs):
        attrs_by_name = dict(attrs)
        field = attrs_by_name.get("data-field")

        if field == "name":
            self._current_field = "name"

        if tag == "a" and field == "url":
            self.url = attrs_by_name.get("href", "").strip()

    def handle_data(self, data):
        if self._current_field == "name":
            self._name_parts.append(data)

    def handle_endtag(self, tag):
        if self._current_field == "name":
            self._current_field = None

    @property
    def name(self):
        return " ".join(part.strip() for part in self._name_parts if part.strip())


def parse_listing(html):
    parser = _ListingParser()
    parser.feed(html)
    parser.close()

    record = {
        "name": parser.name,
        "url": parser.url,
    }

    if not record["name"] or not record["url"]:
        raise ValueError("listing must include name and url")

    return record
