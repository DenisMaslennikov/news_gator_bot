from typing import Type, Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.base import Base


def get_or_create(session: Session, model: Type[Base], **kwargs) -> Tuple[Base, bool]:
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True

