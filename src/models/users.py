from typing import TYPE_CHECKING, Set

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base

from .vars import created_at, intpk, updated_at

if TYPE_CHECKING:
    from .comments import Comment
    from .posts import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    posts: Mapped[Set["Post"]] = relationship(back_populates="user")  # 1 * n
    comments: Mapped[Set["Comment"]] = relationship(back_populates="author")  # 1 * n
