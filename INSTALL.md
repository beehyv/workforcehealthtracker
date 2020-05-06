# Installation Instructions
This project is built using REST framework. The technology stack is as follows:
* Python 3.6+
* Angular 8+
* Angular-Material
* Nodejs
* NPM/Yarn
* Django 1.11
* SQL Based Database (MySQL is preferred but any SQL DB can be used)
* Apache 2.4

The Project contains two modules:
* Backend
* Frontend

## Backend Installation and Setup
* Use `pipenv` or `virtualenv` for creating a new environment
* Prefered way is using `virtualenv`
* Run `virtualenv venv` to to create a virtual environment in your desired location
* Run the following command to activate the virtual environment.
    ```bash
    source <path-to-venv>/bin/activate
    ```
* Navigate to your backend project root
* Run the following command to install the dependencies
    ```bash
    pip3 install -r requirements.txt
    ```
* Once dependencies are installed open `<backend-project-root>/hcwtracker/settings.py` file in your favourite text editor
* Set the following values in the `settings.py` file
    ```python
    Debug = False
    ```  
    Setup SMTP server settings
    ```python
    EMAIL_HOST = ''
    EMAIL_PORT = 587
    EMAIL_HOST_USER = ''
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = True
    ```
    Database connection parameters
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': 3306,
        }
    }
    ```
    The frontend URL
    ```python
    FRONTEND_URL = ''
    ```
 * Run the following commands
     ```bash
    python3 manage.py syncdb
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```
 * Install `mod_wsgi` apache module
 * Open `httpd.conf` or its equivalent to create a virtualhost and restart Apache.
     ```bash
     <VirtualHost *:80>
            
            ServerName www.example.com
            ServerAdmin admin@admin.com
            DocumentRoot /<path-to-backend-root>
    
            ErrorLog ${APACHE_LOG_DIR}/error.log
            CustomLog ${APACHE_LOG_DIR}/access.log combined
            Alias /static /<path-to-backend-root>/static 
            <Directory /<path-to-backend-root>/hcwtracker>
                    <Files wsgi.py>
                            Require all granted
                    </Files>
            </Directory>
            <Directory /<path-to-backend-root>/static>
                    Require all granted
            </Directory>
            WSGIDaemonProcess www-data python-home=/<path-to-virtualenv-root> python-path=/<path-to-backend-root> processes=2 maximum-requests=100
            WSGIProcessGroup www-data
            WSGIScriptAlias / /<path-to-backend-root>/hcwtracker/wsgi.py process-group=www-data
            WSGIPassAuthorization On
    </VirtualHost>
    ```
## Frontend Setup

Frontend code is built using Angular 8. We use npm as the package manager of choice.
* Use `npm` or `yarn` for dependency management
* Our preferred package manager is `npm`
* Navigate to the `<frontend-root>`
* Run 
    ```bash
    npm install
    ```
* Navigate to and open `<frontend-root>/src/app/utils/UrlUtils.ts` using your favourite text editor
* Modify the following line in the file to point to the appropriate backend url.
    ```angular2
    const BASE_URL = '';
    ```
* Run the following code to package and build the frontend distribution
    ```bash
    npx ng build --prod
    ```
* Deploy the code available in `<frontend-path>/dist/HCW-Tracker` into your favourite webserver.


