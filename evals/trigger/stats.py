#!/usr/bin/env python3
"""Stdlib-only statistics for the trigger pressure test's repeated-sampling runs.

Two functions, both exact (no normal approximation):

`clopper_pearson_upper(k, n, alpha=0.05)` -- the one-sided Clopper-Pearson upper
confidence bound on a binomial rate: the smallest p such that
P(X <= k; n, p) = alpha, i.e. the value a fresh sample of n trials from a
true rate above this bound would be unlikely (at level alpha) to produce k or
fewer fires. What it is NOT: a statement about any model, harness, or
phrasing other than the one exact sample it was computed from. A bound
computed at n=5 for one phrasing on one day with one model says nothing about
another phrasing, another model, or the same phrasing next month.

`fisher_exact_two_tailed(a, b, c, d)` -- the exact two-tailed p-value for a
2x2 contingency table `[[a, b], [c, d]]`, computed by summing the
hypergeometric probability of every table sharing the same marginal totals
whose probability is at or below the observed table's. What it is NOT: a
per-phrasing verdict. This project uses it exactly once per round, on the
POOLED must-not-fire 2x2 (total over-fires vs. total non-fires, control vs.
treatment). Pooling treats the five must-not-fire phrasings as exchangeable,
which they are not -- each phrasing has its own unknown fire rate. The pooled
p is a summary statistic about the round as a whole, not a claim about any
single phrasing.

Both functions import only `math` (`math.comb`) from the standard library,
matching this repository's zero-dependency posture.

Usage:
    python3 evals/trigger/stats.py --self-test
"""

import argparse
import math
import sys

DEFAULT_ALPHA = 0.05


def clopper_pearson_upper(k, n, alpha=DEFAULT_ALPHA):
    """One-sided upper Clopper-Pearson bound on the true rate, given k fires in n trials.

    k == n: no p in [0, 1) satisfies P(X <= k; n, p) = alpha (the CDF at k is
    identically 1 for every p when k == n), so the bound is 1.0 by definition.

    k == 0: closed form. P(X <= 0; n, p) = (1 - p) ** n, so the equation
    (1 - p) ** n = alpha solves directly to p = 1 - alpha ** (1 / n).

    k > 0: no closed form is used here on purpose -- the tail is inverted by
    bisection on the monotonically-decreasing CDF, so this function proves
    the general case rather than special-casing every k.
    """
    if n <= 0:
        raise ValueError('n must be positive')
    if k < 0 or k > n:
        raise ValueError('k must be between 0 and n')
    if k == n:
        return 1.0
    if k == 0:
        return 1.0 - alpha ** (1.0 / n)

    def cdf(p):
        return sum(math.comb(n, i) * p ** i * (1.0 - p) ** (n - i) for i in range(k + 1))

    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if cdf(mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def fisher_exact_two_tailed(a, b, c, d):
    """Exact two-tailed p-value for the 2x2 table [[a, b], [c, d]].

    Fixes the row and column margins from the observed table, enumerates
    every table with those same margins, and sums the hypergeometric
    probability of every table at or below the observed table's own
    probability -- the standard definition of the two-tailed exact test. A
    relative tolerance on the comparison guards against floating-point
    equality silently dropping the observed table's own mirror image on the
    other tail.
    """
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    n = row1 + row2
    if n == 0:
        return 1.0
    denom = math.comb(n, col1)

    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    probs = {}
    for x in range(lo, hi + 1):
        probs[x] = math.comb(row1, x) * math.comb(row2, col1 - x) / denom

    observed = probs[a]
    rel_tol = 1e-7
    threshold = observed * (1.0 + rel_tol)
    return sum(p for p in probs.values() if p <= threshold)


# --- self-test ---------------------------------------------------------

_CP_CASES = [
    # (k, n, expected upper bound to 4 dp)
    (0, 1, 0.9500),
    (0, 3, 0.6316),
    (0, 5, 0.4507),
    (0, 10, 0.2589),
    (0, 20, 0.1391),
    (0, 59, 0.0495),
]

_FISHER_CASES = [
    # (a, b, c, d, expected p to 4 dp) -- table [[a, b], [c, d]]
    (3, 2, 0, 5, 0.1667),
    (5, 0, 0, 5, 0.0079),
    (2, 8, 0, 10, 0.4737),
    (5, 5, 0, 10, 0.0325),
    (7, 3, 0, 10, 0.0031),
    (4, 16, 0, 20, 0.1060),
]


def self_test():
    """Prove both functions against values DEBUG-cat10-trigger-over-fire.md already published."""
    failures = []
    case_count = 0

    for k, n, expected in _CP_CASES:
        case_count += 1
        got = round(clopper_pearson_upper(k, n), 4)
        if got != expected:
            failures.append('clopper_pearson_upper(%d, %d) = %.4f, expected %.4f'
                             % (k, n, got, expected))

    case_count += 1
    got = clopper_pearson_upper(5, 5)
    if got != 1.0:
        failures.append('clopper_pearson_upper(5, 5) = %r, expected 1.0 (k == n)' % (got,))

    for a, b, c, d, expected in _FISHER_CASES:
        case_count += 1
        got = round(fisher_exact_two_tailed(a, b, c, d), 4)
        if got != expected:
            failures.append('fisher_exact_two_tailed(%d, %d, %d, %d) = %.4f, expected %.4f'
                             % (a, b, c, d, got, expected))

    case_count += 1
    got = fisher_exact_two_tailed(0, 25, 0, 25)
    if got != 1.0:
        failures.append('fisher_exact_two_tailed(0, 25, 0, 25) = %r, expected 1.0 '
                         '(no fires in either arm)' % (got,))

    case_count += 1
    got = fisher_exact_two_tailed(0, 20, 0, 20)
    if got != 1.0:
        failures.append('fisher_exact_two_tailed(0, 20, 0, 20) = %r, expected 1.0 '
                         '(no fires in either arm, different n)' % (got,))

    for problem in failures:
        print('FAIL: %s' % problem)
    if failures:
        print('self-test FAIL: %d problem(s)' % len(failures))
        return 1
    print('self-test PASS: %d cases' % case_count)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--self-test', action='store_true',
                         help='run the offline value checks and exit (no model call)')
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
