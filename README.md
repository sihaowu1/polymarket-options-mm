# Polymarket Options Market Making 

## Demo

## Background

Polymarket offers contracts like [these](https://polymarket.com/event/wti-closes-above-on-august-4-2026). 
They ask: "Will crude oil close above $80 on Aug 4?"
Since they are binary options, a "Yes" share trading at $0.73 implies a 73% chance to oil finishing above $80. 

But Polymarket is not the only market betting on that. 
We can extract information from oil options. 
Reusing that $80 example, we come up with an estimate using narrow options position such as a call spread:
* Buy the $79.50 strike call
* Sell the $80.50 strike call

Because these two strikes are so close together, the value of this spread behaves like an implied probability that oil finishes above $80, if we price it with Black-Scholes. 

## Trading

Now that we have the implied probability that oil will finish above a certain price, we can calculate the difference. 
Suppose that:
* Polymarket probability: 73%
* Options implied probability: 68%
* Difference: 5%

If Polymarket appears too expensive, we will short it by selling "Yes" contracts. Otherwise, we buy them. 

## Delta 

This also allows us to measure delta. For every point change in oil prices, we collect data on the changes in the Polymarket and options probability. 
The slope of the line would give us the delta. 

Essentially, we market-make on the Polymarket contract using relative pricing to options markets. 