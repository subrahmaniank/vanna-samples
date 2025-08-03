from portfolio_analyzer.base_trainer import BaseTrainer


class SQLTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn

        vn.train(sql='select * from transaction_info ti \
                 inner join portfolio_asset_map pam \
                   on ti.portfolio_asset_map_id  = pam.portfolio_asset_map_id \
                 inner join portfolio p \
                   on pam.portfolio_id  = p.portfolio_id  \
                 inner join asset_info ai \
                   on pam.asset_info_id  = ai.asset_info_id \
                 inner join account_info ai2 \
                   on ai2.account_id = p.account_id; ')

        vn.train(question='Six Months back - what would have been the best \
                 stock to buy if I wanted steady growth \
                 with least variations?',
                 sql="with last_traded_price_picker as \
                    ( select scrip_name, min(last_traded_price) as minltp \
                    , max(last_traded_price) as maxltp \
                    , max(last_traded_price) - min(last_traded_price) as diff \
                    from (select ai.scrip_name, \
                            pi.last_traded_price, \
                            pricing_date as maxdate \
                        from pricing_info pi \
                            inner join asset_info ai \
                              on pi.asset_info_id = ai.asset_info_id \
                        where pricing_date < \
                            (CURRENT_DATE - INTERVAL '6 MONTH') \
                        ) \
                    group by scrip_name  \
                    ) \
                    select scrip_name, diff \
                    from last_traded_price_picker \
                    order by diff asc limit 1;")


if __name__ == "__main__":
    trainer = SQLTrainer()
    trainer.train()
