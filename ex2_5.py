
def geometric(p, k):
    """
    probability for k coin tosses in a geometric distribution with coint p (failure rate)
    """
    if k == 0:
        return 0
    return (1 - p) ** (k - 1) * p


assert geometric(0.5, 0) == 0
assert geometric(0.5, 1) == 0.5
assert geometric(0.3, 2) == 0.3*0.7


def geometric_cdf(p, k):
    """
    probability for k coin tosses in a geometric distribution with coin p (failure rate)
    """
    if p==1: # edge case treatment
        return int(k==1)
    return p*(1-(1-p)**k)/(1-p)  # p(q + q^2 +...+q^k) = p(1-q^k)/q


assert geometric_cdf(0.5, 10) == sum([geometric(0.5, i) for i in range(11)])


def coupon(N, k, N_total=None):
    """
    probability to have k coupons before collecting all N variation
    N - coupon types left to collect
    k - coupons left to collect (aka try amount)
    N_orig - total coupon amount

    Note: implementation from the presentation in lecture 3 slide 21
    """
    if N_total is None:  # if not defined, we assume N is the total coupon amount
        N_total = N
    # stopping conditions
    if k < N or k == 0:  # not possible to achieve cases
        return 0
    if N == 1: # completing the last coupon
        return geometric_cdf(1/N_total, k) # if we want P(T_N=k) we can change geometric_cdf with geometric
    # convolution on N-1
    # (sum over probabilities for collecting N-1 coupons with some k' and then getting
    # the final coupon with k-k')
    prob_new = N / N_total  # probability to get a coupon we already see
    conv_results = []
    for i in range(1, k):
        conv_part = geometric(prob_new, k - i) * coupon(N - 1, i, N_total)
        conv_results.append(conv_part)
    result = sum(conv_results)
    return result

assert coupon(2,2)==0.5
assert coupon(2,3)==0.75

def coupon_DP(N, k, N_total=None):
    """
    Same as coupon method but with dynamic programming implementation
    :param N:
    :param k:
    :param N_total:
    :return:
    """
    if N_total is None:
        N_total = N
    if k==0:
        return 0

    M = [[0]*k for _ in range(N)] # N rows, k columns (starting from 0)
    # (M[i][j] = probability to collect i different coupons with at least j tries)
    M[0][0] = geometric(1 / N_total, 1) # case N=k=1
    for n in range(N):
        prob_new = (n+1) / N_total
        for j in range(k):
            if n == 0:
                M[n][j] = M[n][j - 1] + geometric(prob_new, j + 1)
            else:
                for i in range(k):
                    M[n][j] = M[n][j] + geometric(prob_new, k - i) * M[n - 1][i]
    return M[N-1][k-1]


assert coupon_DP(2,5) == coupon(2,5)
