import time 
import webbrowser 

def open_urls(urls):
    """opens an arbitrary number of urls each in a new tab"""
    for url in urls:
        webbrowser.open_new(url)
        time.sleep(1)

def n_to_s(n, money=False, per=False):
    """truncates num and formats it as dollar or percent"""
    if money:
        return f"${abs(n):.2f}"
    if per:
        return f"{abs(n):.2f}%"
    return f"{n:.2f}"

def hl(s, color):
    """changes the color of a string"""
    return f"\033[{color}m{s}\033[0m"

def pretty_n_to_s(n, money=False, percentage=False, yellow=False):
    """converts num to colored, signed string"""
    s = n_to_s(n, money, percentage)
    if yellow:
        return hl(s, 93)
    if n > 0 and percentage:
        return hl(f"({s})", 92)
    if n > 0:
        return hl("+"+s, 92)
    if n < 0 and percentage:
        return hl(f"({s})", 91)
    if n < 0:
        return hl("-"+s, 91)
    return hl(s, 0)