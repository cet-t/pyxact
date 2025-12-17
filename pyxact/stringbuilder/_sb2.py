import ctypes


class stringbuilder:
    def __init__(self, *initial_parts: str):
        dll_path = "./pyxact/stringbuilder.dll"
        self.lib = ctypes.CDLL(dll_path)

        # 型定義
        self.lib.sb_create.restype = ctypes.c_void_p
        self.lib.sb_append.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.sb_append_line.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.sb_insert.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_char_p,
        ]
        self.lib.sb_insert_line.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_char_p,
        ]
        self.lib.sb_replace.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        self.lib.sb_to_string.argtypes = [ctypes.c_void_p]
        self.lib.sb_to_string.restype = ctypes.c_char_p
        self.lib.sb_raw.argtypes = [ctypes.c_void_p]
        self.lib.sb_raw.restype = ctypes.c_char_p
        self.lib.sb_lines.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        self.lib.sb_lines.restype = ctypes.c_char_p
        self.lib.sb_parts.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        self.lib.sb_parts.restype = ctypes.c_char_p
        self.lib.sb_flags.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        self.lib.sb_flags.restype = ctypes.c_bool
        self.lib.sb_copy.argtypes = [ctypes.c_void_p]
        self.lib.sb_copy.restype = ctypes.c_void_p
        self.lib.sb_flattened_copy.argtypes = [ctypes.c_void_p]
        self.lib.sb_flattened_copy.restype = ctypes.c_void_p
        self.lib.sb_free_string.argtypes = [ctypes.c_char_p]

        # インスタンス作成
        self._ptr = self.lib.sb_create()

        # 初期値追加（可変長引数）
        for part in initial_parts:
            self.append(part)

    def append(self, text: str):
        self.lib.sb_append(self._ptr, text.encode("utf-8"))

    def append_line(self, text: str):
        self.lib.sb_append_line(self._ptr, text.encode("utf-8"))

    def insert(self, index: int, text: str):
        self.lib.sb_insert(self._ptr, index, text.encode("utf-8"))

    def insert_line(self, index: int, text: str):
        self.lib.sb_insert_line(self._ptr, index, text.encode("utf-8"))

    def replace(self, old: str, new: str):
        self.lib.sb_replace(self._ptr, old.encode("utf-8"), new.encode("utf-8"))

    def to_string(self) -> str:
        raw = self.lib.sb_to_string(self._ptr)
        result = raw.decode("utf-8")
        self.lib.sb_free_string(raw)
        return result

    @property
    def raw(self) -> str:
        raw = self.lib.sb_raw(self._ptr)
        result = raw.decode("utf-8")
        self.lib.sb_free_string(raw)
        return result

    @property
    def parts(self) -> list[str]:
        result = []
        i = 0
        while True:
            part_ptr = self.lib.sb_parts(self._ptr, i)
            if not part_ptr:
                break
            result.append(part_ptr.decode("utf-8"))
            self.lib.sb_free_string(part_ptr)
            i += 1
        return result

    @property
    def flags(self) -> list[bool]:
        result = []
        i = 0
        while True:
            try:
                flag = self.lib.sb_flags(self._ptr, i)
                result.append(bool(flag))
                i += 1
            except:
                break
        return result

    def lines(self) -> list[str]:
        result = []
        i = 0
        while True:
            line_ptr = self.lib.sb_lines(self._ptr, i)
            if not line_ptr:
                break
            result.append(line_ptr.decode("utf-8"))
            self.lib.sb_free_string(line_ptr)
            i += 1
        return result

    def copy(self) -> "stringbuilder":
        new_ptr = self.lib.sb_copy(self._ptr)
        clone = stringbuilder()
        clone._ptr = new_ptr
        return clone

    def flattened_copy(self) -> "stringbuilder":
        new_ptr = self.lib.sb_flattened_copy(self._ptr)
        clone = stringbuilder()
        clone._ptr = new_ptr
        return clone

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return f"RustStringBuilder({self.lines()})"

    def __len__(self):
        return len(self.lines())

    def __getitem__(self, index: int) -> str:
        return self.lines()[index]

    def __iter__(self):
        return iter(self.lines())

    def __contains__(self, value: str) -> bool:
        return value in self.raw

    def __eq__(self, other):
        if isinstance(other, stringbuilder):
            return self.raw == other.raw
        elif isinstance(other, str):
            return self.raw == other
        return False

    def __add__(self, other):
        new = self.copy()
        if isinstance(other, stringbuilder):
            for line in other.lines():
                new.append(line)
        elif isinstance(other, str):
            new.append(other)
        else:
            raise TypeError("Unsupported operand type for +")
        return new

    def __iadd__(self, other):
        if isinstance(other, stringbuilder):
            for line in other.lines():
                self.append(line)
        elif isinstance(other, str):
            self.append(other)
        else:
            raise TypeError("Unsupported operand type for +=")
        return self

    def __radd__(self, other):
        if isinstance(other, str):
            new = self.copy()
            new.insert(0, other)
            return new
        raise TypeError("Unsupported operand type for radd")


if __name__ == "__main__":
    print("rustsb")
    sb = stringbuilder("!string!", "?builder?")
    print(sb)
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
    # print("sb_lines:", str(sb._stringbuilder__lines))
    # print("sb_parts:", str(sb._stringbuilder__parts))

    print(repr(sb))
    print(str(sb))
