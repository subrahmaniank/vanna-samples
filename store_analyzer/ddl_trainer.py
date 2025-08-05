from store_analyzer.base_trainer import BaseTrainer


class DDLTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.vn = self.get_vn()

    def train(self):
        vn = self.vn

        vn.train(ddl='CREATE TABLE actor ( \
            actor_id serial4 PRIMARY KEY, \
            first_name varchar NOT NULL, \
            last_name varchar NOT NULL, \
            last_update timestamp NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE address ( \
            address_id serial4 PRIMARY KEY, \
            address varchar NOT NULL, \
            address2 varchar, \
            district varchar NOT NULL, \
            city_id int2 NOT NULL, \
            postal_code varchar, \
            phone varchar, \
            last_update timestamp NOT NULL, \
            FOREIGN KEY (city_id) REFERENCES city(city_id) \
        );')

        vn.train(ddl='CREATE TABLE category ( \
            category_id serial4 PRIMARY KEY, \
            name varchar NOT NULL, \
            last_update timestamp NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE city ( \
            city_id serial4 PRIMARY KEY, \
            city varchar NOT NULL, \
            country_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            FOREIGN KEY (country_id) REFERENCES country(country_id) \
        );')

        vn.train(ddl='CREATE TABLE country ( \
            country_id serial4 PRIMARY KEY, \
            country varchar NOT NULL, \
            last_update timestamp NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE customer ( \
            customer_id serial4 PRIMARY KEY, \
        );')

        vn.train(ddl='CREATE TABLE country ( \
            country_id serial4 PRIMARY KEY, \
            country varchar NOT NULL, \
            last_update timestamp NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE customer ( \
            customer_id serial4 PRIMARY KEY, \
            store_id int2 NOT NULL, \
            first_name varchar NOT NULL, \
            last_name varchar NOT NULL, \
            email varchar, \
            address_id int2 NOT NULL, \
            activebool bool NOT NULL, \
            create_date date NOT NULL, \
            last_update timestamp NOT NULL, \
            active int4 NOT NULL, \
            FOREIGN KEY (store_id) REFERENCES store(store_id), \
            FOREIGN KEY (address_id) REFERENCES address(address_id) \
        ); ')

        vn.train(ddl='CREATE TABLE film ( \
            film_id serial4 PRIMARY KEY, \
            title varchar NOT NULL, \
            description text, \
            release_year year NOT NULL, \
            language_id int2 NOT NULL, \
            rental_duration int2 NOT NULL, \
            rental_rate numeric NOT NULL, \
            length int2 NOT NULL, \
            replacement_cost numeric NOT NULL, \
            rating mpaa_rating NOT NULL, \
            last_update timestamp NOT NULL, \
            special_features _text, \
            fulltext tsvector \
        );')

        vn.train(ddl='CREATE TABLE film_actor ( \
            actor_id int2 NOT NULL, \
            film_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            PRIMARY KEY (actor_id, film_id), \
            FOREIGN KEY (actor_id) REFERENCES actor(actor_id), \
            FOREIGN KEY (film_id) REFERENCES film(film_id) \
        );')

        vn.train(ddl='CREATE TABLE film_category ( \
            film_id int2 NOT NULL, \
            category_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            PRIMARY KEY (film_id, category_id), \
            FOREIGN KEY (film_id) REFERENCES film(film_id), \
            FOREIGN KEY (category_id) REFERENCES category(category_id) \
        );')

        vn.train(ddl='CREATE TABLE inventory ( \
            inventory_id serial4 PRIMARY KEY, \
            film_id int2 NOT NULL, \
            store_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            FOREIGN KEY (film_id) REFERENCES film(film_id), \
            FOREIGN KEY (store_id) REFERENCES store(store_id) \
        );')

        vn.train(ddl='CREATE TABLE "language" ( \
            language_id serial4 PRIMARY KEY, \
            name bpchar NOT NULL, \
            last_update timestamp NOT NULL \
        );')

        vn.train(ddl='CREATE TABLE payment ( \
            payment_id serial4 PRIMARY KEY, \
            customer_id int2 NOT NULL, \
            staff_id int2 NOT NULL, \
            rental_id int4, \
            amount numeric NOT NULL, \
            payment_date timestamp NOT NULL, \
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id), \
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id), \
            FOREIGN KEY (rental_id) REFERENCES rental(rental_id) \
        );')

        vn.train(ddl='CREATE TABLE rental ( \
            rental_id serial4 PRIMARY KEY, \
            rental_date timestamp NOT NULL, \
            inventory_id int4 NOT NULL, \
            customer_id int2 NOT NULL, \
            return_date timestamp, \
            staff_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id), \
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id), \
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id) \
        );')

        vn.train(ddl='CREATE TABLE staff ( \
            staff_id serial4 PRIMARY KEY, \
            first_name varchar NOT NULL, \
            last_name varchar NOT NULL, \
            address_id int2 NOT NULL, \
            email varchar, \
            store_id int2 NOT NULL, \
            active bool NOT NULL, \
            username varchar NOT NULL, \
            password varchar NOT NULL, \
            last_update timestamp NOT NULL, \
            picture bytea, \
            FOREIGN KEY (address_id) REFERENCES address(address_id), \
            FOREIGN KEY (store_id) REFERENCES store(store_id) \
        ); ')

        vn.train(ddl='CREATE TABLE store ( \
            store_id serial4 PRIMARY KEY, \
            manager_staff_id int2 NOT NULL, \
            address_id int2 NOT NULL, \
            last_update timestamp NOT NULL, \
            FOREIGN KEY (manager_staff_id) REFERENCES staff(staff_id), \
            FOREIGN KEY (address_id) REFERENCES address(address_id) \
        );')

        vn.train(ddl='CREATE VIEW actor_info AS \
        SELECT actor_id, first_name, last_name, film_info \
        FROM actor; ')

        vn.train(ddl='CREATE VIEW customer_list AS \
        SELECT id, name, address, zip code, phone, city, country, notes, sid \
        FROM customer; ')

        vn.train(ddl='CREATE VIEW film_list AS \
        SELECT fid, title, description, category, price, length, \
              rating, actors \
        FROM film;')

        vn.train(ddl='CREATE VIEW nicer_but_slower_film_list AS \
        SELECT fid, title, description, category, price, length, \
                 rating, actors \
        FROM film; ')

        vn.train(ddl='CREATE VIEW sales_by_film_category AS \
        SELECT category, total_sales \
        FROM film_category; ')

        vn.train(ddl='CREATE VIEW sales_by_store AS \
        SELECT store, manager, total_sales \
        FROM store;')

        vn.train(ddl='CREATE VIEW staff_list AS \
        SELECT id, name, address, zip code, phone, city, country, sid \
        FROM staff;')


if __name__ == "__main__":
    ddl_trainer = DDLTrainer()
    ddl_trainer.train()
