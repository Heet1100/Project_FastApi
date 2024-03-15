def error_loc(loc: list):
    """
    This function is used to return an error message when there
    is a validation exception.
    :param loc:list: Determine the location of the error
    :return: The location of the error
    """
    tokens = []
    for i in range(1, len(loc)):
        if str(loc[i]).isdigit():
            tokens.append("[" + str(loc[2]) + "]")
        else:
            tokens.append(loc[i])
    return ".".join(tokens)
