from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.db import Base

from typing import Set

from .vars import intpk, created_at, updated_at
from .comments import Comment
from .categories import Category

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[Category]
    body: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[Set['Comment']] = relationship(back_populates='post') # 1 * n