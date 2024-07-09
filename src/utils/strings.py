def add_plural_suffix(name: str) -> str:
    if any(name.endswith(suffix) for suffix in ("s", "x", "z", "ch", "sh")):
        return name + "es"
    elif name.endswith("y") and name[-2] not in "aeiou":
        return name[:-1] + "ies"
    else:
        return name + "s"
