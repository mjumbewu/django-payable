django-payable
==============

Getting Started
---------------

0. Clone this repo.
1. Edit *src/templates/invoice.html*.
2. Set `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` in your environment. You can find your keys at https://dashboard.stripe.com/account/apikeys. If you're developing locally, you can just create a *.env* file in the root folder. This file should have key-value pairs on different lines, e.g. `STRIPE_PUBLIC_KEY=pk_test_1234567890`. You should probably set `DEBUG=True` while developing locally as well.
3. Set up the database with `src/manage.py migrate`.
4. Create an admin user with `src/manage.py createsuperuser`.
