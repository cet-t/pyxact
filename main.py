<<<<<<< HEAD
from dataclasses import dataclass
from seriapyze import serialize
from typing import Optional


@dataclass
@serialize
class Human:
    name: str
    parent: "Optional[Human]"


if __name__ == "__main__":
    parent = Human("parent", None)
    child = Human("child", parent)

    user_json = child.to_json(indent=2)
    print("\njson:\n" + user_json)

    user_yaml = child.to_yaml(indent=2)
    print("\nyaml:\n" + user_yaml)

    user_toml = child.to_toml()
    print("\ntoml:\n" + user_toml)
=======
from pyxact.stringbuilder import stringbuilder

sb = stringbuilder()
sb.append("hello")
sb.append(", ", "world").append_line("!")
sb.insert(0, ">>> ")
print(str(sb))
>>>>>>> parent of 4a00248 (pyxact構成変更)
