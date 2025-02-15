# -*- coding: utf-8 -*-
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
import pytest

from jormungandr.tests.utils_test import MockResponse
from tests.check_utils import get_not_null, s_coord, r_coord, journey_basic_query
from tests.tests_mechanism import dataset, NewDefaultScenarioAbstractTestFixture

DUMMY_INSTANT_SYSTEM_FEED_PUBLISHER = {'id': '42', 'name': '42', 'license': 'I dunno', 'url': 'http://w.tf'}

MOCKED_INSTANCE_CONF = {
    'scenario': 'new_default',
    'instance_config': {
        'ridesharing': [
            {
                "args": {
                    "service_url": "http://wtf",
                    "api_key": "key",
                    "network": "Super Covoit",
                    "rating_scale_min": 0,
                    "rating_scale_max": 5,
                    "crowfly_radius": 200,
                    "timeframe_duration": 1800,
                    "feed_publisher": DUMMY_INSTANT_SYSTEM_FEED_PUBLISHER,
                },
                "class": "jormungandr.scenarios.ridesharing.instant_system.InstantSystem",
            }
        ]
    },
}

INSTANT_SYSTEM_RESPONSE = {
    "total": 1,
    "journeys": [
        {
            "id": "4bcd0b9d-2c9d-42a2-8ffb-4508c952f4fb",
            "departureDate": "2017-12-25T08:07:59+01:00",
            "arrivalDate": "2017-12-25T08:25:36+01:00",
            "duration": 55,
            "distance": 224,
            "url": "https://jky8k.app.goo.gl/?efr=1&apn=com.is.android.rennes&ibi=&isi=&utm_campaign=KISIO&link=https%3A%2F%2Fwww.star.fr%2Fsearch%2F%3FfeatureName%3DsearchResultDetail%26networkId%3D33%26journeyId%3D4bcd0b9d-2c9d-42a2-8ffb-4508c952f4fb",
            "paths": [
                {
                    "mode": "RIDESHARINGAD",
                    "from": {"name": "", "lat": 0.0000898312, "lon": 0.0000898312},
                    "to": {"name": "", "lat": 0.00071865, "lon": 0.00188646},
                    "departureDate": "2017-12-25T08:07:59+01:00",
                    "arrivalDate": "2017-12-25T08:25:36+01:00",
                    "shape": "wosdH|ihIRVDTFDzBjPNhADJ\\`C?TJt@Hj@h@tDp@bFR?bAFRBZDR@JCL@~AJl@Df@DfBNv@B~@DjAFh@HXH~@VbEfANDh@PdAl@\\RdAZnBHpADvBDf@@d@Gv@S\\OlAOl@EbAHjAVNDd@Dd@Mt@u@FGrE{EtBaBr@zCp@dDd@~BRtAHj@X`BFXlAjDLd@v@dDXlAh@TVl@hBtIB`ANpAh@nBf@xATf@Xd@JFPD@JHRLBLKDBbCbBbBbBjApA?VHPPBL`@\\^|BrBDHJ`@AP?PDRFL\\TRAJGRD`Al@jBhA~BbBx@VfALl@PHVDHPFNCVNdCnBpHzDdB|AfAjAj@h@^d@jAhBhAvA?^BNFJPHPCFGVNpBhApBt@ZL|B^dCJfDAZFLRHBNEJQZIdUa@b@JJ`@TXTFTAPKNUH]nBGtOb@vDd@`C`ArAp@zAjAnBnBJJh@h@`_@l`@fIvIfMhNl@t@dAzBnAnDx@xDh@jFfBbRdAnMdBnSjB|JbDbIhMj[rN`_@nEfJzCxDrCtDl@pBDtE^Bn@?h@?t@IdAe@XUFIvBaBvBaBf@Wl@OdAEfAJJXJHJBLCbAbAx@j@fBn@p@X`HfDdAd@NB\\CBLJDFCBI?OGILYn@gDb@uAVe@\\_@jEgDlFgARElBa@|G}AxFwA`AWv@YNI~AaArAg@bEw@pA[t@Y`B{@~BmAtAo@fAk@TYBBH?DGBKTEd@U^QlBcA^QvEcCP@Le@Cm@Eo@Ia@AI",
                    "rideSharingAd": {
                        "id": "24bab9de-653c-4cc4-a947-389c59cf0423",
                        "type": "DRIVER",
                        "from": {"name": "9 Allee Rochester, Rennes", "lat": 0.0000998312, "lon": 0.0000998312},
                        "to": {"name": "2 Avenue Alphonse Legault, Bruz", "lat": 0.00081865, "lon": 0.00198646},
                        "user": {
                            "alias": "Jean P.",
                            "gender": "MALE",
                            "imageUrl": "https://dummyimage.com/128x128/C8E6C9/000.png&text=JP",
                            "rating": {"rate": 0, "count": 0},
                        },
                        "price": {"amount": 170.0, "currency": "EUR"},
                        "vehicle": {"availableSeats": 4},
                    },
                }
            ],
        }
    ],
    "url": "https://jky8k.app.goo.gl/?efr=1&apn=com.is.android.rennes&ibi=&isi=&utm_campaign=KISIO&link=https%3A%2F%2Fwww.star.fr%2Fsearch%2F%3FfeatureName%3DsearchResults%26networkId%3D33%26from%3D48.109377%252C-1.682103%26to%3D48.020335%252C-1.743929%26multimodal%3Dfalse%26departureDate%3D2017-12-25T08%253A00%253A00%252B01%253A00",
}


def mock_instant_system(_, params, headers):
    return MockResponse(INSTANT_SYSTEM_RESPONSE, 200)


@pytest.fixture(scope="function", autouse=True)
def mock_http_instant_system(monkeypatch):
    monkeypatch.setattr(
        'jormungandr.scenarios.ridesharing.instant_system.InstantSystem._call_service', mock_instant_system
    )


@pytest.fixture(scope="function", autouse=True)
def mock_instance_ridesharing_greenlet_pool_size(monkeypatch):
    monkeypatch.setattr(
        'jormungandr.instance.Instance.ridesharing_greenlet_pool_size', property(fget=lambda i: True)
    )


@dataset({'main_routing_test': MOCKED_INSTANCE_CONF})
class TestRidesharingServiceManager(NewDefaultScenarioAbstractTestFixture):
    """
    Integration test with Instant System
    Note: '&forbidden_uris[]=PM' used to avoid line 'PM' and it's vj=vjPB in /journeys
    """

    def test_ridesharing_service_manager_async(self):
        """
        test ridesharing_jouneys details
        """
        q = (
            "journeys?from=0.0000898312;0.0000698312&to=0.00188646;0.00071865&datetime=20120614T075500&"
            "first_section_mode[]={first}&last_section_mode[]={last}&forbidden_uris[]=PM&_min_ridesharing=0".format(
                first='ridesharing', last='walking'
            )
        )
        response = self.query_region(q)
        self.is_valid_journey_response(response, q, check_journey_links=False)

        journeys = get_not_null(response, 'journeys')
        assert len(journeys) == 1
        tickets = response.get('tickets')
        assert len(tickets) == 1
        assert tickets[0].get('cost').get('currency') == 'centime'
        assert tickets[0].get('cost').get('value') == '170.0'
        ticket = tickets[0]

        ridesharing_kraken = journeys[0]
        assert 'ridesharing' in ridesharing_kraken['tags']
        assert 'non_pt' in ridesharing_kraken['tags']
        assert ridesharing_kraken.get('type') == 'best'
        assert ridesharing_kraken.get('durations').get('ridesharing') > 0
        assert ridesharing_kraken.get('durations').get('total') == ridesharing_kraken['durations']['ridesharing']
        assert ridesharing_kraken.get('distances').get('ridesharing') > 0

        rs_sections = ridesharing_kraken.get('sections')
        assert len(rs_sections) == 1
        assert rs_sections[0].get('mode') == 'ridesharing'
        assert rs_sections[0].get('type') == 'street_network'

        sections = ridesharing_kraken.get('sections')

        rs_journeys = sections[0].get('ridesharing_journeys')
        assert len(rs_journeys) == 1
        assert rs_journeys[0].get('distances').get('ridesharing') == 224
        assert rs_journeys[0].get('durations').get('walking') == 2
        assert rs_journeys[0].get('durations').get('ridesharing') == 1057
        assert 'ridesharing' in rs_journeys[0].get('tags')
        rsj_sections = rs_journeys[0].get('sections')
        assert len(rsj_sections) == 3

        assert rsj_sections[0].get('type') == 'crow_fly'
        assert rsj_sections[0].get('mode') == 'walking'
        assert rsj_sections[0].get('duration') == 2
        assert rsj_sections[0].get('departure_date_time') == '20171225T070757'
        assert rsj_sections[0].get('arrival_date_time') == '20171225T070759'

        assert rsj_sections[1].get('type') == 'ridesharing'
        assert rsj_sections[1].get('duration') == 1057
        assert rsj_sections[1].get('departure_date_time') == '20171225T070759'
        assert rsj_sections[1].get('arrival_date_time') == '20171225T072536'
        assert rsj_sections[1].get('geojson').get('coordinates')[0] == [0.0000898312, 0.0000898312]
        assert rsj_sections[1].get('geojson').get('coordinates')[2] == [-1.68635, 48.1101]
        rsj_info = rsj_sections[1].get('ridesharing_informations')
        assert rsj_info.get('driver').get('alias') == 'Jean P.'
        assert rsj_info.get('driver').get('gender') == 'male'
        assert rsj_info.get('driver').get('image') == 'https://dummyimage.com/128x128/C8E6C9/000.png&text=JP'
        assert rsj_info.get('driver').get('rating').get('scale_min') == 0.0
        assert rsj_info.get('driver').get('rating').get('scale_max') == 5.0
        assert rsj_info.get('network') == 'Super Covoit'
        assert rsj_info.get('operator') == 'instant_system'
        assert rsj_info.get('seats').get('available') == 4

        assert 'total' not in rsj_info.get('seats')

        rsj_links = rsj_sections[1].get('links')
        assert len(rsj_links) == 2
        assert rsj_links[0].get('rel') == 'ridesharing_ad'
        assert rsj_links[0].get('type') == 'ridesharing_ad'

        assert rsj_links[1].get('rel') == 'tickets'
        assert rsj_links[1].get('type') == 'ticket'
        assert rsj_links[1].get('id') == ticket['id']
        assert ticket['links'][0]['id'] == rsj_sections[1]['id']
        assert rs_journeys[0].get('fare').get('total').get('value') == tickets[0].get('cost').get('value')

        assert rsj_sections[2].get('type') == 'crow_fly'
        assert rsj_sections[2].get('mode') == 'walking'
        assert rsj_sections[2].get('duration') == 0
        assert rsj_sections[2].get('departure_date_time') == '20171225T072536'
        assert rsj_sections[2].get('arrival_date_time') == '20171225T072536'

        fps = response['feed_publishers']
        assert len(fps) == 2

        def equals_to_dummy_fp(fp):
            return fp == DUMMY_INSTANT_SYSTEM_FEED_PUBLISHER

        assert any(equals_to_dummy_fp(fp) for fp in fps)
