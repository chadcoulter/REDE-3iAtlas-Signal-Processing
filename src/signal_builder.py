"""Build an aligned base signal and SUM, LINEAR and PRODUCT child waves."""
from dataclasses import dataclass
import csv
from pathlib import Path

try:
    from .signal_parser import SignalParser
except ImportError:
    from signal_parser import SignalParser


def _integers(values):
    values = tuple(values)
    if any(type(value) is not int for value in values):
        raise TypeError('base signal values must be integers')
    return values


def _modulus(value):
    if type(value) is not int or value <= 0:
        raise ValueError('modulus must be a positive integer')
    return value


def BuildSumWave(values, modulus=231):
    """Return (first + second) % modulus for adjacent base samples."""
    values, modulus = _integers(values), _modulus(modulus)
    return tuple((a + b) % modulus for a, b in zip(values, values[1:]))


def BuildLinearWave(values, modulus=231, multiplier=22):
    """Return (first * multiplier + second) % modulus in source order."""
    values, modulus = _integers(values), _modulus(modulus)
    if type(multiplier) is not int:
        raise TypeError('multiplier must be an integer')
    return tuple((a * multiplier + b) % modulus for a, b in zip(values, values[1:]))


def BuildProductWave(values, modulus=231):
    """Return (first * second) % modulus for adjacent base samples."""
    values, modulus = _integers(values), _modulus(modulus)
    return tuple((a * b) % modulus for a, b in zip(values, values[1:]))


@dataclass(frozen=True)
class BuiltSignal:
    base: tuple
    source_indices: tuple
    sum_wave: tuple
    linear_wave: tuple
    product_wave: tuple
    modulus: int
    multiplier: int

    def rows(self):
        """One row per base point; child waves are anchored to the first of a pair."""
        for i, value in enumerate(self.base):
            paired = i + 1 < len(self.base)
            yield (i, self.source_indices[i], value,
                   self.source_indices[i+1] if paired else None,
                   self.base[i+1] if paired else None,
                   self.sum_wave[i] if paired else None,
                   self.linear_wave[i] if paired else None,
                   self.product_wave[i] if paired else None)

    def SaveCSV(self, path):
        """Save exact integers; refuse to overwrite an existing file."""
        with Path(path).open('x', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(CSV_COLUMNS)
            writer.writerows(self.rows())
        return Path(path)


CSV_COLUMNS = ('sample_index', 'source_index', 'base_value', 'next_source_index',
               'next_base_value', 'sum_wave', 'linear_wave', 'product_wave')


class SignalBuilder(SignalParser):
    """Add signal construction without changing the existing parser class."""
    BuildSumWave = staticmethod(BuildSumWave)
    BuildLinearWave = staticmethod(BuildLinearWave)
    BuildProductWave = staticmethod(BuildProductWave)

    def BuildSignal(self, source, modulus=231, multiplier=22):
        """Build from Hebrew text or an integer iterable, preserving source indices.

        Text uses the parser's ordinary gematria and configured Hebrew overrides.
        Structural characters are skipped, retaining their gaps in source indices;
        the parser's unknown='error' rule instead rejects them. Numeric inputs use
        their sequence positions. No padding, wraparound pair or normalization.
        """
        modulus = _modulus(modulus)
        if isinstance(source, str):
            mapping = dict(self.HEBREW_GEMATRIA)
            mapping.update(self.rules['hebrew'])
            values, indices = [], []
            for index, glyph in enumerate(source):
                if glyph in mapping:
                    values.append(mapping[glyph])
                    indices.append(index)
                elif self.rules['unknown'] == 'error':
                    raise ValueError(f'no Hebrew rule for {glyph!r} at index {index}')
            values = _integers(values)
            indices = tuple(indices)
        else:
            values = _integers(source)
            indices = tuple(range(len(values)))
        return BuiltSignal(values, indices, BuildSumWave(values, modulus),
                           BuildLinearWave(values, modulus, multiplier),
                           BuildProductWave(values, modulus), modulus, multiplier)


def BuildSignal(source, modulus=231, multiplier=22, rules=None):
    """Convenience function equivalent to SignalBuilder(rules).BuildSignal(...)."""
    return SignalBuilder(rules).BuildSignal(source, modulus, multiplier)
