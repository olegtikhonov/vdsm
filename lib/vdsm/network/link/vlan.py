# Copyright 2018 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#
from __future__ import absolute_import
from __future__ import division

from vdsm.network.link import bond
from vdsm.network.link import iface
from vdsm.network.link import nic


def speed(dev_name):
    """Return the vlan's underlying device speed."""
    dev_speed = 0
    interface = iface.iface(dev_name)
    iface_type = interface.type()
    if iface_type == iface.Type.NIC:
        # vlans on a nics expose the speed through sysfs
        dev_speed = nic.read_speed_using_sysfs(dev_name)
    elif iface_type == iface.Type.BOND:
        dev_speed = bond.speed(dev_name)

    return dev_speed


def get_vlans_on_base_device(base_dev_name):
    return (iface_properties['name'] for iface_properties in iface.list()
            if iface_properties.get('device') == base_dev_name and
            iface_properties.get('type') == iface.Type.VLAN)


def is_base_device(dev_name):
    return any(get_vlans_on_base_device(dev_name))
