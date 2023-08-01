import time 
import webbrowser 

def open_urls(urls):
    """opens an arbitrary number of urls each in a new tab"""
    for url in urls:
        webbrowser.open_new(url)
        time.sleep(1)

def n_to_s(n, money=False, per=False):
    """truncates num and formats it as currency or percent"""
    if money:
        return f'${n:.2f}'
    if per:
        return f'{n:.2f}%'
    return f'{n:.2f}'

def pretty_n_to_s(n, money=False, percentage=False, yellow=False):
    """converts num to colored, signed string"""
    s = n_to_s(n, money, percentage)
    def append_to(x): 
        return x + '\033[0m'
    if yellow:
        return append_to(f'\033[93m{s}')
    if n > 0 and percentage:
        return append_to(f'\033[92m({s})')
    if n > 0:
        return append_to(f'\033[92m+{s}')
    if n < 0 and percentage:
        return append_to(f'\033[91m({s})')
    if n < 0:
        return append_to(f'\033[91m{s}')
    return append_to(s)