import math
import os
from iexfinance.stocks import Stock

from Stock_Data import StockData


def getSymbol():
    string = input("Enter stock symbol: ")
    return Stock(string, token=os.environ['IEX_TOKEN'])


# Calculate CAGR (Compound Annual Growth) (end value / beginning value)^(1/n) - 1 for future revenue projections
def calculateCAGR(revenue):
    return (revenue[0] / revenue[len(revenue) - 1]) ** (1 / len(revenue))


# project revenue 5 years out
def calculateRevenueProjection(revenue, RevenueProjection, CAGR):
    RevenueProjection.append(math.trunc(revenue[0] * CAGR))
    for i in range(1, 5):
        RevenueProjection.append(math.trunc(RevenueProjection[i - 1] * CAGR))


# calculate average net margin
def calculateNetMargin(netIncome, revenue):
    netMargin = netIncome / revenue
    total = sum(netMargin)
    avgNetMargin = total / len(netMargin)
    print("net margin:", "%.2f" % (avgNetMargin * 100), "%")

    return avgNetMargin


# project net income 5 years
def caclulateNetIncomProjection(NetIncomeProjection, RevenueProjection, avgNetMargin):
    for i in range(0, 5):
        NetIncomeProjection.append(math.trunc(RevenueProjection[i] * avgNetMargin))


# calculate average FCF/NI ratio
def calculateFreeCashFlowNetIncomeRatio(FreeCashFlow, netIncome):
    FCF_NI_Ratio = FreeCashFlow / netIncome
    #print("FCF ratio", FCF_NI_Ratio)
    ratioTotal = sum(FCF_NI_Ratio)
    avgFreeCashFlowNetIncomeRatio = ratioTotal / len(FCF_NI_Ratio)
    #print("Average Net Income Ratio",  "%.2f" % ((avgFreeCashFlowNetIncomeRatio - 1) * 100), "%")

    return avgFreeCashFlowNetIncomeRatio


# project FCF
def calculateFreeCashFlowProjection(FCFProjection, NetIncomeProjection, avgFreeCashFlowNetIncomeRatio):
    for i in NetIncomeProjection:
        FCFProjection.append(math.trunc(i * avgFreeCashFlowNetIncomeRatio))
    #print("Free Cash Flow Projection:", FCFProjection)


# Calculate WACC
def calculateWACC(stock):
    debtWeight = calculateDebtWeight(stock)
    AdjustedCostOfDebt = calculateAdjustedCostOfDebt(stock)

    #  calculate CAPM risk free rate is chosen let's say 1.6% Rm market rate is 7.5%
    CostOfEquity = calculateCostOfEquity(stock, .015, .075)
    EquityWeight = calculateEquityWeight(CostOfEquity)

    EBIT = stock.IncomeStatement['ebit'][0]
    TaxExpense = stock.getIncomeStatement()['incomeTax'][0]

    # calculating WACC
    WACC = debtWeight * AdjustedCostOfDebt * (1 - (TaxExpense / EBIT)) + EquityWeight * CostOfEquity
    print("WACC:", "%.2F" % (WACC * 100), "%")

    return WACC


# calculate debt wright percent
def calculateDebtWeight(stock):
    totalDebt = stock.getBalanceSheet()['currentLongTermDebt'][0] + stock.getBalanceSheet()['longTermDebt'][0]
    marketCap = stock.getAdvanceStats()['marketcap'][0]

    return totalDebt / (totalDebt + marketCap)


# calculate adjusted cost of debt
def calculateAdjustedCostOfDebt(stock):
    totalDebt = stock.getBalanceSheet()['currentLongTermDebt'][0] + stock.getBalanceSheet()['longTermDebt'][0]
    EBIT = stock.IncomeStatement['ebit'][0]
    InterestExpense = stock.getIncomeStatement()['interestIncome'][0]
    TaxExpense = stock.getIncomeStatement()['incomeTax'][0]

    return (InterestExpense / totalDebt) * (1 - (TaxExpense / EBIT))


# calculate cost of equity
def calculateCostOfEquity(stock, riskFreeRate, marketRate):
    beta = stock.getAdvanceStats()['beta'][0]
    return riskFreeRate + beta * (marketRate - riskFreeRate)


# calculate equity weight
def calculateEquityWeight(debtWeight):
    return 1 - debtWeight


# calculate terminal value perpetual growth is relatively conservative 2.5-4% (us/world economy)
def calculateTerminalValue(PerpetualGrowthRate, FCFProjection, WACC):
    return (FCFProjection[4] * (1 + PerpetualGrowthRate)) / (WACC - PerpetualGrowthRate)


# print("Terminal Value:", TerminalValue)

# calculate Present Value of Free Cash Flow
def calculatePresentValue(PresentValueFreeCashFlow, FCFProjection, WACC, TerminalValue):
    for i in range(0, len(FCFProjection)):
        DiscountFactor = (1 + WACC) ** (i + 1)
        PresentValueFreeCashFlow.append(math.trunc(FCFProjection[i] / DiscountFactor))

    PresentTerminalValue = math.trunc(TerminalValue / DiscountFactor)
    PresentValueFreeCashFlow.append(PresentTerminalValue)

    # print("Present Terminal Value", PresentTerminalValue)
    # print("Present Value", PresentValueFreeCashFlow)


# calculate intrinsic value of the business
def calculateIntrinsicValue(stock, PresentValueFreeCashFlow):
    OustandingShares = stock.getAdvanceStats()['sharesOutstanding'][0]
    #print("Outstanding shares (millions):", OustandingShares / 1000000)
    IntrinsicValueOfBusiness = sum(PresentValueFreeCashFlow)
    #print("Intrinsic Value of the Business (millions):", IntrinsicValueOfBusiness / 1000000)
    FairValue = IntrinsicValueOfBusiness / OustandingShares
    print("Fair Value:", FairValue)
    return FairValue


def DCF(stock):
    RevenueProjection = []
    FCFProjection = []
    NetIncomeProjection = []
    PresentValueFreeCashFlow = []
    FreeCashFlow = stock.getCashFlowStatement()['cashFlow'] + stock.getCashFlowStatement()['capitalExpenditures']
    netIncome = stock.getIncomeStatement()['netIncome']
    revenue = stock.getIncomeStatement()['totalRevenue']

    calculateRevenueProjection(revenue, RevenueProjection, calculateCAGR(revenue))
    caclulateNetIncomProjection(NetIncomeProjection, RevenueProjection, calculateNetMargin(netIncome, revenue))
    calculateFreeCashFlowProjection(FCFProjection, NetIncomeProjection,
                                    calculateFreeCashFlowNetIncomeRatio(FreeCashFlow, netIncome))

    WACC = calculateWACC(stock)

    TV = calculateTerminalValue(.04, FCFProjection, WACC)

    calculatePresentValue(PresentValueFreeCashFlow, FCFProjection, WACC, TV)

    return calculateIntrinsicValue(stock, PresentValueFreeCashFlow)


def checkValid():
    while True:
        try:
            stock = StockData(getSymbol())
            break
        except Exception as e:
            print("Invalid Ticker")
    return stock


def main():
    stock = checkValid()
    DCF(stock)


if __name__ == "__main__":
    main()
