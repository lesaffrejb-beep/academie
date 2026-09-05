"""Instant réel puis identité originale ; aucune réécriture du journal.

Les anciennes dates sans offset sont interprétées en UTC. La fraction est
comparée comme décimale exacte, sans troncature à la microseconde.
"""
import re
from datetime import datetime, timezone
from decimal import Decimal


def cle_chronologique(ligne):
    quand = str(ligne.get('quand', ''))
    match = re.fullmatch(r'(\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2})(?:\.(\d+))?([Zz]|[+-]\d{2}:\d{2})?', quand)
    try:
        if not match:
            raise ValueError('date illisible')
        debut, fraction, zone = match.groups()
        date = datetime.fromisoformat(debut.upper() + (zone or '+00:00').upper().replace('Z', '+00:00'))
        instant = int((date.astimezone(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds())
        precision = Decimal('0.' + (fraction or '0'))
        return (1, instant, precision, quand, str(ligne.get('mode', '')), str(ligne.get('nonce', '')))
    except ValueError:
        return (0, 0, Decimal(0), quand, str(ligne.get('mode', '')), str(ligne.get('nonce', '')))
