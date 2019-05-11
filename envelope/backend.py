import functools
from typing import Callable, Any

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from envelope.config import Config

config = Config()

engine = create_engine(f"sqlite:///{config.database_path}", echo=config.debug_mode)
session = scoped_session(sessionmaker(autocommit=False, bind=engine))


class Base(object):
    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    def _flush(self):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


BaseModel = declarative_base(cls=Base)
BaseModel.query = session.query_property()


def commit(func: Callable) -> Any:  # type: ignore
    @functools.wraps(func)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
        result = func(self, *args, **kwargs)
        session.commit()
        return result

    return wrapper
