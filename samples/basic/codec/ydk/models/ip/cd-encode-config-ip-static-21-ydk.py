#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Encode config for model Cisco-IOS-XR-ip-static-cfg.

usage: cd-encode-config-ip-static-21-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.ip import Cisco_IOS_XR_ip_static_cfg as xr_ip_static_cfg
import logging


def config_router_static(router_static):
    """Add config data to router_static object."""
    vrf_unicast = router_static.default_vrf.address_family.vrfipv6.vrf_unicast
    vrf_prefix = vrf_unicast.vrf_prefixes.VrfPrefix()
    vrf_prefix.prefix = "::"
    vrf_prefix.prefix_length = 0
    vrf_next_hop_next_hop_address = vrf_prefix.vrf_route.vrf_next_hop_table. \
        VrfNextHopNextHopAddress()
    vrf_next_hop_next_hop_address.next_hop_address = "2001:db8::1:3"
    vrf_prefix.vrf_route.vrf_next_hop_table.vrf_next_hop_next_hop_address. \
        append(vrf_next_hop_next_hop_address)
    vrf_unicast.vrf_prefixes.vrf_prefix.append(vrf_prefix)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    router_static = xr_ip_static_cfg.RouterStatic()  # create config object
    config_router_static(router_static)  # add object configuration

    print(codec.encode(provider, router_static))  # encode and print object
    provider.close()
    exit()
# End of script
