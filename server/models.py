import datetime

from sqlalchemy_serializer import SerializerMixin

from .globals import globals as g


class AIProject(g.db.Model, SerializerMixin):
    __tablename__ = 'ai_project'
    id = g.db.Column(g.db.Integer, primary_key=True)
    name = g.db.Column(g.db.String, unique=True, nullable=False)
    model_dir = g.db.Column(g.db.String)
    description = g.db.Column(g.db.String)
    project_price = g.db.Column(g.db.Integer)
    price_per_nft = g.db.Column(g.db.Integer)
    no_of_ainfts = g.db.Column(g.db.Integer)
    status = g.db.Column(g.db.String)
    account = g.db.Column(g.db.String)
    logo = g.db.Column(g.db.String)
    banner = g.db.Column(g.db.String)
    created_date = g.db.Column(g.db.DateTime, default=datetime.datetime.utcnow)


class SmartContract(g.db.Model, SerializerMixin):
    __tablename__ = "smart_contract"
    id = g.db.Column(g.db.Integer, primary_key=True)
    address = g.db.Column(g.db.String, nullable=False)
    chain = g.db.Column(g.db.String, nullable=False)
    projectId = g.db.Column(g.db.Integer, nullable=False)
    compiledContractPath = g.db.Column(g.db.String, nullable=False)
    created_date = g.db.Column(g.db.DateTime, default=datetime.datetime.utcnow)


class AINFT(g.db.Model, SerializerMixin):
    __tablename__ = 'ai_nft'
    id = g.db.Column(g.db.Integer, primary_key=True)
    projectId = g.db.Column(g.db.Integer, nullable=False)
    fileName = g.db.Column(g.db.String, unique=True, nullable=False)
    dataCid = g.db.Column(g.db.String, nullable=True)
    metadataCid = g.db.Column(g.db.String, nullable=True)
    format = g.db.Column(g.db.String, nullable=True)
    tokenId = g.db.Column(g.db.String, nullable=True)
    status = g.db.Column(g.db.String, default="pending")
    created_date = g.db.Column(g.db.DateTime, default=datetime.datetime.utcnow)


class UserDetails(g.db.Model, SerializerMixin):
    __tablename__ = 'user_details'
    id = g.db.Column(g.db.Integer, primary_key=True)
    username = g.db.Column(g.db.String, default="User")
    address = g.db.Column(g.db.String, nullable=False)
    profilePicture = g.db.Column(g.db.String, nullable=True)
    banner = g.db.Column(g.db.String, nullable=True)
    created_date = g.db.Column(g.db.DateTime, default=datetime.datetime.utcnow)
