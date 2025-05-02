# pylint: disable=R0913:too-many-arguments, R0903:too-few-public-methods


class HttpRequest:
    """Representa uma requisição HTTP na camada de apresentação.

    Esta classe modela os componentes de uma requisição HTTP, incluindo cabeçalhos,
    corpo, parâmetros de consulta, parâmetros de caminho, URL e endereço IPv4. É utilizada
    na camada de apresentação para estruturar os dados recebidos em solicitações HTTP.

    Args:
        headers (dict, optional): Dicionário contendo os cabeçalhos da requisição. Defaults to None.
        body (dict, optional): Dicionário contendo o corpo da requisição. Defaults to None.
        query_params (dict, optional): Dicionário contendo os parâmetros de consulta (query string).
            Defaults to None.
        path_params (dict, optional): Dicionário contendo os parâmetros extraídos do caminho da URL.
            Defaults to None.
        url (str, optional): URL completa da requisição. Defaults to None.
        ipv4 (str, optional): Endereço IPv4 do cliente que fez a requisição. Defaults to None.

    Attributes:
        headers (dict): Dicionário com os cabeçalhos da requisição.
        body (dict): Dicionário com o corpo da requisição.
        query_params (dict): Dicionário com os parâmetros de consulta.
        path_params (dict): Dicionário com os parâmetros de caminho.
        url (str): URL da requisição.
        ipv4 (str): Endereço IPv4 do cliente.
    """

    def __init__(
        self,
        *,
        headers=None,
        body=None,
        query_params=None,
        path_params=None,
        url=None,
        ipv4=None,
    ) -> None:
        self.headers = headers
        self.body = body
        self.query_params = query_params
        self.path_params = path_params
        self.url = url
        self.ipv4 = ipv4
