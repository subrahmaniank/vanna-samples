from portfolio_analyzer.base_trainer import BaseTrainer


class DDLTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn

        vn.train(ddl='CREATE TABLE Asset_Info ( \
            Asset_Info_ID SERIAL PRIMARY KEY, \
            Ticker TEXT NOT NULL, \
            Cusip TEXT NOT NULL, \
            Scrip_Name TEXT NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE Pricing_Info ( \
            Pricing_Info_ID SERIAL PRIMARY KEY, \
            Asset_Info_ID INTEGER REFERENCES Asset_Info(Asset_Info_ID), \
            Pricing_Date DATE NOT NULL, \
            Last_Traded_Price REAL NOT NULL, \
            Volume REAL, \
            Open_Price REAL, \
            High_Price REAL, \
            Low_Price REAL \
        );')

        '''
        vn.train(ddl='CREATE TABLE Historical_Pricing_Info ( \
            Pricing_Date DATE NOT NULL, \
            Last_Traded_Price REAL NOT NULL, \
            Volume INTEGER, \
            Open REAL, \
            High REAL, \
            Low REAL, \
            Ticker TEXT, \
            Cusip TEXT, \
            Scrip_Name TEXT \
        );')

        '''

        vn.train(ddl='CREATE TABLE account_info ( \
        account_id SERIAL PRIMARY KEY, \
        account_name TEXT, \
        account_start_date DATE, \
        account_end_date DATE, \
        account_status TEXT, \
        primary_owner_tax_id TEXT \
        );')

        vn.train(ddl='CREATE TABLE portfolio ( \
            portfolio_id SERIAL PRIMARY KEY, \
            portfolio_name TEXT, \
            account_id INTEGER REFERENCES account_info(account_id) \
        );')

        vn.train(ddl='CREATE TABLE portfolio_asset_map ( \
            portfolio_asset_map_id SERIAL PRIMARY KEY, \
            portfolio_id INTEGER REFERENCES portfolio(portfolio_id), \
            asset_info_id INTEGER REFERENCES asset_info(asset_info_id) \
        );')

        vn.train(ddl='CREATE TABLE transaction_info ( \
            transaction_info_id SERIAL PRIMARY KEY, \
            portfolio_asset_map_id INTEGER REFERENCES \
                 portfolio_asset_map(portfolio_asset_map_id), \
            transaction_date DATE, \
            quantity REAL, \
            transaction_price REAL, \
            transaction_fee REAL, \
            transaction_tax REAL, \
            settlement_date DATE, \
            transaction_description TEXT, \
            performed_by_user TEXT, \
            transaction_status TEXT \
        );')

        vn.train(ddl='CREATE TABLE generated_name_info ( \
            first_name TEXT, \
            middle_name TEXT, \
            last_name TEXT, \
            full_name TEXT \
        );')


if __name__ == "__main__":
    ddl_trainer = DDLTrainer()
    ddl_trainer.train()
