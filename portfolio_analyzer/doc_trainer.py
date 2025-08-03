from portfolio_analyzer.base_trainer import BaseTrainer


class DocTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn

        vn.train(documentation="COMMENT ON TABLE public.Asset_Info contains the \
                different assets being traded. ")
        vn.train(documentation="COMMENT ON COLUMN Asset_Info.asset_info_id contains \
                the unique identifier for each asset. this is the \
                primary key for the table")
        vn.train(documentation="COMMENT ON COLUMN Asset_Info.ticker contains the \
                ticker code for the asset being traded")
        vn.train(documentation="COMMENT ON COLUMN Asset_Info.cusip contains the \
                9 digit CUSIP code for the asset")
        vn.train(documentation="COMMENT ON COLUMN Asset_Info.scrip_name contains the \
                scrip name associated with the asset")

        vn.train(documentation="Asset_Info table only contains the details of stock. \
                It does not have any information on mutual funds or derivatives")
        vn.train(documentation="Asset_Info.scrip_name is the stock name.")
        vn.train(documentation="Asset_Info.scrip_name is the asset name.")
        vn.train(documentation="Asset_Info.cusip is a nine-digit alphanumeric code \
                that is used to identify securities, such as stocks, bonds, \
                and other financial instruments.")


        vn.train(documentation="COMMENT ON TABLE public.account_info contains the \
                details of the accounts. It has the account name, the status of the \
                account and the tax id of the account holder.")
        vn.train(documentation="COMMENT ON COLUMN account_info.account_id contains \
                the unique identifier for each account. The values are \
                auto generated and this column is the primary key for the table")
        vn.train(documentation="COMMENT ON COLUMN account_info.account_name contains \
                the full name of the account holder. The format is first name and \
                last name seperated by a space")
        vn.train(documentation="COMMENT ON COLUMN account_info.start_date contains \
                the date on which the account was started.")
        vn.train(documentation="COMMENT ON COLUMN account_info.end_date contains \
                the date on which the account was closed. Active accounts will \
                not have an end date")
        vn.train(documentation="COMMENT ON COLUMN account_info.account_status contains \
                the status of the account. The values are 'Active' and 'Closed'")
        vn.train(documentation="COMMENT ON COLUMN account_info.primary_owner_tax_id \
                column contains the tax id of the account holders. \
                It contains the full tax id of the account holder.")

        vn.train(documentation="account_info.Primary_Owner_Tax_Id also contains the \
                SSN number for individuals.")
        vn.train(documentation="account_info.Primary_Owner_Tax_Id contains unique \
                identifier of the account holder or location.")
        vn.train(documentation="account_info.Primary_Owner_Tax_Id has the first \
                set of three digits is called the Area Number.")
        vn.train(documentation="account_info.Primary_Owner_Tax_Id has the second \
                set of two digits is called the Group Number.")
        vn.train(documentation="account_info.Primary_Owner_Tax_Id has the \
                final set of four digits is the Serial Number.")

        vn.train(documentation="COMMENT ON TABLE public.Portfolio contains the \
                different portfolio for each account. An Account can have \
                multiple portfolios.")
        vn.train(documentation="COMMENT ON COLUMN Portfolio.portfolio_id contains the \
                unique identifier for each portfolio. The values are auto generated \
                and this column is the primary key for the table")
        vn.train(documentation="COMMENT ON COLUMN Portfolio.portfolio_name contains \
                the name of each portfolio")
        vn.train(documentation="COMMENT ON COLUMN Portfolio.account_id contains the \
                account that this portfolio belongs to. \
                This column is a foreign key to the account_info table")

        vn.train(documentation="COMMENT ON TABLE public.Portfolio_Asset_Map contains \
                the mapping between each portfolios and assets. Each portfolio can \
                contain more than 1 asset")
        vn.train(documentation="COMMENT ON COLUMN \
                Portfolio_Asset_Map.portfolio_asset_map_id \
                contains the unique identifier for each portfolio and asset mapping. \
                The values are auto generated and this column is the \
                primary key for the table")
        vn.train(documentation="COMMENT ON COLUMN Portfolio_Asset_Map.portfolio_id \
                contains the portfolio that this asset belongs to. \
                This column is a foreign key to the portfolio table")
        vn.train(documentation="COMMENT ON COLUMN Portfolio_Asset_Map.asset_info_id \
                contains the asset that is part of the portfolio. \
                This column is a foreign key to the asset_info table")

        vn.train(documentation="COMMENT ON TABLE public.Pricing_Info contains the \
                pricing information of an asset on a particular date. \
                It has the different prices for the given date.")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.pricing_info_id \
                contains the unique identifier for each pricing information. \
                The values are auto generated and this column is the primary key \
                for the table")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.asset_info_id contains \
                the asset for which the pricing pricing information is defined. \
                This column is a foreign key to the asset_info table")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.pricing_date contains \
                the date for which the pricing information is defined")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.Last_Traded_Price is \
                the stock price for the given pricing date")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.Volume is the total \
                number of stocks traded for a given asset on the pricing date")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.Open_Price is the \
                stock price at which the market opened for the given pricing date")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.High_Price is the \
                highest the stock price went for the given pricing date")
        vn.train(documentation="COMMENT ON COLUMN Pricing_Info.Low_Price is the \
                lowest the stock price went for the given pricing date")

        vn.train(documentation="COMMENT ON TABLE public.Transaction_Info contains the \
                transaction details of each transaction. It has the details of the \
                transaction date, the asset and portfolio, the quantity and the \
                price at which the asset was transacted. It also contains the \
                fee and tax on each transaction")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_info_id\
                contains the unique identifier for each transaction. The values are \
                auto generated and this column is the primary key for the table")
        vn.train(documentation="COMMENT ON COLUMN \
                Transaction_Info.portfolio_asset_map_id \
                contains the portfolio asset mapping for which the transaction was \
                executed. This column is a foreign key to the \
                portfolio_asset_map table")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_date \
                contains the date for which the transaction was execueted. \
                It is also the date on which the trade was done.")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.quantity contains \
                the quantity of stocks or assets purchased.")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_price \
                contains the amount at which the stock or asset was purchased.")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_fee \
                contains the fees charged for each transaction. \
                The fees is 30% of the transaction price")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_tax \
                contains the tax charged for each transction. \
                The tax is 10% of the transaction price")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.settlement_date \
                contains the date on which the settlement was done.")
        vn.train(documentation="COMMENT ON COLUMN \
                Transaction_Info.transaction_description \
                contains the date for which the transaction was execueted")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.performed_by_user \
                contains the date for which the transaction was execueted")
        vn.train(documentation="COMMENT ON COLUMN Transaction_Info.transaction_status \
                contains the information whether the transaction is \
                successful or failed.")

        vn.train(documentation="Trade date is when a transaction is executed.")
        vn.train(documentation="Transaction Price is the product of quantity \
                in the transaction_info and last_traded_price that is available \
                in the pricing_info table")
        vn.train(documentation="LTP refers to the last traded price of the asset.")
        vn.train(documentation="Trade refers to the transaction of \
                buying or selling of an asset.")


if __name__ == "__main__":
    doc_trainer = DocTrainer()
    doc_trainer.train()