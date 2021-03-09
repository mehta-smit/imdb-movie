"""
Database Models & Configurations
"""

from sqlalchemy import create_engine, event
from sqlalchemy import exc, select
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI


def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False
    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result


class DbSession:
    def __init__(self, **kwargs):
        self.database_url = kwargs.pop("database_url")
        self.pool_pre_ping = kwargs.pop("pool_pre_ping", False)
        self.is_read_session = kwargs.pop("is_read_session", False)
        self.kwargs = kwargs
        self.kwargs['pool_recycle'] = kwargs.get("pool_recycle", 3600)
        self.factory, self.session = None, None

    def get_session(self):
        if self.session:
            return self.session

        factory = self.get_session_factory()
        self.session = factory()
        return self.session

    def get_session_factory(self):
        if self.factory:
            return self.factory

        db_engine = create_engine(self.database_url, **self.kwargs)

        if self.pool_pre_ping:
            event.listen(db_engine, "engine_connect", ping_connection)
        db_session_factory = sessionmaker(
            bind=db_engine, autocommit=self.is_read_session)
        self.factory = db_session_factory

        return self.factory


db_session_obj = None


def _get_db_session_obj(url):
    global db_session_obj
    db_session_obj = DbSession(database_url=url, pool_recycle=3600, pool_pre_ping=True, pool_size=20)
    return db_session_obj


def get_imdb_session(url):
    session_imdb_obj = _get_db_session_obj(url)
    global session
    session = scoped_session(session_imdb_obj.get_session_factory())
    return session


# imdb database sessions
session = get_imdb_session(SQLALCHEMY_DATABASE_URI)


def close_session(response_or_exc):
    session.remove()
    return response_or_exc
