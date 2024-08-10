from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.db import Base

from .vars import intpk, created_at, updated_at
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .posts import Posts
    from .users import Users


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[intpk]
    body: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'))
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    post: Mapped['Posts'] = relationship(back_populates='comments')
    author: Mapped['Users'] = relationship(back_populates='comments')