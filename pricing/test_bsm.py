"""
This file is to sanity test the call-spread model
The call spread has values close to N(d2)
So the numbers check out
"""

from bsm import call_spread_probability, prob_above

F, T, vol = 82.66, 0.00137, 0.86

for strike in (80, 82, 85):
    exact = prob_above(F, strike, T, vol)

    for width in (1.0, 0.1, 0.01):
        approx = call_spread_probability(F, strike - width / 2, strike + width / 2, T, vol)
        err = abs(approx - exact)
        print(f"strike={strike} width={width:<5} call_spread={approx:.6f} prob_above={exact:.6f} err={err:.6f}")
        assert err < width, f"call spread should approach prob_above as width shrinks (width={width})"

print("ok")
