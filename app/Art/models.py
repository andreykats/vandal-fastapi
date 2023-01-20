from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db_sql import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    base_layer_id = Column(Integer, index=True)
    is_active = Column(Boolean, default=False)
    height = Column(Integer)
    width = Column(Integer)

    owner = relationship("User", back_populates="items")
