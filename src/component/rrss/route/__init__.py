# Copyright (C) 2025 Francisco Bartolo (See LICENCE)

"""Read RSS Blueprint Module."""

import os
from flask import Blueprint
from utils.utils import load_blueprint_schema # pylint: disable=import-error

rrss_bp = Blueprint('rrss', __name__, url_prefix='/rrss')
this_dir = os.path.dirname(os.path.abspath(__file__))
rrss_bp.template_route = os.path.join(this_dir, "..", "neutral", "route")
load_blueprint_schema(rrss_bp)

from . import routes  # pylint: disable=C0413  # noqa: F401
