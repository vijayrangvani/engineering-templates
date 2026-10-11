"""PRACTICE: SQLAlchemy engine + session per request.
Reference answer: ../../../fastapi-app/app/db.py

Shape:
  1. connect_args: check_same_thread=False ONLY for sqlite
  2. engine = create_engine(url, connect_args, pool_pre_ping=True, echo=debug)
  3. SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
  4. class Base(DeclarativeBase)
  5. get_db(): open session -> yield -> commit | except: rollback + raise | finally: close
  6. DbSession = Annotated[Session, Depends(get_db)]
"""
# TODO
