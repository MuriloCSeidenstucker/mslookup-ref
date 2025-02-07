# pylint: disable=C0209:consider-using-f-string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    """Gerencia a conexão com o banco de dados utilizando SQLAlchemy."""

    def __init__(self) -> None:
        self.__connection_string = "{}://{}:{}@{}:{}/{}".format(
            "mysql+pymysql", "root", "root", "localhost", "3306", "ms_database"
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        """Cria e retorna um objeto de engine do SQLAlchemy.

        Returns:
            sqlalchemy.engine.Engine: Instância da engine de conexão com o banco de dados.
        """
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        """Retorna a engine do banco de dados.

        Returns:
            sqlalchemy.engine.Engine: Instância da engine de conexão com o banco de dados.
        """
        return self.__engine

    def __enter__(self):
        """Inicia uma sessão no banco de dados.

        Returns:
            DBConnectionHandler: Retorna a própria instância com a sessão ativa.
        """
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a sessão do banco de dados ao sair do contexto.

        Args:
            exc_type (Exception, optional): Tipo da exceção, se houver.
            exc_val (Exception, optional): Valor da exceção, se houver.
            exc_tb (traceback, optional): Traceback da exceção, se houver.
        """
        self.session.close()
