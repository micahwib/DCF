class StockData:
    def __init__(self, symbol):
        # Advanaced Fundamentals call does not support all stocks.
        self.CashFlowStatement = symbol.get_cash_flow(period='annual', last=4)
        self.IncomeStatement = symbol.get_income_statement(period='annual', last=4)
        self.BalanceSheet = symbol.get_balance_sheet(period='annual')
        self.AdvanceStats = symbol.get_advanced_stats()

    def getCashFlowStatement(self):
        return self.CashFlowStatement

    def getIncomeStatement(self):
        return self.IncomeStatement

    def getBalanceSheet(self):
        return self.BalanceSheet

    def getAdvanceStats(self):
        return self.AdvanceStats

