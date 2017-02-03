def version2str(ver):
    ver = map(str, ver)
    return ".".join(ver[:3]) + "".join(ver[3:])

__version__ = (0, 5, 1, "rc", 1)

version_str = version2str(__version__)
