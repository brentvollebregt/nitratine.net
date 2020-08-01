def chunk_list(l, n):
    """ Yield successive n-sized chunks from l. src: https://stackoverflow.com/a/312464 """
    for i in range(0, len(l), n):
        yield l[i:i + n]
