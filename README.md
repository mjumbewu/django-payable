django-payable
==============

Getting Started
---------------

0. Clone this repo.
1. Set `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` in your environment. You can find your keys at https://dashboard.stripe.com/account/apikeys. If you're developing locally, you can create an *.env* file in the root folder. This file should have key-value pairs on different lines, e.g. `STRIPE_PUBLIC_KEY=pk_test_1234567890`. You should probably set `DEBUG=True` while developing locally as well.
2. Set up the database with `src/manage.py migrate`.
3. Create an admin user with `src/manage.py createsuperuser`.
4. Start the server with `src/manage.py runserver`.
5. Create your first invoice at http://localhost:8000/admin/payable/invoice/add/.
6. Edit *src/templates/invoice.html* and *src/static/styles/invoice.css* until your invoice looks acceptable.
7. Deploy your app to Heroku or your favorite hosting platform.
