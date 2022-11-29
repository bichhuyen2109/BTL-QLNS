from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship,  backref
from QLNS import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(100), nullable=False)
    book = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


book_tag= db.Table('book_tag',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    inventory = Column(Integer,default=0)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='book_tag', lazy='subquery',
                        backref=backref('book', lazy=True))
    bill_details = relationship('BillDetails', backref='product', lazy=True)
    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User (BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    date = Column(DateTime)
    gender = Column(Boolean, default=True)
    phone = Column(String(10), nullable=True )
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    bill = relationship('Bill', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Bill(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('BillDetails', backref='bill', lazy=True)


class BillDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='Huyen', username='admin', password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1668919194/cld-sample-4.jpg')
        # db.session.add(u)
        # db.session.commit()
        #
        # password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        # u = User(name='Nhi', username='user', password=password,
        #          user_role=UserRole.USER,
        #          avatar='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1668919194/cld-sample-4.jpg')
        # db.session.add(u)
        # db.session.commit()

        # c1 = Category(name='Khoa học công nghệ')
        # c2 = Category(name='Nghệ thuật')
        # c3 = Category(name='Truyện')
        # c4 = Category(name='Tâm linh')
        # c5 = Category(name='Tâm lý')
        #
        # db.session.add_all([c1, c2, c3, c4, c5])
        # db.session.commit()

        # p1 = Book(name='LIFE 3.0',
        #             description='Nội dung chính của Life 3.0 bàn về Trí tuệ nhân tạo (Artificial Intelligence – AI) và những ảnh hưởng của nó tới đời sống con người.',
        #             author='Max Tegmark', price=161000, category_id=1,
        #             image='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1669474235/LIEF3.0_b8frkh.jpg')
        # p2 =Book(name='Doraemon',
        #             description='Đôrêmon là một chú mèo máy được Nôbitô, cháu ba đời của Nôbita gửi về quá khứ cho ông mình để giúp đỡ Nôbita tiến bộ, tức là cũng sẽ cải thiện hoàn cảnh của con cháu Nôbita sau này.',
        #             author='Fujiko F. Fujio', price=18000, category_id=3,
        #             image='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1669474236/DORAEMON_xksadg.jpg')
        # p3 = Book(name='ISMS-Hiểu Về Nghệ Thuật Hiện Đại',
        #             description='Cuốn sách này là một cẩm nang ngắn gọn giới thiệu cho bạn đọc về 55 trào lưu, trường phái và phong cách thịnh hành từ thời kỳ bình minh hé sáng của nghệ thuật hiện đại cuối thế kỷ 19 cho đến nay.',
        #             author='Sam Phillips', price=245000, category_id=2,
        #             image='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1669474237/isms_x7oy3w.jpg')
        # p4 = Book(name='Khám phá thế giới tâm linh',
        #             description='Bằng những trải nghiệm sống động từ chính cuộc đời mình, cùng với đầu óc khoa học cởi mở, tiếp thu cả những tinh hoa triết lý phương Đông và phương Tây, tác giả Gary Zukav muốn chia sẻ với mọi người những hiểu biết về thế giới nội tâm của con người qua một cách nhìn khác.',
        #             author='Gary Zukav', price=78000, category_id=4,
        #             image='https://res.cloudinary.com/dtoc5lqfe/image/upload/v1669477718/KPTGTamLinh_ygxrsn.webp')
        # db.session.add_all([p1, p2, p3, p4])
        # db.session.commit()