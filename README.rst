===============================
instant2fa
===============================

Instant2FA Python bindings.

Installation
------------

Install it via PyPI:

.. code-block:: shell

    pip install instant2fa

Usage
-----

.. code-block:: python

    import instant2fa

    instant2fa.access_key = 'YOUR_ACCESS_KEY'
    instant2fa.access_secret = 'YOUR_ACCESS_SECRET'

    distinct_id = 'A_UNIQUE_ID_FOR_A_USER'

    hosted_page_url = instant2fa.create_settings(distinct_id)
    hosted_page_url = instant2fa.create_verification(distinct_id)
    verification_succeeded = instant2fa.confirm_verification(distinct_id, token)

Development
-----------

To start development, run:

.. code-block:: shell

    $ git clone git@github.com:clef/instant2fa-python.git instant2fa
    $ cd instant2fa
    $ make develop
