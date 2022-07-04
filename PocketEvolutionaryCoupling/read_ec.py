def read_ec(infile):
    """
    this function read EC values from the output of pmlc program
    """
    ec = {}
    try:
        data = open(infile,'r').readlines()
    except IOError,io:
        exit('IOError: %s' % str(io))
    for line in data:
        x = line.split()
        tmpkey = (x[0],x[1],x[2],x[3])
        ec[tmpkey] = x[5]
    return ec
