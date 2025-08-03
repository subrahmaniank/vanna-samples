from store_analyzer import EnvironmentLoader, MyVanna
from vanna.flask import VannaFlaskApp

class StoreAnalyzerApp:
    def __init__(self):
        self.env_vars = EnvironmentLoader.load_environment_variables()
        self._initialize_vanna()
        self._initialize_flask_app()

    def _initialize_vanna(self):
        self.vn = MyVanna.create_instance(self.env_vars)
        self.vn.connect_to_postgres(
            host=self.env_vars["db_host"],
            dbname=self.env_vars["db_name"],
            user=self.env_vars["db_username"],
            password=self.env_vars["db_password"],
            port=self.env_vars["db_port"],
        )

    def _initialize_flask_app(self):
        self.app = VannaFlaskApp(
            self.vn,
            allow_llm_to_see_data=True,
            logo="https://logodix.com/logo/1132951.jpg",
            title='Welcome to DVD Rental Store',
            subtitle='Your AI-powered agent for answering questions on DVD rentals.',
        )

    def run(self):
        self.app.run(host='0.0.0.0', port=8084, debug=True)


if __name__ == "__main__":
    app = StoreAnalyzerApp()
    app.run()