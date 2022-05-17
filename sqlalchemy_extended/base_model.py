from datetime import date, datetime
from typing import Any, Dict, Iterable


class BaseModel:
    """
    This is an alternative Base class which you can use to extend from.

    If you use the declarative_base tool from SQLAlchemy, simply do the following:

    .. code-block:: python

        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy_extended import BaseModel

        class MyBase(BaseModel)
            pass

        declarative_base(cls=MyBase)
    """

    @staticmethod
    def ensure_serializable(value: Any) -> Any:
        if type(value) in (date, datetime):
            return value.isoformat()
        return value

    def __repr__(self) -> str:
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def __eq__(self, other):
        return all(
            [
                getattr(self, col) == getattr(other, col)
                for col in self.columns()
                if getattr(self, col) is not None and getattr(other, col) is not None
            ]
        )

    def columns(self) -> Iterable[str]:
        return (c.name for c in self.__table__.columns)

    def dto(self) -> Dict[Any, Any]:
        dto_dict = {
            k: self.ensure_serializable(getattr(self, k)) for k in self.safe_columns()
        }
        return dict(dto_dict)

    def safe_columns(self) -> Iterable[str]:
        columns = self.columns()
        if not hasattr(self, "__restricted_columns__"):
            return columns
        return tuple(set(columns) - set(self.__restricted_columns__))

    def update(self, **kwargs: Dict[str, str]) -> None:
        """
        Given a list of keword arguments, update the model.

        Skips the id column.
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
        if hasattr(self, "updated_at"):
            setattr(self, "updated_at", datetime.utcnow())
