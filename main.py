from pyxact.stringbuilder import stringbuilder

sb = stringbuilder()
sb.append("hello")
sb.append(", ", "world").append_line("!")
sb.insert(0, ">>> ")
print(str(sb))
