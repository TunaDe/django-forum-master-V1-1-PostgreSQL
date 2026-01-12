# Minimal re-implementation of distutils.version.LooseVersion
# sufficient for Django 3.1 usage. Uses packaging if available.
from __future__ import annotations

try:
    from packaging.version import Version as _PkgVersion  # type: ignore
except Exception:  # packaging may be unavailable; fall back to naive string compare
    class _PkgVersion:  # type: ignore
        def __init__(self, v: str) -> None:
            self.v = str(v)
        def __lt__(self, other: "_PkgVersion") -> bool: return self.v < other.v
        def __le__(self, other: "_PkgVersion") -> bool: return self.v <= other.v
        def __eq__(self, other: object) -> bool:
            if not isinstance(other, _PkgVersion):
                return False
            return self.v == other.v
        def __ne__(self, other: object) -> bool:
            if not isinstance(other, _PkgVersion):
                return True
            return self.v != other.v
        def __gt__(self, other: "_PkgVersion") -> bool: return self.v > other.v
        def __ge__(self, other: "_PkgVersion") -> bool: return self.v >= other.v

class LooseVersion:
    def __init__(self, vstring: str) -> None:
        self.vstring = vstring
        self._v = _PkgVersion(vstring)
    def __repr__(self) -> str:
        return f"LooseVersion ('{self.vstring}')"
    def __lt__(self, other: "LooseVersion") -> bool: return self._v < other._v
    def __le__(self, other: "LooseVersion") -> bool: return self._v <= other._v
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LooseVersion):
            return False
        return self._v == other._v
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, LooseVersion):
            return True
        return self._v != other._v
    def __gt__(self, other: "LooseVersion") -> bool: return self._v > other._v
    def __ge__(self, other: "LooseVersion") -> bool: return self._v >= other._v
