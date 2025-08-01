from sqlalchemy import create_engine, Column, DateTime, func, Table, ForeignKey, VARCHAR, Integer, Text, BOOLEAN
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship

sqlite_database = "sqlite:///video_base.db"
engine = create_engine(sqlite_database, echo=True)

Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Categories(BaseModel):
    __tablename__ = 'categories'
    category = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(255), nullable=True)
    poster = Column(VARCHAR(255), nullable=True)
    library: Mapped[list['Library'] | None] = relationship(back_populates="category_name")


class Library(BaseModel):
    __tablename__ = 'library'
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category_name: Mapped["Categories"] = relationship(back_populates="library")
    category_path = Column(VARCHAR(255), nullable=True)


class Stars(BaseModel):
    __tablename__ = 'stars'
    first_name = Column(VARCHAR(255), nullable=True)
    last_name = Column(VARCHAR(255), nullable=True)
    bio = Column(VARCHAR(255), nullable=True)


class KPinfo(BaseModel):
    __tablename__ = 'kpinfo'
    kp_id = Column(Integer, nullable=False, unique=True)
    name = Column(VARCHAR(255), nullable=False)
    year = Column(Integer, nullable=True, unique=False)
    poster = Column(VARCHAR(255), nullable=True)
    describe = Column(Text, nullable=True)
    rate = Column(VARCHAR(255), nullable=True)
    video_files: Mapped[list['VideoFiles']] = relationship(back_populates="kpinfo")


class VideoFiles(BaseModel):
    __tablename__ = 'videofiles'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category = Column(VARCHAR(255), nullable=True)
    seasons: Mapped[list['Seasons'] | None] = relationship(back_populates="videofiles")
    file_path = Column(VARCHAR(255), nullable=False, unique=True)
    file_name = Column(VARCHAR(255), nullable=False)
    favorite = Column(BOOLEAN, unique=False, default=False)
    video_length = Column(Integer, nullable=True)
    last_position = Column(Integer, nullable=True)
    active = Column(BOOLEAN, unique=False, default=True)
    poster = Column(VARCHAR(255), nullable=True)
    kpinfo_id: Mapped[int | None] = mapped_column(ForeignKey("kpinfo.id"))
    kpinfo: Mapped[KPinfo | None] = relationship(back_populates="video_files")


class Seasons(BaseModel):
    __tablename__ = "seasons"
    id: Mapped[int] = mapped_column(primary_key=True)
    videofiles_id: Mapped[int] = mapped_column(ForeignKey("videofiles.id", ondelete='CASCADE'))
    videofiles: Mapped[VideoFiles] = relationship(back_populates="seasons")
    file_path = Column(VARCHAR(255), nullable=False, unique=True)
    file_name = Column(VARCHAR(255), nullable=False)
    favorite = Column(BOOLEAN, unique=False, default=False)
    active = Column(BOOLEAN, unique=False, default=True)
    series: Mapped[list['Series']] = relationship(cascade='save-update, merge, delete',
                                                  passive_deletes=True,)
    name = Column(VARCHAR(255), nullable=True)
    poster = Column(VARCHAR(255), nullable=True)


class Series(BaseModel):
    __tablename__ = "series"
    id: Mapped[int] = mapped_column(primary_key=True)
    seasons_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete='CASCADE'))
    file_path = Column(VARCHAR(255), nullable=False, unique=True)
    file_name = Column(VARCHAR(255), nullable=False)
    favorite = Column(BOOLEAN, unique=False, default=False)
    video_length = Column(Integer, nullable=True)
    last_position = Column(Integer, nullable=True)
    active = Column(BOOLEAN, unique=False, default=True)
    name = Column(VARCHAR(255), nullable=True)
    poster = Column(VARCHAR(255), nullable=True)


class BackupBd(BaseModel):
    __tablename__ = 'backup'
    file_path = Column(VARCHAR(255), nullable=False)
    file_name = Column(VARCHAR(255), nullable=True)


class Playlist(BaseModel):
    __tablename__ = 'playlist'
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_name = Column(VARCHAR(255), nullable=True)
    timeshift = Column(VARCHAR(255), nullable=True)
    catchup_days = Column(VARCHAR(255), nullable=True)
    catchup_type = Column(VARCHAR(255), nullable=True)
    tvg_id = Column(VARCHAR(255), nullable=False)
    group_title = Column(VARCHAR(255), nullable=False)
    tvg_logo = Column(VARCHAR(255), nullable=True)
    url = Column(VARCHAR(255), nullable=False)
    favorite = Column(BOOLEAN, unique=False, default=False)
    active = Column(BOOLEAN, unique=False, default=True)


class EpgProgrammes(BaseModel):
    __tablename__ = 'epg_programmes'
    id: Mapped[int] = mapped_column(primary_key=True)
    programme_start = Column(DateTime(timezone=True))
    programme_end = Column(DateTime(timezone=True))
    title = Column(VARCHAR(255))
    describe = Column(Text, nullable=True)
    tvg_id = Column(VARCHAR(255), nullable=False)


class Favorite(BaseModel):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_name = Column(VARCHAR(255), nullable=True)
    tvg_id = Column(VARCHAR(255), nullable=True)
    group = Column(VARCHAR(255), nullable=False)
    tvg_logo = Column(VARCHAR(255), nullable=True)


class Settings(BaseModel):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(primary_key=True)
    playlist_url = Column(VARCHAR(255), nullable=True)
    epg_url = Column(VARCHAR(255), nullable=True)


# Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)
# Seasons.__table__.drop(bind=engine)
# Playlist.__table__.create(bind=engine)
# Playlist.__table__.drop(bind=engine)
# Epg.__table__.drop(bind=engine)
# Favorite.__table__.create(bind=engine)
# KPinfo.__table__.drop(bind=engine)
# KPinfo.__table__.create(bind=engine)
# VideoFiles.__table__.drop(bind=engine)
# VideoFiles.__table__.create(bind=engine)
# BackupBd.__table__.drop(bind=engine)
# BackupBd.__table__.create(bind=engine)
# Seasons.__table__.drop(bind=engine)
# Seasons.__table__.create(bind=engine)
# Series.__table__.drop(bind=engine)
# Series.__table__.create(bind=engine)
# association_table_serials.drop(bind=engine)
# association_table_serials.create(bind=engine)
# Categories.__table__.drop(bind=engine)
# Categories.__table__.create(bind=engine)
# Library.__table__.drop(bind=engine)
# Library.__table__.create(bind=engine)
# EpgChannel.__table__.drop(bind=engine)
# Playlist.__table__.drop(bind=engine)
# Playlist.__table__.create(bind=engine)
# EpgProgrammes.__table__.drop(bind=engine)
# EpgProgrammes.__table__.create(bind=engine)
# Settings.__table__.drop(bind=engine)
# Settings.__table__.create(bind=engine)
