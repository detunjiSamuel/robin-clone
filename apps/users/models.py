from datetime import datetime
from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import FileStorage
from datetime import datetime

import os
import boto3

from db import db

class User(db.Model , UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    networth = db.Column(db.Float, default=0.00)
    image_url = db.Column(db.String, nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    assets = db.relationship("Asset",
                             back_populates="user",
                             cascade="all, delete-orphan")

    watchlists = db.relationship("WatchList",
                                 back_populates="user",
                                 cascade="all, delete-orphan")

    transactions = db.relationship(
        "Transaction", back_populates='user', cascade='all, delete-orphan')

    news = db.relationship("News", back_populates='user',
                           cascade='all, delete-orphan')

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            "networth": self.networth,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'joinedAt': self.created_at,
            'imageUrl': self.image_url
        }

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def upload_profile(self, file: FileStorage) -> str:
        filename = 'profile-image/' + self.email + \
            str(datetime.now()) + '.' + file.filename.split('.')[-1]

        s3 = boto3.client(
            's3',
            region_name=os.environ.get('S3_REGION'),
            aws_access_key_id=os.environ.get('S3_KEY'),
            aws_secret_access_key=os.environ.get('S3_SECRET')
        )

        s3.upload_fileobj(
            file,
            os.environ.get('S3_BUCKET'),
            filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        self.image_url = f"{os.environ.get('S3_LOCATION')}/{filename}"
        db.session.commit()

        return self.image_url

    def delete_profile(self):
        s3 = boto3.client(
            's3',
            region_name=os.environ.get('S3_REGION'),
            aws_access_key_id=os.environ.get('S3_KEY'),
            aws_secret_access_key=os.environ.get('S3_SECRET')
        )

        s3.delete_object(
            Bucket=os.environ.get('S3_BUCKET'),
            Key=self.image_url.split('amazonaws.com/')[1]
        )

        self.image_url = None
        db.session.commit()


class Asset(db.Model):
    __tablename__ = "assets"

    __table_args__ = (
        db.UniqueConstraint("user_id", "symbol"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    avg_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="assets")

    def json(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "quantity": self.quantity,
            "avgPrice": self.avg_price
        }
    

class Transaction(db.Model):
    __tablename__ = 'transactions'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    # sell or buy
    transaction_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates='transactions')