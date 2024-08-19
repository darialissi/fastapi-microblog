from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base

from typing import Set

from .vars import intpk, created_at, updated_at

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .posts import Post
    from .comments import Comment


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    posts: Mapped[Set['Post']] = relationship(back_populates='user') # 1 * n
    comments: Mapped[Set['Comment']] = relationship(back_populates='author') # 1 * n
