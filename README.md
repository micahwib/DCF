# DCF
This program uses IEX Cloud's API: https://iexcloud.io. In addition the IEXFinance library was used: https://github.com/addisonlynch/iexfinance.

This program is a Discounted Cash Flow Model which projects future free cash flow of a company out 5 years and discounts future free cash 
to a present value to determine whether or not the company is over/under valued at it's current stock price. This program uses WACC to calculate
the Net Present Value of a company. Future revenue growth was projected using an average growth of the past 4 years and net income was projected by
using the average net margin over the last 4 years multiplied by the projected revenue. Feel free to let me know if I need to fine tune the calculation,
whether my math is completely off or if I oversimplified projections/assumptions. 

Assumptions are hard coded. This Project is merely a stepping stone for a bigger future project of mine thus the simple design and code.
