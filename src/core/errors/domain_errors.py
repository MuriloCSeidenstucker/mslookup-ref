class DomainError(Exception):
    """Classe base para todos os erros de domínio da aplicação."""


class DrugNotFoundError(DomainError):
    """Exceção lançada quando um medicamento solicitado não é encontrado."""


class InvalidFilterError(DomainError):
    """Exceção lançada quando filtros fornecidos para busca são inválidos."""
