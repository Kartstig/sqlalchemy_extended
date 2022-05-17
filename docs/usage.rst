=====
Usage
=====

If you use the declarative_base tool from SQLAlchemy, simply do the following:

.. code-block:: python

    import BaseModel

    class MyBase(BaseModel):
        pass

    declarative_base(cls=MyBase)
