

def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def fib_memo(n, memo):
    if n <= 1:
        return n
    elif memo[n] == -1:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

n = 32

memo=[-1] * (n + 1)
fib_memo(n, memo)

def fib_tab(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

#print(fib_tab(32))

def coin_change_memo(S, memo):
    if S <= 0:
        return 0
    elif S not in memo:
        memo[S] = 1 + min(coin_change_memo(S - 1, memo),
                      coin_change_memo(S - 4, memo),
                      coin_change_memo(S - 5, memo))
    return memo[S]

def which_coins(S, coin_change):
    coins = [1, 4, 5]

    coins_used = [0, 0, 0]

    while S > 0:
        smallest_number = float('inf')
        smallest_coin = 0
        for i in range(len(coins)):
            n = S - coins[i]
            if n >= 0:
                if (coin_change[n] < smallest_number):
                    smallest_number = coin_change[n]
                    smallest_coin = i
        coins_used[smallest_coin] += 1
        S -= coins[smallest_coin]
    return coins_used

def coin_change_tab(S):
    dp = [float('inf')] * (S + 1)
    dp[0] = 0
    for i in range(1, S + 1):
        dp[i] = 1 + min(dp[i - 1], dp[i - 4], dp[i - 5])

    coins_used = which_coins(S, dp)
    print("The sum \"" + str(S) + "\" was achieved with " + str(coins_used[0]) + " \"1\"'s, " + \
        str(coins_used[1]) + " \"4\"'s, and " + str(coins_used[2]) + " \"5\"'s")

    return dp[S]

if __name__=="__main__":

    s = 8
    memo = [float('inf')] * (s + 1)
    minimum_coins = coin_change_memo(s, memo)

    s = 13
    minimum_coins_tab = coin_change_tab(s)

