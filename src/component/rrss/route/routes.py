# Copyright (C) 2025 Francisco Bartolo (See LICENCE)

"""Home routes module."""

from flask import Response, request
from app.extensions import cache, require_header_set_redirect # pylint: disable=import-error
from .dispatcher_rrss import DispatcherRrss
from . import rrss_bp


@rrss_bp.route('/', defaults={'route': 'rrss'}, methods=['GET'])
def rrss(route) -> Response:
    """Route handler for the home page."""
    dispatch = DispatcherRrss(request, route)
    dispatch.schema_data['dispatch_result'] = True
    return dispatch.view.render()


@rrss_bp.route('/ajax', defaults={'route': 'rrss/ajax'}, methods=['GET'])
@require_header_set_redirect('Requested-With-Ajax', "rrss.rrss")
@cache.cached(timeout=120)
def rrss_ajax(route) -> Response:
    """Route handler for the home page."""
    dispatch = DispatcherRrss(request, route)
    dispatch.schema_data['dispatch_result'] = dispatch.get_rss()
    dispatch.view.response.headers['Cache-Control'] = "max-age=60"
    return dispatch.view.render()


@rrss_bp.route('/ajax/<name_rss>', defaults={'route': 'rrss/ajax'}, methods=['GET'])
@require_header_set_redirect('Requested-With-Ajax', "rrss.rrss")
@cache.cached(timeout=120)
def rrss_ajax_name(route, name_rss) -> Response:
    """Route handler for the home page."""
    dispatch = DispatcherRrss(request, route)
    dispatch.schema_data['dispatch_result'] = dispatch.get_rss(name_rss)
    dispatch.view.response.headers['Cache-Control'] = "max-age=60"
    return dispatch.view.render()
