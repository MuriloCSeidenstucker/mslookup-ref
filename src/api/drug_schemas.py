from pydantic import BaseModel, ConfigDict, Field


class DrugAttributesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    registration_number: str = Field(
        ...,
        min_length=9,
        max_length=13,
        description="Número de registro oficial do medicamento na ANVISA",
        examples=["123456789"],
    )
    product_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nome comercial do produto",
        examples=["AMOXICILINA"],
    )
    active_ingredient: str | None = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Princípio ativo do medicamento",
        examples=["AMOXICILINA TRI-hIDRATADA"],
    )
    registration_holder: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Empresa detentora do registro na ANVISA",
        examples=["PRATI DONADUZZI & CIA LTDA"],
    )
    regulatory_category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Categoria regulatória do medicamento",
        examples=["Genérico"],
    )
    expiration_date: str | None = Field(
        ...,
        description="Data de validade do registro em formato ISO (AAAA-MM-DD)",
        examples=["2030-12-31"],
    )


class DrugResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    count: int = Field(..., description="Quantidade total de registros retornados")
    data: list[DrugAttributesSchema] = Field(
        ..., description="Lista contendo os medicamentos localizados"
    )


class DrugQuerySchema(BaseModel):
    product_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome comercial ou parte dele para busca por aproximação",
        examples=["AMOXICILINA"],
    )
    active_ingredient: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Filtro opcional por princípio ativo",
        examples=["AMOXICILINA TRI-hIDRATADA"],
    )
    registration_holder: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Filtro opcional pela empresa detentora do registro",
        examples=["PRATI DONADUZZI & CIA LTDA"],
    )
    regulatory_category: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Filtro opcional por categoria regulatória",
        examples=["Genérico"],
    )
