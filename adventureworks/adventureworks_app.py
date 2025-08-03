from adventureworks.common import EnvironmentLoader, MyVanna
from vanna.flask import VannaFlaskApp


class AdventureWorksApp:
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
            logo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpCI3pneonjeQ-Qd20sXcRNcnATzu5nWorORswRsQuGupMqywTVScfzOLfasYNNATG5tI&usqp=CAU",
            title='Welcome to Order Analyzer',
            subtitle='Your AI-powered agent for answering questions on your orders.',
        )

    def run(self):
        self.app.run(host='0.0.0.0', port=8086, debug=True)


if __name__ == "__main__":
    app = AdventureWorksApp()
    app.run()
