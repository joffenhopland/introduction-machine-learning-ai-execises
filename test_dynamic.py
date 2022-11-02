import timeit

exec_time_recursive = timeit.timeit(stmt="fib(32)",
                          setup="from dynamic import fib",
                          number=10) / 10

memo_code = '''
n = 32
memo=[-1]*(n+1)
fib_memo(n, memo)
'''
exec_time_memo = timeit.timeit(stmt=memo_code,
                          setup="from dynamic import fib_memo",
                          number=10) / 10

exec_time_tab = timeit.timeit(stmt="fib_tab(32)",
                          setup="from dynamic import fib_tab",
                          number=10) / 10

print(f"Execution time for recursive fibonacci : {exec_time_recursive}s")
print(f"Execution time for memoized fibonacci: {exec_time_memo}s")
print(f"Execution time for tabular fibonacci: {exec_time_tab}s")

