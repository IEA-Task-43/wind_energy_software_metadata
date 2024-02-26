"""Module for the top-level wind energy software metadata model.

"""

import datetime
from typing import Literal

import pydantic as pdt


class Author(pdt.BaseModel):
    """Details of an author, also known as creator."""

    name: str
    orcid: str
    affiliation: str


class Distribution(pdt.BaseModel):
    """Details of a software distribution."""

    distribution_platform: str
    url: str

class WindEnergySoftwareMetadataDocument(pdt.BaseModel):
    """Metadata document for a piece of wind energy software."""

    id: str
    name: str
    description: str
    latest_release_version: str
    latest_release_date: datetime.date

    license: str
    source_access_right: Literal["open", "closed"]

    authors: list[Author]

    programming_languages: list[str]
    supported_platforms: list[str]

    resource_type: Literal["software"] = "software"
    resource_subtype: Literal["model", "analysis", "optimisation"]

    repository_url: str
    documentation_url: str

    distributions: list[Distribution]

    function: str  # The purpose for the software to exist

    time_domain: Literal["steady", "dynamic"]

    representation_level: Literal["wind_farm", "turbine"]
    turbine_representation: Literal["actuator", "bem", "vortex_method", "geometry_resolved"] | None
    location: Literal["onshore", "offshore"] | None

    input_description: str
    output_description: str
