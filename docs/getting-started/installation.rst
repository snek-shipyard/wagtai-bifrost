Installation
============

Add library to an existing Wagtail project:

``pip install wagtail_bifrost``

Add the following to the ``installed_apps`` list in your wagtail
settings file:

::

   installed_apps = [
       ...
       "bifrost",
       "graphene_django",
       ...
   ]

For GraphQL Subscriptions with Django Channels, run ``pip install wagtail_bifrost[channels]`` and add
``channels`` to installed apps:

::

   installed_apps = [
       ...
       "bifrost",
       "graphene_django",
       "channels",
       ...
   ]

Add the following to the bottom of the same settings file where each key
is the app you want to this library to scan and the value is the prefix
you want to give to GraphQL types (you can usually leave this blank):

::

   # Bifrost Config:
   GRAPHENE = {"SCHEMA": "bifrost.schema.schema"}
   BIFROST_APPS = {
       "home": ""
   }

Add the GraphQL urls to your ``urls.py``:

::

   from bifrost import urls as bifrost_urls
   ...
   urlpatterns = [
       ...
       url(r"", include(bifrost_urls)),
       ...
   ]

Done! Now you can proceed onto configuring your models to generate
GraphQL types that adopt their structure.

By default, all field and argument names will be converted from `snake_case`
to `camelCase`. To disable this behavior, set the `BIFROST_AUTO_CAMELCASE`
setting to `False` on your project settings.

* **Next Steps**

  * :doc:`examples`
  * :doc:`../general-usage/graphql-types`


*Your GraphQL endpoint is available at http://localhost:8000/graphql/*
