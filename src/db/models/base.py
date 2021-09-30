import re

from sqlalchemy import Column, Integer, MetaData, TIMESTAMP
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.functions import func

camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')


def camel_to_snake_case(name):
    def _join(match):
        word = match.group()

        if len(word) > 1:
            return f'_{word[:-1]}_{word[-1]}'.lower()

        return f'_{word.lower()}'

    return camelcase_re.sub(_join, name).lstrip('_')


naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata = MetaData(naming_convention=naming_convention)


@as_declarative(metadata=metadata)
class Base:
    __name__: str

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
            server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
            server_default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)

