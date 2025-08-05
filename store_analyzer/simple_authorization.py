import logging
import flask

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleAuthorization:
    def __init__(self, env_vars: dict, vn: any = None, users: dict = None,):
        self.users = users if users is not None else {}
        self.vn = vn
        self.env_vars = env_vars

    def get_user(self, flask_request) -> any:
        return flask_request.cookies.get('user')

    def is_logged_in(self, user: any) -> bool:
        return user is not None and user != ""

    def override_config_for_user(self, user: any, config: dict) -> dict:
        password = flask.request.cookies.get('password')
        config.update({"postgres_username": user,
                      "postgres_password": password})

        return config

    def login_form(self) -> str:
        return '''
            <div class="p-4 sm:p-7">
            <div class="text-center">
                <h1 class="block text-2xl font-bold
                        text-gray-800 dark:text-white">
                    Sign in
                </h1>
            </div>
            <div class="mt-5">
            <form action="/auth/login" method="POST">
            <div class="grid gap-y-4">
                <div>
                <label for="user" class="block text-sm mb-2 dark:text-white">
                    Username
                </label>
                <input type="text" id="user" name="user"
                    class="py-3 px-4 block w-full border border-gray-200
                            rounded-lg text-sm" required>
                </div>
                <div>
                <label for="password"
                        class="block text-sm mb-2 dark:text-white">
                    Password
                </label>
                <input type="password" id="password" name="password"
                    class="py-3 px-4 block w-full border border-gray-200
                        rounded-lg text-sm" required>
                </div>
                <button type="submit" class="w-full py-3 px-4 inline-flex
                    justify-center items-center gap-x-2 text-sm
                    font-semibold rounded-lg border border-transparent
                    bg-blue-600 text-white hover:bg-blue-700">
                    Sign in
                </button>
            </div>
            </form>
            </div>
            </div>
        '''

    def login_handler(self, flask_request) -> str:
        user = flask_request.form['user']
        password = flask_request.form['password']
        response = flask.redirect('/')
        response.set_cookie('user', user)
        response.set_cookie('password', password)
        logger.info(f"User: {user}, Password: {password}")
        for stored_user in self.users:
            logger.info(f"Checking user: {stored_user['user']} and \
                        password: {stored_user['password']}")
            if (
                stored_user["user"].lower() == user.lower()
                and stored_user["password"] == password
            ):
                logger.info(f"User {user} authenticated successfully.")
                response = flask.make_response('Logged in as ' + user)
                response.set_cookie('user', user)
                # Redirect to the main page
                response.headers['Location'] = '/'
                response.status_code = 302
                self.vn.connect_to_postgres(
                    host=self.env_vars["db_host"],
                    dbname=self.env_vars["db_name"],
                    user=user,
                    password=password,
                    port=self.env_vars["db_port"],
                )
                return response

        logger.error(f"Login failed for user: {user}")
        return flask.make_response(
            'Login failed. Please check your username and password.',
            401,
            {'Content-Type': 'text/plain'}
        )

    def callback_handler(self, flask_request) -> str:
        user = flask_request.args['user']
        response = flask.make_response('Logged in as ' + user)
        response.set_cookie('user', user)
        return response

    def logout_handler(self, flask_request) -> str:
        response = flask.make_response('')
        response.delete_cookie('user')
        response.delete_cookie('password')
        # Redirect to main page so the sign-in form appears
        response.headers['Location'] = '/'
        response.status_code = 302
        return response
