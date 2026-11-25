"""Strict data loader (Zack 2026-11-25): every planner reads game numbers through here.
Source = Idleon Toolbox's own parser run on the save (snapshots/<save>/tb_parsed.json.gz, built by tools/tb_parse.sh).
Anything missing or empty RAISES DataMissing instead of quietly returning nothing, so no card can skip a check.

    from data import load
    D = load()                       # latest snapshot
    D.system('sailing')              # whole section for a system in model/data_map.yaml
    D.get('account.sailing.captains')
    D.char('Autistocat')['level']
    D.age_hours                      # how old the game save is
"""
import gzip, json, time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SNAPS = ROOT / 'snapshots'
MAP = yaml.safe_load(open(ROOT / 'model' / 'data_map.yaml'))


class DataMissing(Exception):
    pass


def _empty(v):
    return v is None or (isinstance(v, (list, dict, str)) and len(v) == 0)


class Data:
    def __init__(self, stamp=None):
        self.stamp = stamp or (SNAPS / 'LATEST').read_text().strip()
        f = SNAPS / self.stamp / 'tb_parsed.json.gz'
        if not f.exists():
            raise DataMissing(f"no Toolbox parse for {self.stamp}: run tools/tb_parse.sh {self.stamp}")
        self.raw = json.load(gzip.open(f))
        self.account, self.characters = self.raw['account'], self.raw['characters']
        self.save_time = self.raw.get('_meta', {}).get('parsed_at_save_time')
        self.age_hours = (time.time() - self.save_time) / 3600 if self.save_time else None

    def get(self, path, allow_empty=False):
        node = self.raw
        for part in path.split('.'):
            if isinstance(node, dict) and part in node:
                node = node[part]
            elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
                node = node[int(part)]
            else:
                raise DataMissing(f"{path}: '{part}' not in the parsed save ({self.stamp})")
        if not allow_empty and _empty(node):
            raise DataMissing(f"{path}: present but empty ({self.stamp})")
        return node

    def system(self, name, allow_empty=False):
        m = MAP.get(name)
        if m is None:
            raise DataMissing(f"system '{name}' is not in model/data_map.yaml")
        if m.get('meta'):
            raise DataMissing(f"'{name}' is an AutoReview meta group, not game data")
        p = m.get('path')
        if not p:
            raise DataMissing(f"'{name}' is not in Toolbox's parser: use AutoReview / the raw save and say so")
        if p.startswith('@characters.'):
            field = p.split('.', 1)[1]
            out = {c.get('name', str(i)): c.get(field) for i, c in enumerate(self.characters)}
            if not allow_empty and all(_empty(v) for v in out.values()):
                raise DataMissing(f"{name}: every character's {field} is empty ({self.stamp})")
            return out
        return self.get('account.' + p, allow_empty)

    def item_count(self, raw):
        """Owned count of an item (storage chest + every character's bags), by game raw name (e.g. 'Coral3')."""
        n = sum(i.get('amount') or 0 for i in self.get('account.storage.list', True) if i.get('rawName') == raw)
        for c in self.characters:
            n += sum(i.get('amount') or 0 for i in (c.get('inventory') or []) if isinstance(i, dict) and i.get('rawName') == raw)
        return n

    def char(self, name):
        for c in self.characters:
            if c.get('name') == name:
                return c
        raise DataMissing(f"character {name} not in the parsed save ({self.stamp})")


def load(stamp=None):
    return Data(stamp)
