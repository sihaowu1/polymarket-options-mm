# Polymarket Options Market Making 

## Background

Polymarket offers contracts like [these](https://polymarket.com/event/wti-closes-above-on-august-4-2026). 
They ask: "Will crude oil close above $80 on Aug 4?"
Since they are binary options, a "Yes" share trading at $0.73 implies a 73% chance to oil finishing above $80. 

But Polymarket is not the only market betting on that. 
We can extract information from oil options. 
If we price the 79.50/80.50 call spread in Black-Scholes at 90 IV with 30 DTE, you get a "fair" probability that oil finishes above $80. 

Sensitivity to volatility (aka vega) and time to expiry can be ignored, as vega is negligible for a call spread and time to expiry is mirrored in the Polymarket contract. 
So, that just gives us a probability that oil finishes above $80 for some future date. 

Because these two strikes are so close together, the value of this spread behaves like an implied probability that oil finishes above $80, if we price it with Black-Scholes. 

## Black-Scholes

If you look at the payoff diagram of the 79.50/80.50 call spread, you'll notice that the payoff is binary. That is:
* Pays $1 for above 80
* Loss $1 for below 80

!! include image here later

We have: implied probability ~ (Call(K1) - Call(K2)) / (K2 - K1), where Call(K) is the call price at strike K. We calculate Call(K) using Black-Scholes. 

We don't use the discounted or risk-neutral probability since for short dated contracts, the discount factor is very small. 

Also, note that in the payoff diagram, it doesn't jump from -$1 to $1 immediately across $80 underlying. So it's better interpreted as the average probability across the interval. Mathematically, this means:

(Call(K2) - Call(K1)) / (K2 - K1) = (1 / (K2 - K1)) integral from K1 to K2 (exp(-rT) * Q(S > K)) dK

where r is risk-free rate, T is time to expiry, Q is risk-neutral pricing distribution. we lowkey don't need this since our contract is so short-lived and narrow

## Trading

Now that we have the implied probability that oil will finish above a certain price, we can calculate the difference. 
Suppose that:
* Polymarket probability: 73%
* Options implied probability: 68%
* Difference: 5%

If Polymarket appears too expensive, we will short it by selling "Yes" contracts. Otherwise, we buy them. 

We only transact on Polymarket since there are no maker fees. 

## Delta 

This also allows us to measure delta. For every point change in oil prices, we collect data on the changes in the Polymarket and options probability. 
The slope of the line would give us the delta. 

Essentially, we market-make on the Polymarket contract using relative pricing to options markets. 

## Set Up
