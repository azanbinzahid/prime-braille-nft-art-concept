# Sieve of Eratosthenes
# David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/


def gen_primes(start, max_count):
    """ Generate an infinite sequence of prime numbers.
    """
    D = {}  # map composite integers to primes witnessing their compositeness
    q = 2   # first integer to test for primality
    count = 0

    while count < max_count:
        if q not in D:
            if q >= start:  # ignore if not falls in range
                count += 1
                yield q     # not marked composite, must be prime

            D[q*q] = [q]    # first multiple of q not already marked
        else:
            for p in D[q]:  # move each witness to its next multiple
                D.setdefault(p+q, []).append(p)
            del D[q]        # no longer need D[q], free memory
        q += 1
