from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base

from .vars import created_at, intpk, updated_at

if TYPE_CHECKING:
    from .posts import Post
    from .users import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[intpk]
    body: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
