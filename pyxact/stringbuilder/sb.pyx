import ctypes
from typing import Iterator, Optional, TypeGuard


class stringbuilder:
    def __init__(self, *value: object) -> None:
        self.__parts: list[str] = []
        self.__line_flags: list[bool] = []
        self.__lines: list[str] = []
        if value:
            self.append_line(*value)

    def append(self, *values: object) -> "stringbuilder":
        for value in values:
            self.__parts.append(str(value))
            self.__line_flags.append(False)
        self.__rebuild_lines()
        return self

    def append_line(self, *values: object) -> "stringbuilder":
        for v in values:
            self.__parts.append(str(v) + "\n")
            self.__line_flags.append(True)
        self.__rebuild_lines()
        return self

    def __rebuild_lines(self) -> None:
        self.__lines = [p[:-1] if p.endswith("\n") else p for p in self.__parts]

    def __rebuild_flags(self, new_str: str) -> None:
        self.__parts = new_str.splitlines(keepends=True)
        self.__line_flags = [p.endswith("\n") for p in self.__parts]
        self.__rebuild_lines()

    def insert(self, index: int, *values: object) -> "stringbuilder":
        parts = []
        flags = []

        for v in values:
            parts.append(str(v))
            flags.append(False)

        self.__parts[index:index] = parts
        self.__line_flags[index:index] = flags
        self.__rebuild_lines()
        return self

    def insert_line(self, index: int, *values: object) -> "stringbuilder":
        parts = []
        flags = []

        for value in values:
            parts.append(str(value) + "\n")
            flags.append(True)

        self.__parts[index:index] = parts
        self.__line_flags[index:index] = flags
        self.__rebuild_lines()
        return self

    def remove(self, start: int, length: int) -> "stringbuilder":
        s = self.raw
        self.__rebuild_flags(s[:start] + s[start + length :])
        return self

    def replace(self, old, new) -> "stringbuilder":
        s = self.raw.replace(str(old), str(new))
        self.__rebuild_flags(s)
        return self

    def clear(self) -> "stringbuilder":
        self.__parts.clear()
        self.__line_flags.clear()
        self.__lines.clear()
        return self

    def copy(self) -> "stringbuilder":
        sb = stringbuilder()
        sb.__parts = self.__parts.copy()
        sb.__line_flags = self.__line_flags.copy()
        sb.__rebuild_lines()
        return sb

    def copy_flattened(self) -> "stringbuilder":
        return stringbuilder(str(self))

    @property
    def raw(self) -> str:
        return "".join(self.__parts)

    @property
    def parts(self) -> list[str]:
        return self.__parts.copy()

    @property
    def lines(self) -> list[str]:
        return self.__lines.copy()

    @property
    def flags(self) -> list[bool]:
        return self.__line_flags.copy()

    def __str__(self) -> str:
        return "\n".join(self)

    def __repr__(self) -> str:
        preview = ", ".join(repr(p) for p in self.__parts[:3])
        if len(self.__parts) > 3:
            preview += ", ..."
        return f"<stringbuilder parts=[{preview}] len={len(self)}>"

    def __len__(self) -> int:
        return len(self.raw)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__lines)

    def __list__(self) -> list[str]:
        return self.__lines

    def __hash__(self) -> int:
        return hash(str(self))

    def __getitem__(self, k: int | slice) -> str:
        return self.raw[k]

    def __setitem__(self, k: int, v: str) -> "stringbuilder":
        full = self.raw
        if not isinstance(v, str) or len(v) != 1:
            raise ValueError()
        new_str = full[:k] + v + full[k + 1 :]
        self.__rebuild_flags(new_str)
        return self

    def __delitem__(self, key: int | slice) -> None:
        full = self.raw
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop if key.stop is not None else len(full)
            step = key.step or 1
            if step != 1:
                indices = set(range(start, stop, step))
                new_str = "".join(c for i, c in enumerate(full) if i not in indices)
            else:
                new_str = full[:start] + full[stop:]
        else:
            new_str = full[:key] + full[key + 1 :]
        self.__rebuild_flags(new_str)

    def __add__(self, other: object) -> "stringbuilder":
        result = stringbuilder()
        result.__parts = self.__parts.copy()
        result.__line_flags = self.__line_flags.copy()
        if self.__is_sb(other):
            result.__parts.extend(other.__parts)
            result.__line_flags.extend(other.__line_flags)
        else:
            result.append(str(other))
        result.__rebuild_lines()
        return result

    def __radd__(self, other: object) -> "stringbuilder":
        result = stringbuilder()
        if self.__is_sb(other):
            result.__parts = other.__parts.copy()
            result.__line_flags = other.__line_flags.copy()
        else:
            result.append(str(other))
        result.__parts.extend(self.__parts)
        result.__line_flags.extend(self.__line_flags)
        result.__rebuild_lines()
        return result

    def __iadd__(self, other: object) -> "stringbuilder":
        if self.__is_sb(other):
            self.__parts.extend(other.__parts)
            self.__line_flags.extend(other.__line_flags)
        else:
            self.append(str(other))
        self.__rebuild_lines()
        return self

    def __is_sb(self, a: object) -> TypeGuard["stringbuilder"]:
        return isinstance(a, stringbuilder)


if __name__ == "__main__":
    sb = stringbuilder("!string!", "?builder?")
    print("sb:", list(sb))

    sb.append_line("Hello")
    print("append_line:", list(sb))

    sb.append("World")
    print("append:", list(sb))

    sb.insert(-1, "INSERT")
    print("insert:", list(sb))

    sb.insert_line(3, "INSERT_LINE")
    print("insert_line:", list(sb))

    sb.append_line("APPEND_LINE")
    print("append_line:", list(sb))

    sb.replace("e", "è")
    print("replace:", list(sb))

    sb = sb + stringbuilder("__ADD__")
    print("__add__:", list(sb))

    sb = "__RADD__" + sb
    print("__radd__:", list(sb))

    sb += "__IADD__"
    print("__iadd__:", list(sb))
    print("sb_lines:", str(sb._stringbuilder__lines))
    print("sb_parts:", str(sb._stringbuilder__parts))

    print(repr(sb))
    print(str(sb))

    print("rustsb")
