from dataclasses import dataclass
from datetime import date, timedelta
from random import randint
from uuid import UUID, uuid4
from pyxact import linq
from pyxact.sb import stringbuilder
import pyxact.ts as ts


@dataclass
class User:
    name: str
    uuid: UUID
    registerd_at: date


if __name__ == "__main__":
    users = linq.linq[User]()
    today = date.today()

    for i in range(1, 100, 2):
        uuid = uuid4()
        users.append(User(uuid.hex, uuid, today))
        today += timedelta(days=1)

    print("\n".join(users.select(lambda e: f"{e.name} - {e.registerd_at}")))

    time = ts.from_seconds(randint(0, 60 * 60 * 24))
    print(time)
    print(-time * 2)

    sb = stringbuilder()
    sb.append_line("[append_line1]", "[append_line2]")
    sb.insert_line(0, "[insert_line10]", "[insert_line20]")
    sb.append("[append1]", "[append2]")
    print(sb)
