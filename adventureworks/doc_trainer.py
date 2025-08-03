from adventureworks.base_trainer import BaseTrainer


class DocTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):

        vn = self.vn

        vn.train(documentation='The schema person contains objects related \
                 to names and addresses of customers, vendors, and employees')
        vn.train(documentation='The schema HumanResources contains objects \
                 related to employees and departments.')
        vn.train(documentation='The employee is considered as active in \
                 department if the EndDate in EmployeeDepartmentHistory \
                 is null, i.e., there is not end date of that record')
        vn.train(documentation='The employee is considered as inactive \
                 in department if the EndDate in EmployeeDepartmentHistory \
                 is not null, i.e., there is not end date of that record')
        vn.train(documentation='The employee is a person. When looking for \
                 the employee name, look for the person associated with \
                 the employee from the person table and show the \
                 relevant information')
        vn.train(documentation="The age of the employee is years between \
                 today and the date of birth of the employee and is \
                 always represented in years")
        vn.train(documentation="The employee names are present in the \
                 Person.person table. The businessEntityID is used to join \
                 the HumanResources.employee table with the \
                 Person.person table.")

        vn.train(documentation='COMMENT ON TABLE Person.Person IS Human \
                 beings involved with AdventureWorks: employees, \
                 customer contacts, \
                 and vendor contacts.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.Person.BusinessEntityID \
                 IS Primary key for Person records.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.PersonType \
                 IS Primary type of person: SC = Store Contact, \
                 IN = Individual (retail) customer, SP = Sales person, \
                 EM = Employee (non-sales), VC = Vendor contact, \
                 GC = General contact')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.NameStyle \
                 IS 0 = The data in FirstName and LastName are stored \
                 in western style (first name, last name) order.  \
                 1 = Eastern style (last name, first name) order.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.Title IS \
                 A courtesy title. For example, Mr. or Ms.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.FirstName IS \
                 First name of the person.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.MiddleName IS \
                 Middle name or middle initial of the person.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.LastName IS \
                 Last name of the person.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.Suffix IS \
                 Surname suffix. For example, Sr. or Jr.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.Person.EmailPromotion \
                 IS 0 = Contact does not wish to receive e-mail promotions, \
                 1 = Contact does wish to receive e-mail promotions \
                 from AdventureWorks, 2 = Contact does wish to receive \
                 e-mail promotions from AdventureWorks and selected partners.')
        vn.train(documentation='COMMENT ON COLUMN Person.Person.Demographics \
                 IS Personal information such as hobbies, and income \
                 collected from online shoppers. Used for sales analysis.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.Person.AdditionalContactInfo IS \
                 Additional contact information about the person stored \
                 in xml format.')

        vn.train(documentation='COMMENT ON TABLE Sales.PersonCreditCard IS \
                 Cross-reference table mapping people to their credit card \
                 information in the CreditCard table.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.PersonCreditCard.BusinessEntityID IS Business entity \
                 identification number. Foreign key to \
                 Person.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.PersonCreditCard.CreditCardID IS Credit card \
                 identification number. Foreign key to \
                 CreditCard.CreditCardID.')

        vn.train(documentation='COMMENT ON TABLE Person.PersonPhone IS \
                 Telephone number and type of a person.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.PersonPhone.BusinessEntityID IS \
                 Business entity identification number. Foreign key to \
                 Person.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.PersonPhone.PhoneNumber IS Telephone number \
                 identification number.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Person.PersonPhone.PhoneNumberTypeID IS Kind of phone number.\
                  Foreign key to PhoneNumberType.PhoneNumberTypeID.')

        vn.train(documentation='COMMENT ON TABLE Purchasing.Vendor IS \
                 Companies from whom Adventure Works Cycles purchases \
                 parts or other goods.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Purchasing.Vendor.BusinessEntityID IS Primary key \
                 for Vendor records.  Foreign key to \
                 BusinessEntity.BusinessEntityID')
        vn.train(documentation='COMMENT ON COLUMN \
                 Purchasing.Vendor.AccountNumber IS Vendor account \
                 (identification) number.')
        vn.train(documentation='COMMENT ON COLUMN Purchasing.Vendor.Name IS \
                Company name.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Purchasing.Vendor.CreditRating IS 1 = Superior, \
                 2 = Excellent, 3 = Above average, 4 = Average, \
                 5 = Below average')
        vn.train(documentation='COMMENT ON COLUMN \
                 Purchasing.Vendor.PreferredVendorStatus IS \
                 0 = Do not use if another vendor is available. \
                 1 = Preferred over other vendors supplying the same product.')
        vn.train(documentation='COMMENT ON COLUMN Purchasing.Vendor.ActiveFlag\
                 IS  0 = Vendor no longer used. 1 = Vendor is actively used.')
        vn.train(documentation='COMMENT ON COLUMN \
                Purchasing.Vendor.PurchasingWebServiceURL IS Vendor URL.')

        vn.train(documentation='COMMENT ON TABLE Sales.SalesOrderDetail IS \
                 Individual products associated with a specific sales order. \
                 See SalesOrderHeader.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.SalesOrderID IS Primary key. \
                 Foreign key to SalesOrderHeader.SalesOrderID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.SalesOrderDetailID IS Primary key. \
                 One incremental unique number per product sold.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.CarrierTrackingNumber IS \
                 Shipment tracking number supplied by the shipper.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.OrderQty IS \
                 Quantity ordered per product.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.ProductID IS Product \
                 sold to customer. Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.SpecialOfferID IS Promotional code. \
                 Foreign key to SpecialOffer.SpecialOfferID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.UnitPrice IS Selling price \
                 of a single product.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderDetail.UnitPriceDiscount IS Discount amount.')

        vn.train(documentation='COMMENT ON TABLE Sales.SalesOrderHeader IS \
                 General sales order information.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.SalesOrderID IS Primary key.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.RevisionNumber IS Incremental number \
                 to track changes to the sales order over time.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.OrderDate IS Dates the sales order \
                 was created.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.DueDate IS Date the order is due \
                 to the customer.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.ShipDate IS Date the order was \
                 shipped to the customer.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.Status IS Order current status. \
                 1 = In process) 2 = Approved) 3 = Backordered) 4 = Rejected) \
                 5 = Shipped) 6 = Cancelled')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.OnlineOrderFlag IS \
                 0 = Order placed by sales person. \
                 1 = Order placed online by customer.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.PurchaseOrderNumber IS Customer \
                 purchase order number reference.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.AccountNumber IS \
                 Financial accounting number reference.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.CustomerID IS \
                 Customer identification number. \
                 Foreign key to Customer.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.SalesPersonID IS Sales person who \
                 created the sales order. \
                 Foreign key to SalesPerson.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.TerritoryID IS Territory in which \
                 the sale was made. \
                 Foreign key to SalesTerritory.SalesTerritoryID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.BillToAddressID IS Customer \
                 billing address. Foreign key to Address.AddressID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.ShipToAddressID IS Customer \
                 shipping address. Foreign key to Address.AddressID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.ShipMethodID IS Shipping method.\
                 Foreign key to ShipMethod.ShipMethodID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.CreditCardID IS Credit card \
                 identification number. Foreign key to \
                 CreditCard.CreditCardID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.CreditCardApprovalCode IS \
                 Approval code provided by the credit card company.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.CurrencyRateID IS Currency exchange \
                 rate used. Foreign key to CurrencyRate.CurrencyRateID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.SubTotal IS Sales subtotal. \
                 Computed as SUM(SalesOrderDetail.LineTotal) for the \
                 appropriate SalesOrderID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.TaxAmt IS Tax amount.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.Freight IS Shipping cost.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.TotalDue IS Total due from customer.\
                  Computed as Subtotal + TaxAmt + Freight.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeader.Comment IS Sales \
                 representative comments.')

        vn.train(documentation='COMMENT ON TABLE \
                 Sales.SalesOrderHeaderSalesReason IS Cross-reference \
                 table mapping sales orders to sales reason codes.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeaderSalesReason.SalesOrderID IS \
                 Primary key. Foreign key to SalesOrderHeader.SalesOrderID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Sales.SalesOrderHeaderSalesReason.SalesReasonID IS \
                 Primary key. Foreign key to SalesReason.SalesReasonID.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SalesPerson IS Sales representative current information.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesPerson.BusinessEntityID IS Primary key for SalesPerson records. Foreign key to Employee.BusinessEntityID')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesPerson.TerritoryID IS Territory currently assigned to. Foreign key to SalesTerritory.SalesTerritoryID.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPerson.SalesQuota IS Projected yearly sales.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPerson.Bonus IS Bonus due if quota is met.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPerson.CommissionPct IS Commision percent received per sale.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPerson.SalesYTD IS Sales total year to date.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPerson.SalesLastYear IS Sales total of previous year.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SalesPersonQuotaHistory IS Sales performance tracking.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesPersonQuotaHistory.BusinessEntityID IS Sales person identification number. Foreign key to SalesPerson.BusinessEntityID.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPersonQuotaHistory.QuotaDate IS Sales quota date.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesPersonQuotaHistory.SalesQuota IS Sales quota amount.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SalesReason IS Lookup table of customer purchase reasons.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesReason.SalesReasonID IS Primary key for SalesReason records.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesReason.Name IS Sales reason description.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesReason.ReasonType IS Category the sales reason belongs to.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SalesTaxRate IS Tax rate lookup table.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTaxRate.SalesTaxRateID IS Primary key for SalesTaxRate records.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTaxRate.StateProvinceID IS State, province, or country/region the sales tax applies to.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTaxRate.TaxType IS 1 = Tax applied to retail transactions, 2 = Tax applied to wholesale transactions, 3 = Tax applied to all sales (retail and wholesale) transactions.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesTaxRate.TaxRate IS Tax rate amount.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesTaxRate.Name IS Tax rate description.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SalesTerritory IS Sales territory lookup table.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.TerritoryID IS Primary key for SalesTerritory records.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesTerritory.Name IS Sales territory description')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.CountryRegionCode IS ISO standard country or region code. Foreign key to CountryRegion.CountryRegionCode.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.Group IS Geographic area to which the sales territory belong.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SalesTerritory.SalesYTD IS Sales in the territory year to date.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.SalesLastYear IS Sales in the territory the previous year.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.CostYTD IS Business costs in the territory year to date.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritory.CostLastYear IS Business costs in the territory the previous year.')

        vn.train(documentation='COMMENT ON TABLE Sales.SalesTerritoryHistory IS Sales representative transfers to other sales territories.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritoryHistory.BusinessEntityID IS Primary key. The sales rep.  Foreign key to SalesPerson.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritoryHistory.TerritoryID IS Primary key. Territory identification number. Foreign key to SalesTerritory.SalesTerritoryID.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritoryHistory.StartDate IS Primary key. Date the sales representive started work in the territory.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SalesTerritoryHistory.EndDate IS Date the sales representative left work in the territory.')

        vn.train(documentation='COMMENT ON TABLE Sales.ShoppingCartItem IS Contains online customer orders until the order is submitted or cancelled.')
        vn.train(documentation='COMMENT ON COLUMN Sales.ShoppingCartItem.ShoppingCartItemID IS Primary key for ShoppingCartItem records.')
        vn.train(documentation='COMMENT ON COLUMN Sales.ShoppingCartItem.ShoppingCartID IS Shopping cart identification number.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.ShoppingCartItem.Quantity IS Product quantity ordered.')
        vn.train(documentation='COMMENT ON COLUMN Sales.ShoppingCartItem.ProductID IS Product ordered. Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN Sales.ShoppingCartItem.DateCreated IS Date the time the record was created.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.SpecialOffer IS Sale discounts lookup table.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SpecialOffer.SpecialOfferID IS Primary key for SpecialOffer records.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.Description IS Discount description.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.DiscountPct IS Discount precentage.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.Type IS Discount type category.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SpecialOffer.Category IS Group the discount applies to such as Reseller or Customer.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.StartDate IS Discount start date.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.EndDate IS Discount end date.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.MinQty IS Minimum discount percent allowed.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.SpecialOffer.MaxQty IS Maximum discount percent allowed.')

        vn.train(documentation='COMMENT ON TABLE Sales.SpecialOfferProduct IS Cross-reference table mapping products to special offer discounts.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SpecialOfferProduct.SpecialOfferID IS Primary key for SpecialOfferProduct records.')
        vn.train(documentation='COMMENT ON COLUMN Sales.SpecialOfferProduct.ProductID IS Product identification number. Foreign key to Product.ProductID.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.Store IS Customers (resellers) of Adventure Works products.')
        vn.train(documentation='COMMENT ON COLUMN Sales.Store.BusinessEntityID IS Primary key. Foreign key to Customer.BusinessEntityID.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Store.Name IS Name of the store.')
        vn.train(documentation='COMMENT ON COLUMN Sales.Store.SalesPersonID IS ID of the sales person assigned to the customer. Foreign key to SalesPerson.BusinessEntityID.')
        vn.train(documentation='COMMENT ON COLUMN Sales.Store.Demographics IS Demographic informationg about the store such as the number of employees, annual sales and store type.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.Currency IS Lookup table containing standard ISO currencies.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Currency.CurrencyCode IS The ISO code for the Currency.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Currency.Name IS Currency name.')

        vn.train(
            documentation='COMMENT ON TABLE Sales.CurrencyRate IS Currency exchange rates.')
        vn.train(documentation='COMMENT ON COLUMN Sales.CurrencyRate.CurrencyRateID IS Primary key for CurrencyRate records.')
        vn.train(documentation='COMMENT ON COLUMN Sales.CurrencyRate.CurrencyRateDate IS Date and time the exchange rate was obtained.')
        vn.train(documentation='COMMENT ON COLUMN Sales.CurrencyRate.FromCurrencyCode IS Exchange rate was converted from this currency code.')
        vn.train(documentation='COMMENT ON COLUMN Sales.CurrencyRate.ToCurrencyCode IS Exchange rate was converted to this currency code.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.CurrencyRate.AverageRate IS Average exchange rate for the day.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.CurrencyRate.EndOfDayRate IS Final exchange rate for the day.')

        vn.train(documentation='COMMENT ON TABLE Sales.Customer IS Current customer information. Also see the Person and Store tables.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Customer.CustomerID IS Primary key.')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Customer.PersonID IS Foreign key to Person.BusinessEntityID')
        vn.train(
            documentation='COMMENT ON COLUMN Sales.Customer.StoreID IS Foreign key to Store.BusinessEntityID')
        vn.train(documentation='COMMENT ON COLUMN Sales.Customer.TerritoryID IS ID of the territory in which the customer is located. Foreign key to SalesTerritory.SalesTerritoryID.')

        vn.train(documentation='COMMENT ON TABLE  Production.Product IS Products sold or used in the manfacturing of sold products.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.ProductID IS Primary key for Product records.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Name IS Name of the product.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.ProductNumber IS Unique product identification number.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.MakeFlag IS 0 = Product is purchased, 1 = Product is manufactured in-house.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.FinishedGoodsFlag IS 0 = Product is not a salable item. 1 = Product is salable.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Color IS Product color.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.SafetyStockLevel IS Minimum inventory quantity.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.ReorderPoint IS Inventory level that triggers a purchase order or work order.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.StandardCost IS Standard cost of the product.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.ListPrice IS Selling price.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Size IS Product size.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.SizeUnitMeasureCode IS Unit of measure for Size column.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.WeightUnitMeasureCode IS Unit of measure for Weight column.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Weight IS Product weight.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.DaysToManufacture IS Number of days required to manufacture the product.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.ProductLine IS R = Road, M = Mountain, T = Touring, S = Standard')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Class IS H = High, M = Medium, L = Low')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.Style IS W = Womens, M = Mens, U = Universal')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.ProductSubcategoryID IS Product is a member of this product subcategory. Foreign key to ProductSubCategory.ProductSubCategoryID.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.ProductModelID IS Product is a member of this product model. Foreign key to ProductModel.ProductModelID.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.SellStartDate IS Date the product was available for sale.')
        vn.train(documentation='COMMENT ON COLUMN Production.Product.SellEndDate IS Date the product was no longer available for sale.')
        vn.train(
            documentation='COMMENT ON COLUMN Production.Product.DiscontinuedDate IS Date the product was discontinued.')

        vn.train(documentation='COMMENT ON TABLE  Production.ProductCategory IS High-level product categorization.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCategory.ProductCategoryID IS Primary key for ProductCategory records.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCategory.Name IS Category description.')

        vn.train(documentation='COMMENT ON TABLE  Production.ProductCostHistory IS Changes in the cost of a product over time.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCostHistory.ProductID IS Product identification number. Foreign key to Product.ProductID')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCostHistory.StartDate IS Product cost start date.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCostHistory.EndDate IS Product cost end date.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductCostHistory.StandardCost IS Standard cost of the product.')

        vn.train(documentation='COMMENT ON TABLE  Production.ProductDescription IS Product descriptions in several languages.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductDescription.ProductDescriptionID IS Primary key for ProductDescription records.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductDescription.Description IS Description of the product.')

        vn.train(documentation='COMMENT ON TABLE  Production.ProductDocument IS Cross-reference table mapping products to related product documents.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductDocument.ProductID IS Product identification number. Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductDocument.DocumentNode IS Document identification number. Foreign key to Document.DocumentNode.')

        vn.train(documentation='COMMENT ON TABLE  Production.ProductInventory IS Product inventory information.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductInventory.ProductID IS Product identification number. Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductInventory.LocationID IS Inventory location identification number. Foreign key to Location.LocationID.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductInventory.Shelf IS Storage compartment within an inventory location.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductInventory.Bin IS Storage container on a shelf in an inventory location.')
        vn.train(documentation='COMMENT ON COLUMN Production.ProductInventory.Quantity IS Quantity of products in the inventory location.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductListPriceHistory IS Changes in the \
                 list price of a product over time.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductListPriceHistory.ProductID IS \
                 Product identification number. \
                 Foreign key to Product.ProductID')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductListPriceHistory.StartDate IS \
                 List price start date.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductListPriceHistory.EndDate IS \
                 List price end date')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductListPriceHistory.ListPrice IS \
                 Product list price.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductModel IS Product model classification.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModel.ProductModelID IS Primary key \
                 for ProductModel records.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModel.Name IS Product model description.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModel.CatalogDescription IS \
                 Detailed product catalog information in xml format.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModel.Instructions IS Manufacturing \
                 instructions in xml format.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductModelIllustration IS \
                 Cross-reference table mapping product models \
                 and illustrations.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModelIllustration.ProductModelID0 \
                 IS Primary key. \
                 Foreign key to ProductModel.ProductModelID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModelIllustration.IllustrationID IS \
                 Primary key. \
                 Foreign key to Illustration.IllustrationID.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductModelProductDescriptionCulture \
                 IS Cross-reference table mapping product descriptions \
                 and the language the description is written in.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModelProductDescriptionCulture.ProductModelID \
                 IS Primary key. \
                 Foreign key to ProductModel.ProductModelID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModelProductDescriptionCulture.ProductDescriptionID \
                 IS Primary key. \
                 Foreign key to ProductDescription.ProductDescriptionID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductModelProductDescriptionCulture.CultureID \
                 IS Culture identification number. \
                 Foreign key to Culture.CultureID.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductPhoto IS Product images.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductPhoto.ProductPhotoID IS \
                 Primary key for ProductPhoto records.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductPhoto.ThumbNailPhoto IS \
                 Small image of the product.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductPhoto.ThumbnailPhotoFileName IS \
                 Small image file name.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductPhoto.LargePhoto IS \
                 Large image of the product.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductPhoto.LargePhotoFileName IS \
                 Large image file name.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductProductPhoto IS Cross-reference \
                 table mapping products and product photos.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductProductPhoto.ProductID IS \
                 Product identification number. \
                 Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductProductPhoto.ProductPhotoID IS \
                 Product photo identification number. \
                 Foreign key to ProductPhoto.ProductPhotoID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductProductPhoto.Primary IS \
                 0 = Photo is not the principal image. \
                 1 = Photo is the principal image.')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductReview IS Customer reviews of products \
                 they have purchased.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.ProductReviewID IS Primary key \
                 for ProductReview records.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.ProductID IS \
                 Product identification number. \
                 Foreign key to Product.ProductID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.ReviewerName IS Name of \
                 the reviewer.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.ReviewDate IS Date review \
                 was submitted.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.EmailAddress IS Reviewers \
                 e-mail address.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.Rating IS Product rating \
                 given by the reviewer. Scale is 1 to 5 with 5 as \
                 the highest rating.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductReview.Comments IS Reviewers comments')

        vn.train(documentation='COMMENT ON TABLE  \
                 Production.ProductSubcategory IS Product subcategories. \
                 See ProductCategory table.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductSubcategory.ProductSubcategoryID IS \
                 Primary key for ProductSubcategory records.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductSubcategory.ProductCategoryID IS \
                 Product category identification number. \
                 Foreign key to ProductCategory.ProductCategoryID.')
        vn.train(documentation='COMMENT ON COLUMN \
                 Production.ProductSubcategory.Name IS \
                 Subcategory description.')

        vn.train(documentation='Production schema contains objects related to \
                 products, inventory, and manufacturing.')
        vn.train(documentation='the column ProductSubcategoryID in the \
                 Product table defines the subcategory to which the product \
                 belongs to. Foreign key to \
                 ProductSubCategory.ProductSubCategoryID.')
        vn.train(documentation='Prouduction.Product is a table that defines \
                 the various products. The products belong to different \
                 subcategories and models. \
                 See also ProductCategory table and ProductModel table.')
        vn.train(documentation='Prouduction.ProductSubcategory is a table \
                 that defines the Product subcategories. \
                 See also ProductCategory table.')
        vn.train(documentation='Prouduction.ProductCategory is a table \
                 that defines the Product categories.')
        vn.train(documentation='the column ProductSubcategoryID in the \
                 Product table defines the subcategory to which the product \
                 belongs to. \
                 Foreign key to ProductSubCategory.ProductSubCategoryID.')
        vn.train(documentation='the column ProductCategoryID in the \
                 productSubCategory table defines the productCategory \
                 that the subcategory belongs to. \
                 Foreign key to ProductCategory.ProductCategoryID.')
        vn.train(documentation='The schema purchasing contains objects \
                 related to vendors and purchase orders')

        vn.train(documentation='Purchasing.ProductVendor is \
                 cross-reference table mapping vendors with \
                 the products they supply.')
        vn.train(documentation='Purchasing.PurchaseOrderDetail is \
                 individual products associated with a specific \
                 purchase order. See PurchaseOrderHeader.')
        vn.train(documentation='Purchasing.PurchaseOrderHeader is \
                 general purchase order information. See PurchaseOrderDetail.')

        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.ProductID is \
                 Primary key. Foreign key to Product.ProductID.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.BusinessEntityID is \
                 Primary key. Foreign key to Vendor.BusinessEntityID.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.AverageLeadTime is \
                 The average span of time (in days) between placing an \
                 order with the vendor and receiving the purchased product.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.StandardPrice is \
                 The vendor''s usual selling price.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.LastReceiptCost is \
                 The selling price when last purchased.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.LastReceiptDate is \
                 Date the product was last received by the vendor.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.MinOrderQty is \
                 The maximum quantity that should be ordered.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.MaxOrderQty is \
                 The minimum quantity that should be ordered.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.OnOrderQty is \
                 The quantity currently on order.')
        vn.train(documentation='The column in \
                 Purchasing.ProductVendor.UnitMeasureCode is \
                 The product''s unit of measure.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.PurchaseOrderID is \
                 Primary key. Foreign key to \
                 PurchaseOrderHeader.PurchaseOrderID.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.PurchaseOrderDetailID is \
                 Primary key. One line number per purchased product.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.DueDate is \
                 Date the product is expected to be received.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.OrderQty is \
                 Quantity ordered.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.ProductID is \
                 Product identification number. \
                 Foreign key to Product.ProductID.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.UnitPrice is \
                 Vendor''s selling price of a single product.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.ReceivedQty is \
                 Quantity actually received from the vendor.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderDetail.RejectedQty is \
                 Quantity rejected during inspection.')

        vn.train(documentation='The column in \
                Purchasing.PurchaseOrderHeader.PurchaseOrderID \
                    is Primary key.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.RevisionNumber is \
                 Incremental number to track changes to the purchase \
                 order over time.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.Status is \
                 Order current status. 1 = Pending) \
                 2 = Approved) 3 = Rejected) 4 = Complete')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.EmployeeID is \
                 Employee who created the purchase order. \
                 Foreign key to Employee.BusinessEntityID.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.VendorID is \
                 Vendor with whom the purchase order is placed. \
                 Foreign key to Vendor.BusinessEntityID.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.ShipMethodID is \
                 Shipping method. Foreign key to ShipMethod.ShipMethodID.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.OrderDate is \
                 Purchase order creation date.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.ShipDate is \
                 Estimated shipment date from the vendor.')
        vn.train(documentation='The column in \
                Purchasing.PurchaseOrderHeader.SubTotal \
                    is Purchase order subtotal.')
        vn.train(documentation='The column in \
                Purchasing.PurchaseOrderHeader.TaxAmt \
                is Tax amount.')
        vn.train(documentation='The column in \
                 Purchasing.PurchaseOrderHeader.Freight \
                 is Shipping cost.')

        vn.train(documentation="The vendor is identified by BusinessEntityId \
                 in Purchasing.Vendor table. Use that to join with \
                 vendorId columns in other tables.")
        vn.train(documentation="Purchasing.Vendor table is joined with \
                 Purchasing.PurchaseOrderHeader table to get the details \
                 of the purchased by vendor. \
                 Vendor.BusinessEntityId = PurchaseOrderHeader.VendorId \
                 will be the join condition")
        vn.train(documentation='Purchasing.PurchaseOrderDetail is joined with \
                 Production.Product table to get the product details')
        vn.train(documentation="When getting the purchase details by vendor, \
                 always use Purchasing.PurchaseOrderHeader to join with \
                 the Purchasing.Vendor table. \
                 Do not join PurchaseOrderDetail to the vendor table directly")
        vn.train(documentation="Purchasing.PurchaseOrderDetail has the \
                 details of the product and the quantity. \
                 When responding to requests on the product or quantity, \
                 use the Purchasing.PurchaseOrderDetail table")
        vn.train(documentation="The sale amount by a vendor is indicated by \
                 the subtotal amount in Purchasing.PurchaseOrderHeader table.")
        vn.train(documentation="OTIF stands for on time delivery and in full. \
                 This can be identified by looking at Sales.SalesOrderHeader \
                 table and checking the difference between order date and \
                 shipping date. If the difference is greater than 1 day, \
                 it is considered not delivered on time and in full.")

        vn.train(documentation="The Sales.Customer is joined \
                 with Person.Person \
                 table customer.personid = person.businessentityid")
        vn.train(documentation="The customer name is retrieved from the \
                Person.Person table")
        vn.train(documentation="The customer gender is not stored in \
            any table")
        vn.train(documentation="The order line amount is calculated as the \
                 product of the quantity and the unit price")
        vn.train(documentation="Customer address are maintained in address \
                 table. Customer needs to be joined with person table. \
                 Person needs to be joined by businessEntityAddress table \
                 on businessEntityId. BusinessEntityAddress table needs to be \
                 joined with address table on addressId column")

        vn.train(documentation="Delayed shipment is defined as the difference \
                 between the sales order date and the ship date. If the \
                 difference is greater than 5 days, it is considered delayed")


if __name__ == "__main__":
    doc_trainer = DocTrainer()
    doc_trainer.train()
