from html.parser import HTMLParser


class _ListingsParser(HTMLParser):
    """Collect listing records from fixture-style data-field HTML markers."""

    def __init__(self):
        """Prepare parser state for collecting listing records."""
        super().__init__()
        self._current_field = None
        self._field_depth = 0
        self._current_record = None
        self.records = []

    def handle_starttag(self, tag, attrs):
        """Start collecting a listing name or URL when a matching tag appears."""
        attrs_by_name = dict(attrs)
        field = attrs_by_name.get("data-field")

        if field == "name":
            self._finish_current_record()
            self._current_record = {"name_parts": [], "url": ""}
            self._current_field = "name"
            self._field_depth = 1
            return

        if self._current_field == "name":
            self._field_depth += 1

        if tag == "a" and field == "url":
            if self._current_record is None:
                self._current_record = {"name_parts": [], "url": ""}
            self._current_record["url"] = attrs_by_name.get("href", "").strip()

    def handle_data(self, data):
        """Collect text while inside a listing name field."""
        if self._current_field == "name" and self._current_record is not None:
            self._current_record["name_parts"].append(data)

    def handle_endtag(self, tag):
        """Stop collecting name text when the current name tag closes."""
        if self._current_field == "name":
            self._field_depth -= 1
            if self._field_depth <= 0:
                self._current_field = None

    def finish(self):
        """Flush the final record after HTML parsing completes."""
        self._finish_current_record()

    def _finish_current_record(self):
        """Store the current record if it has at least one collected field."""
        if self._current_record is None:
            return

        name = " ".join(
            part.strip() for part in self._current_record["name_parts"] if part.strip()
        )
        url = self._current_record["url"]

        if name or url:
            self.records.append({"name": name, "url": url})

        self._current_record = None


def parse_listings(html):
    """Parse all listing records and require each one to have name and URL."""
    parser = _ListingsParser()
    parser.feed(html)
    parser.close()
    parser.finish()

    if not parser.records:
        raise ValueError("listing must include name and url")

    for record in parser.records:
        if not record["name"] or not record["url"]:
            raise ValueError("listing must include name and url")

    return parser.records


def parse_listing(html):
    """Parse HTML and return the first listing record."""
    return parse_listings(html)[0]
