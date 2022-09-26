# Copyright (c) 2001-2022, Hove and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Hove (www.hove.com).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# channel `#navitia` on riot https://riot.im/app/#/room/#navitia:matrix.org
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division

import pybreaker
import string
import logging
from jormungandr.external_services.external_service import AbstractExternalService
from jormungandr import utils
import gevent
import gevent.pool
from jormungandr import cache, app
from jormungandr.interfaces.v1.serializer.pt import VehicleJourneyPositionsSerializer
from navitiacommon import type_pb2


class VehiclePosition(AbstractExternalService):
    def __init__(self, service_url, timeout=2, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.service_url = service_url
        self.timeout = timeout
        self.breaker = pybreaker.CircuitBreaker(
            fail_max=kwargs.get('circuit_breaker_max_fail', app.config['CIRCUIT_BREAKER_MAX_FORSETI_FAIL']),
            reset_timeout=kwargs.get(
                'circuit_breaker_reset_timeout', app.config['CIRCUIT_BREAKER_FORSETI_TIMEOUT_S']
            ),
        )

    @cache.memoize(app.config.get(str('CACHE_CONFIGURATION'), {}).get(str('TIMEOUT_FORSETI'), 10))
    def get_response(self, arguments):
        """
        Get vehicle_position information from Forseti webservice
        """
        raw_response = self._call_webservice(arguments)

        # We don't need any further action if raw_response is None
        if raw_response is None:
            return None
        resp = self.response_marshaller(raw_response)
        if resp is None:
            return None
        return resp.get('vehicle_positions', [])

    def _line_code_add_vehicle_position(self, vehicle_position, response_json):
        vehicle_journey_position = type_pb2.VehicleJourneyPosition()
        vehicle_journey_position.coord.lon = response_json.get("longitude")
        vehicle_journey_position.coord.lat = response_json.get("latitude")
        vehicle_journey_position.bearing = response_json.get("bearing")
        vehicle_journey_position.speed = response_json.get("speed")
        vehicle_journey_position.data_freshness = type_pb2.REALTIME
        # the property `occupancy`
        occupancy = response_json.get("occupancy", None)
        if occupancy is not None:
            vehicle_journey_position.occupancy = occupancy
        # the property `feed_created_at`
        feed_created_at = response_json.get("feed_created_at", None)
        if feed_created_at:
            feed_created_at_timestamp = utils.make_timestamp_from_str(feed_created_at)
            vehicle_journey_position.feed_created_at = feed_created_at_timestamp
        vehicle_position.vehicle_journey_positions.append(vehicle_journey_position)

    def update_response(self, instance, vehicle_positions, **kwargs):
        futures = []
        # TODO define new parameter forseti_pool_size ?
        pool = gevent.pool.Pool(instance.realtime_pool_size)

        # Copy the current request context to be used in greenlet
        reqctx = utils.copy_flask_request_context()

        def line_code_worker(vehicle_position, args):
            # Use the copied request context in greenlet
            with utils.copy_context_in_greenlet_stack(reqctx):
                return vehicle_position, self.get_response(args)

        # Remove all items of the list `vehicle_journey_positions`
        for vehicle_position in vehicle_positions:
            num_of_vehicle_journey_positions = len(vehicle_position.vehicle_journey_positions)
            for _ in range(num_of_vehicle_journey_positions):
                del vehicle_position.vehicle_journey_positions[-1]

        # Keep all line codes
        for vehicle_position in vehicle_positions:
            line_uri = vehicle_position.line.uri
            line_code = string.split(line_uri, ":")[2]
            args = self.get_codes('line', line_code)
            futures.append(pool.spawn(line_code_worker, vehicle_position, args))

        for future in gevent.iwait(futures):
            vehicle_position, response = future.get()
            if response is not None:
                for i, res_element in enumerate(response):
                    self._line_code_add_vehicle_position(vehicle_position, res_element)
