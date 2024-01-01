from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Foo(Base):
    __tablename__ = "foo"

    id: Mapped[int] = mapped_column(primary_key=True)
    a: Mapped[int]
    b: Mapped[int]


func.row_number().over(order_by=Foo.a, partition_by=Foo.b.desc())
func.row_number().over(order_by=[Foo.a.desc(), Foo.b.desc()])
func.row_number().over(partition_by=[Foo.a.desc(), Foo.b.desc()])
func.row_number().over(order_by="a", partition_by=("a", "b"))
func.row_number().over(partition_by="a", order_by=("a", "b"))


# EXPECTED_TYPE: Function[Any]
reveal_type(func.row_number().filter())
# EXPECTED_TYPE: FunctionFilter[Any]
reveal_type(func.row_number().filter(Foo.a > 0))


# test #10801
# EXPECTED_TYPE: max[int]
reveal_type(func.max(Foo.b))


stmt1 = select(
    Foo.a,
    func.min(Foo.b),
).group_by(Foo.a)
# EXPECTED_TYPE: Select[Tuple[int, int]]
reveal_type(stmt1)
