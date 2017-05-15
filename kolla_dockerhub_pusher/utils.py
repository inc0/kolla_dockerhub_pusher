def get_file_name(base, type, release):
    fname = "{base}-{type}-registry-{release}.tar.gz".format(
        base = base,
        type = type,
        release = release)
    return fname
