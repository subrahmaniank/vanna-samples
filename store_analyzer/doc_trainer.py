from store_analyzer.base_trainer import BaseTrainer


class DocTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):

        vn = self.vn

        # Here are the comments for each table and its columns in the `dvdrental` database:

        # Table: actor
        vn.train(
            documentation="COMMENT ON TABLE actor IS Stores information about actors.")
        vn.train(
            documentation="COMMENT ON COLUMN actor.actor_id IS Unique identifier for each actor.")
        vn.train(
            documentation="COMMENT ON COLUMN actor.first_name IS First name of the actor.")
        vn.train(
            documentation="COMMENT ON COLUMN actor.last_name IS Last name of the actor.")
        vn.train(
            documentation="COMMENT ON COLUMN actor.last_update IS Timestamp of the last update to the actor record.")

        # Table: actor_info
        vn.train(
            documentation="COMMENT ON VIEW actor_info IS View that combines actor information with film details.")
        vn.train(
            documentation="COMMENT ON COLUMN actor_info.actor_id IS Unique identifier for each actor.")
        vn.train(
            documentation="COMMENT ON COLUMN actor_info.first_name IS First name of the actor.")
        vn.train(
            documentation="COMMENT ON COLUMN actor_info.last_name IS Last name of the actor.")
        vn.train(documentation="COMMENT ON COLUMN actor_info.film_info IS Information about films associated with the actor.")

        # Table: address
        vn.train(
            documentation="COMMENT ON TABLE address IS Stores address details for customers and staff.")
        vn.train(
            documentation="COMMENT ON COLUMN address.address_id IS Unique identifier for each address.")
        vn.train(
            documentation="COMMENT ON COLUMN address.address IS Primary address line.")
        vn.train(
            documentation="COMMENT ON COLUMN address.address2 IS Secondary address line (optional).")
        vn.train(
            documentation="COMMENT ON COLUMN address.district IS District of the address.")
        vn.train(
            documentation="COMMENT ON COLUMN address.city_id IS Identifier for the city associated with the address.")
        vn.train(
            documentation="COMMENT ON COLUMN address.postal_code IS Postal code for the address.")
        vn.train(
            documentation="COMMENT ON COLUMN address.phone IS Phone number associated with the address.")
        vn.train(documentation="COMMENT ON COLUMN address.last_update IS Timestamp of the last update to the address record.")

        # Table: category
        vn.train(documentation="COMMENT ON TABLE category IS Stores film categories.")
        vn.train(
            documentation="COMMENT ON COLUMN category.category_id IS Unique identifier for each category.")
        vn.train(
            documentation="COMMENT ON COLUMN category.name IS Name of the film category.")
        vn.train(documentation="COMMENT ON COLUMN category.last_update IS Timestamp of the last update to the category record.")

        # Table: city
        vn.train(documentation="COMMENT ON TABLE city IS Stores city details.")
        vn.train(
            documentation="COMMENT ON COLUMN city.city_id IS Unique identifier for each city.")
        vn.train(documentation="COMMENT ON COLUMN city.city IS Name of the city.")
        vn.train(
            documentation="COMMENT ON COLUMN city.country_id IS Identifier for the country associated with the city.")
        vn.train(
            documentation="COMMENT ON COLUMN city.last_update IS Timestamp of the last update to the city record.")

        # Table: country
        vn.train(documentation="COMMENT ON TABLE country IS Stores country details.")
        vn.train(
            documentation="COMMENT ON COLUMN country.country_id IS Unique identifier for each country.")
        vn.train(
            documentation="COMMENT ON COLUMN country.country IS Name of the country.")
        vn.train(documentation="COMMENT ON COLUMN country.last_update IS Timestamp of the last update to the country record.")

        # Table: customer
        vn.train(
            documentation="COMMENT ON TABLE customer IS Stores customer information.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.customer_id IS Unique identifier for each customer.")
        vn.train(documentation="COMMENT ON COLUMN customer.store_id IS Identifier for the store associated with the customer.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.first_name IS First name of the customer.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.last_name IS Last name of the customer.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.email IS Email address of the customer.")
        vn.train(documentation="COMMENT ON COLUMN customer.address_id IS Identifier for the address associated with the customer.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.activebool IS Indicates if the customer is active.")
        vn.train(
            documentation="COMMENT ON COLUMN customer.create_date IS Date when the customer was created.")
        vn.train(documentation="COMMENT ON COLUMN customer.last_update IS Timestamp of the last update to the customer record.")
        vn.train(documentation="COMMENT ON COLUMN customer.active IS Active status of the customer represented as an integer.")

        # Table: film
        vn.train(documentation="COMMENT ON TABLE film IS Stores film details.")
        vn.train(
            documentation="COMMENT ON COLUMN film.film_id IS Unique identifier for each film.")
        vn.train(documentation="COMMENT ON COLUMN film.title IS Title of the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.description IS Description of the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.release_year IS Year the film was released.")
        vn.train(
            documentation="COMMENT ON COLUMN film.language_id IS Identifier for the language of the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.rental_duration IS Duration for which the film can be rented.")
        vn.train(
            documentation="COMMENT ON COLUMN film.rental_rate IS Rental rate for the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.length IS Length of the film in minutes.")
        vn.train(
            documentation="COMMENT ON COLUMN film.replacement_cost IS Cost to replace the film if lost or damaged.")
        vn.train(
            documentation="COMMENT ON COLUMN film.rating IS MPAA rating of the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.last_update IS Timestamp of the last update to the film record.")
        vn.train(
            documentation="COMMENT ON COLUMN film.special_features IS Special features available for the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film.fulltext IS Full-text search vector for the film.")

        # Table: film_actor
        vn.train(
            documentation="COMMENT ON TABLE film_actor IS Associates actors with films.")
        vn.train(
            documentation="COMMENT ON COLUMN film_actor.actor_id IS Identifier for the actor.")
        vn.train(
            documentation="COMMENT ON COLUMN film_actor.film_id IS Identifier for the film.")
        vn.train(documentation="COMMENT ON COLUMN film_actor.last_update IS Timestamp of the last update to the film-actor association.")

        # Table: film_category
        vn.train(
            documentation="COMMENT ON TABLE film_category IS Associates films with categories.")
        vn.train(
            documentation="COMMENT ON COLUMN film_category.film_id IS Identifier for the film.")
        vn.train(
            documentation="COMMENT ON COLUMN film_category.category_id IS Identifier for the category.")
        vn.train(documentation="COMMENT ON COLUMN film_category.last_update IS Timestamp of the last update to the film-category association.")

        # Table: inventory
        vn.train(
            documentation="COMMENT ON TABLE inventory IS Stores inventory details for films in stores.")
        vn.train(
            documentation="COMMENT ON COLUMN inventory.inventory_id IS Unique identifier for each inventory item.")
        vn.train(
            documentation="COMMENT ON COLUMN inventory.film_id IS Identifier for the film in inventory.")
        vn.train(documentation="COMMENT ON COLUMN inventory.store_id IS Identifier for the store where the film is available.")
        vn.train(documentation="COMMENT ON COLUMN inventory.last_update IS Timestamp of the last update to the inventory record.")

        # Table: language
        vn.train(
            documentation="COMMENT ON TABLE language IS Stores language details for films.")
        vn.train(
            documentation="COMMENT ON COLUMN language.language_id IS Unique identifier for each language.")
        vn.train(
            documentation="COMMENT ON COLUMN language.name IS Name of the language.")
        vn.train(documentation="COMMENT ON COLUMN language.last_update IS Timestamp of the last update to the language record.")

        # Table: payment
        vn.train(
            documentation="COMMENT ON TABLE payment IS Stores payment details for rentals.")
        vn.train(
            documentation="COMMENT ON COLUMN payment.payment_id IS Unique identifier for each payment.")
        vn.train(
            documentation="COMMENT ON COLUMN payment.customer_id IS Identifier for the customer making the payment.")
        vn.train(documentation="COMMENT ON COLUMN payment.staff_id IS Identifier for the staff member processing the payment.")
        vn.train(documentation="COMMENT ON COLUMN payment.rental_id IS Identifier for the rental associated with the payment.")
        vn.train(
            documentation="COMMENT ON COLUMN payment.amount IS Amount of the payment.")
        vn.train(
            documentation="COMMENT ON COLUMN payment.payment_date IS Date and time when the payment was made.")

        # Table: rental
        vn.train(
            documentation="COMMENT ON TABLE rental IS Stores rental transaction details.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.rental_id IS Unique identifier for each rental transaction.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.rental_date IS Date and time when the rental occurred.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.inventory_id IS Identifier for the inventory item being rented.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.customer_id IS Identifier for the customer renting the film.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.return_date IS Date and time when the film was returned.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.staff_id IS Identifier for the staff member processing the rental.")
        vn.train(
            documentation="COMMENT ON COLUMN rental.last_update IS Timestamp of the last update to the rental record.")

        # Table: staff
        vn.train(
            documentation="COMMENT ON TABLE staff IS Stores staff member details.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.staff_id IS Unique identifier for each staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.first_name IS First name of the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.last_name IS Last name of the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.address_id IS Identifier for the address of the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.email IS Email address of the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.store_id IS Identifier for the store where the staff member works.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.active IS Indicates if the staff member is active.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.username IS Username for the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.password IS Password for the staff member.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.last_update IS Timestamp of the last update to the staff record.")
        vn.train(
            documentation="COMMENT ON COLUMN staff.picture IS Picture of the staff member.")

        # Table: store
        vn.train(
            documentation="COMMENT ON TABLE store IS Stores details about stores.")
        vn.train(
            documentation="COMMENT ON COLUMN store.store_id IS Unique identifier for each store.")
        vn.train(documentation="COMMENT ON COLUMN store.manager_staff_id IS Identifier for the staff member managing the store.")
        vn.train(
            documentation="COMMENT ON COLUMN store.address_id IS Identifier for the address of the store.")
        vn.train(
            documentation="COMMENT ON COLUMN store.last_update IS Timestamp of the last update to the store record.")

        # additional docs
        vn.train(
            documentation="Rental duration is determined by the difference between return date and the rental date")


if __name__ == "__main__":
    doc_trainer = DocTrainer()
    doc_trainer.train()
