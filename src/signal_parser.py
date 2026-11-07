"""Generic character-signal parser with Hebrew and Greek parsing modes."""

from copy import deepcopy


class SignalParser:
    """Parse an exact character stream as Hebrew gematria or Book II Greek transforms."""

    HEBREW_GEMATRIA = {
        "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7,
        "ח": 8, "ט": 9, "י": 10, "כ": 20, "ך": 20, "ל": 30,
        "מ": 40, "ם": 40, "נ": 50, "ן": 50, "ס": 60, "ע": 70,
        "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
        "ש": 300, "ת": 400,
    }

    GREEK_OPERATORS = {
        "Α": "Origin", "Β": "Branch", "Γ": "Boundary frame / transform operator",
        "Δ": "Change", "Ε": "Threshold", "Ζ": "Link", "Η": "State",
        "Θ": "Constraint", "Ι": "Instance", "Κ": "Context", "Λ": "Lattice resolution",
        "Μ": "Measure", "Ν": "Novel state", "Ξ": "Contradiction",
        "Ο": "Observation", "Π": "Projection", "Ρ": "Relation", "Σ": "Aggregation",
        "Τ": "Whole-state traversal", "Υ": "Fork / choice", "Φ": "Form",
        "Χ": "Crossing / Kai carrier", "Ψ": "Pattern", "Ω": "Target / terminal field",
    }

    GREEK_SPECIAL = {
        "Ϛ": ("Unresolvedness", "Resolve observable unresolvedness", "unresolved"),
        "ϛ": ("Unresolvedness", "Resolve hidden unresolvedness", "unresolved"),
        "Ϙ": ("Actor participation", "Resolve observable actor participation", "actor"),
        "ϙ": ("Actor participation", "Resolve hidden actor participation", "actor"),
        "Ϟ": ("Indexed relationships", "Resolve observable numeral/indexed relationships", "indexed"),
        "ϟ": ("Indexed relationships", "Resolve hidden indexed relationships", "indexed"),
        "Ϝ": ("Retention", "Resolve observable retained constituents", "retention"),
        "ϝ": ("Retention", "Resolve hidden retained constituents", "retention"),
        "Ͷ": ("Context-specific retention", "Resolve observable context-specific retention", "retention"),
        "ͷ": ("Context-specific retention", "Resolve hidden context-specific retention", "retention"),
        "Ϻ": ("Differential", "Resolve observable differential", "differential"),
        "ϻ": ("Differential", "Resolve hidden differential", "differential"),
        "Ͳ": ("Archaic/indeterminate order", "Resolve observable archaic/indeterminate order", "order"),
        "ͳ": ("Archaic/indeterminate order", "Resolve hidden archaic/indeterminate order", "order"),
        "Ϡ": ("Extended numerical order", "Resolve observable extended numerical order", "order"),
        "ϡ": ("Extended numerical order", "Resolve hidden extended numerical order", "order"),
        "Ͱ": ("Contextual emergence", "Resolve observable contextual emergence", "context"),
        "ͱ": ("Contextual emergence", "Resolve hidden contextual emergence", "context"),
        "Ϳ": ("Mediation", "Resolve observable mediation", "mediation"),
        "ϳ": ("Mediation", "Resolve hidden mediation", "mediation"),
        "Ϸ": ("Representation change", "Resolve observable representation change", "representation"),
        "ϸ": ("Representation change", "Resolve hidden representation change", "representation"),
        "Ϲ": ("Active change", "Resolve observable active change", "change"),
        "ϲ": ("Active change", "Resolve hidden active change", "change"),
        "Ͻ": ("Reversal/reconsideration", "Resolve observable reversal/reconsideration", "reversal"),
        "ͻ": ("Reversal/reconsideration", "Resolve hidden reversal/reconsideration", "reversal"),
        "Ͼ": ("Accounted reversal/residue", "Resolve observable accounted reversal/residue", "residue"),
        "ͼ": ("Accounted reversal/residue", "Resolve hidden accounted reversal/residue", "residue"),
        "Ͽ": ("Witnessed change", "Resolve observable witnessed change", "witness"),
        "ͽ": ("Witnessed change", "Resolve hidden witnessed change", "witness"),
        "ς": ("Terminal closure", "Terminal closure of the relevant relational path", "closure"),
        "ϗ": ("Conjunction and composition", "Join relational states through conjunction and composition", "composition"),
        "Ϗ": ("Conjunction and composition", "Join relational states through conjunction and composition", "composition"),
        "𐆠": ("Relational authority", "Resolve authority and relational boundary", "authority"),
    }

    def __init__(self, rules=None):
        self.rules = {"hebrew": {}, "greek": {}, "unknown": "retain"}
        self.configure(rules or {})
        self.reset()

    def configure(self, rules):
        """Set optional Hebrew values or Greek operator overrides."""
        if not isinstance(rules, dict):
            raise TypeError("rules must be a dictionary")
        hebrew = rules.get("hebrew", {})
        greek = rules.get("greek", {})
        unknown = rules.get("unknown", self.rules["unknown"])
        if not isinstance(hebrew, dict) or not isinstance(greek, dict):
            raise TypeError("hebrew and greek rules must be dictionaries")
        if any(not isinstance(value, int) for value in hebrew.values()):
            raise TypeError("Hebrew gematria values must be integers")
        if unknown not in {"retain", "error"}:
            raise ValueError("unknown must be 'retain' or 'error'")
        self.rules = {"hebrew": deepcopy(hebrew), "greek": deepcopy(greek), "unknown": unknown}
        return self

    def reset(self):
        """Clear state while retaining parser rules."""
        self.source = ""
        self.mode = None
        self.state = {
            "occurrences": [], "signal": [], "mapped_indices": [],
            "structural_tokens": [], "signal_total": 0,
            "relations": [], "open_relation_ids": [], "unresolved": [],
            "actors": [], "witnesses": [], "retained": [], "closures": [],
        }
        self.result = None
        return self

    def parse(self, source, mode="hebrew"):
        """Parse a complete source using explicit `hebrew` or `greek` mode."""
        self.reset()
        self.mode = self._validate_mode(mode)
        self.parse_chunk(source)
        return self.finalize()

    def parse_hebrew(self, source):
        """Parse source into ordinary Hebrew gematria values."""
        return self.parse(source, mode="hebrew")

    def parse_greek(self, source):
        """Parse source as Book II Greek transform occurrences."""
        return self.parse(source, mode="greek")

    def derive_checksum_triples(self, source=None, modulus=231, multiplier=22):
        """Emit aligned SUM, LINEAR, and PRODUCT triples for adjacent Hebrew values.

        When `source` is supplied it is first parsed as Hebrew. Without `source`,
        the current parser state must already be a Hebrew parse.
        """
        if source is not None:
            self.parse_hebrew(source)
        if self.mode != "hebrew":
            raise RuntimeError("derive checksum triples from a Hebrew parse")
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError("modulus must be a positive integer")
        if not isinstance(multiplier, int):
            raise TypeError("multiplier must be an integer")

        values = self.state["signal"]
        indices = self.state["mapped_indices"]
        triples = []
        for pair_index, (first, second) in enumerate(zip(values, values[1:])):
            triples.append({
                "pair_index": pair_index,
                "source_indices": (indices[pair_index], indices[pair_index + 1]),
                "values": (first, second),
                "sum": (first + second) % modulus,
                "linear": (first * multiplier + second) % modulus,
                "product": (first * second) % modulus,
            })
        return triples

    def reconstruct_from_triples(self, triples, alphabet=None, modulus=231, multiplier=22, max_paths=1024):
        """Recover gematria paths from overlapping checksum triples.

        Pair candidates are derived from `alphabet`, then chained by their shared
        middle value. The result retains every surviving path instead of selecting
        an arbitrary candidate when the supplied triples remain ambiguous.
        """
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError("modulus must be a positive integer")
        if not isinstance(multiplier, int):
            raise TypeError("multiplier must be an integer")
        if not isinstance(max_paths, int) or max_paths < 1:
            raise ValueError("max_paths must be a positive integer")
        alphabet = self.HEBREW_GEMATRIA if alphabet is None else alphabet
        if not isinstance(alphabet, dict) or not alphabet:
            raise ValueError("alphabet must be a non-empty glyph-to-integer dictionary")
        if any(not isinstance(value, int) for value in alphabet.values()):
            raise TypeError("alphabet values must be integers")

        normalized = [self._normalize_triple(triple) for triple in triples]
        if not normalized:
            return {"value_paths": [[]], "canonical_text_paths": [""], "ambiguous": False}

        values = sorted(set(alphabet.values()))
        candidates_by_signature = {}
        for first in values:
            for second in values:
                signature = (
                    (first + second) % modulus,
                    (first * multiplier + second) % modulus,
                    (first * second) % modulus,
                )
                candidates_by_signature.setdefault(signature, []).append((first, second))

        candidate_rows = [candidates_by_signature.get(signature, []) for signature in normalized]
        if not candidate_rows[0]:
            return self._reconstruction_result([], alphabet, candidate_rows)

        paths = [[first, second] for first, second in candidate_rows[0]]
        if len(paths) > max_paths:
            raise RuntimeError("candidate path limit reached; provide more context or raise max_paths")
        for candidates in candidate_rows[1:]:
            paths = [path + [second] for path in paths for first, second in candidates if first == path[-1]]
            if len(paths) > max_paths:
                raise RuntimeError("candidate path limit reached; provide more context or raise max_paths")
            if not paths:
                break
        return self._reconstruction_result(paths, alphabet, candidate_rows)

    def parse_chunk(self, chunk):
        """Parse an exact continuation chunk in the selected mode."""
        if self.mode is None:
            raise RuntimeError("select a mode with parse(), parse_hebrew(), or parse_greek() first")
        if not isinstance(chunk, str):
            raise TypeError("signal chunks must be strings")
        start = len(self.source)
        self.source += chunk
        for offset, character in enumerate(chunk):
            self.apply_rule(character, start + offset)
        return self

    def apply_rule(self, token, index=None):
        """Apply the active Hebrew or Greek rule to one exact character."""
        if not isinstance(token, str) or len(token) != 1:
            raise ValueError("a parser token must be exactly one Unicode character")
        index = len(self.state["occurrences"]) if index is None else index
        occurrence = self._apply_hebrew(token, index) if self.mode == "hebrew" else self._apply_greek(token, index)
        self.state["occurrences"].append(occurrence)
        self.result = None
        return occurrence

    def finalize(self):
        """Return a snapshot without discarding any open or structural state."""
        self.result = {
            "mode": self.mode, "source": self.source,
            "occurrences": deepcopy(self.state["occurrences"]),
            "signal": list(self.state["signal"]),
            "signal_total": self.state["signal_total"],
            "mapped_indices": list(self.state["mapped_indices"]),
            "structural_tokens": deepcopy(self.state["structural_tokens"]),
            "relations": deepcopy(self.state["relations"]),
            "open_relation_ids": list(self.state["open_relation_ids"]),
            "unresolved_ids": list(self.state["unresolved"]),
            "closure_count": len(self.state["closures"]),
        }
        return deepcopy(self.result)

    def _apply_hebrew(self, character, index):
        value = self.rules["hebrew"].get(character, self.HEBREW_GEMATRIA.get(character))
        if value is not None:
            signal_index = len(self.state["signal"])
            self.state["signal"].append(value)
            self.state["mapped_indices"].append(index)
            self.state["signal_total"] += value
            return {"index": index, "character": character, "kind": "Hebrew gematria letter", "gematria_value": value, "signal_index": signal_index}
        return self._structural(character, index)

    def _apply_greek(self, character, index):
        operator = self._greek_operator(character)
        if operator is None:
            return self._structural(character, index)
        relation_id = len(self.state["relations"])
        category = operator["category"]
        self.state["relations"].append({"id": relation_id, "source_index": index, "operator": character, "role": operator["role"], "status": "open"})
        self.state["open_relation_ids"].append(relation_id)
        if category == "unresolved":
            self.state["unresolved"].append(relation_id)
        elif category == "actor":
            self.state["actors"].append(relation_id)
        elif category == "retention":
            self.state["retained"].append(relation_id)
        elif category == "witness":
            self.state["witnesses"].append(relation_id)
        elif category == "closure":
            self.state["closures"].append({"marker_relation_id": relation_id, "scope": "unspecified"})
        return {"index": index, "character": character, "operator": character, "role": operator["role"], "action": operator["action"], "relation_id": relation_id, "retained_remainder": list(self.state["open_relation_ids"])}

    def _greek_operator(self, character):
        if character in self.rules["greek"]:
            return deepcopy(self.rules["greek"][character])
        if character in self.GREEK_SPECIAL:
            role, action, category = self.GREEK_SPECIAL[character]
            return {"role": role, "action": action, "category": category}
        uppercase = character.upper()
        glyphs = set(self.GREEK_OPERATORS) | {glyph.lower() for glyph in self.GREEK_OPERATORS}
        if character in glyphs:
            resolution = "observable" if character == uppercase else "hidden"
            role = self.GREEK_OPERATORS[uppercase]
            return {"role": role, "action": f"Resolve {resolution} {role.lower()}", "category": "standard"}
        return None

    def _structural(self, character, index):
        if self.rules["unknown"] == "error":
            raise ValueError(f"no {self.mode} rule for {character!r} at index {index}")
        occurrence = {"index": index, "character": character, "kind": "structural or unmapped token", "value": None}
        self.state["structural_tokens"].append(occurrence)
        return occurrence

    @staticmethod
    def _validate_mode(mode):
        if mode not in {"hebrew", "greek"}:
            raise ValueError("mode must be 'hebrew' or 'greek'")
        return mode

    @staticmethod
    def _normalize_triple(triple):
        if isinstance(triple, dict):
            try:
                return (triple["sum"], triple["linear"], triple["product"])
            except KeyError as error:
                raise ValueError("triple dictionaries need sum, linear, and product") from error
        if isinstance(triple, (tuple, list)) and len(triple) == 3:
            return tuple(triple)
        raise TypeError("each triple must be a mapping or a three-item sequence")

    @staticmethod
    def _reconstruction_result(paths, alphabet, candidate_rows):
        glyphs_by_value = {}
        for glyph, value in alphabet.items():
            glyphs_by_value.setdefault(value, []).append(glyph)
        canonical = ["".join(glyphs_by_value[value][0] for value in path) for path in paths]
        return {
            "value_paths": paths,
            "canonical_text_paths": canonical,
            "letter_candidates": [[glyphs_by_value[value] for value in path] for path in paths],
            "candidate_pair_counts": [len(row) for row in candidate_rows],
            "ambiguous": len(paths) != 1,
        }
