# Copyright 2017 Red Hat, Inc.
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

import json

from testlib import VdsmTestCase
from testlib import mock

from vdsm.network.link import dpdk


class ReportDpdkPortsTests(VdsmTestCase):

    def test_vfio_pci_driver(self):
        self._test_one_dpdk_device('vfio-pci')

    def test_igb_uio_driver(self):
        self._test_one_dpdk_device('igb_uio')

    def test_uiopci__generic_driver(self):
        self._test_one_dpdk_device('uio_pci_generic')

    def _test_one_dpdk_device(self, driver):
        lshw_output = json.dumps({'id': 'fake.redhat.com', 'class': 'system',
                                  'vendor': 'HP', 'serial': 'GB803344A9',
                                  'children': [
                                      {'id': 'core', 'class': 'bus',
                                       'description': 'Motherboard', },
                                      {'id': 'pci:0', 'class': 'bridge',
                                       'handle': 'PCIBUS:0000:00',
                                       'description': 'Host bridge',
                                       'product': '5500 I/O Hub to ESI Port',
                                       'vendor': 'Intel Corporation',
                                       'children': [
                                           {'id': 'network:1',
                                            'class': 'network',
                                            'handle': 'PCI:0000:02:00.1',
                                            'vendor': 'Intel Corporation',
                                            'configuration': {
                                                'driver': driver}}]}]})

        with mock.patch.object(dpdk, 'execCmd',
                               return_value=(
                                   0, lshw_output.encode('utf-8'), None)):
            expected_ports = {'dpdk0': '0000:02:00.1'}
            self.assertEqual(expected_ports, dpdk.get_dpdk_devices())

    def test_two_different_dpdk_devices(self):
        lshw_output = json.dumps({'id': 'fake.redhat.com', 'class': 'system',
                                  'vendor': 'HP', 'serial': 'GB803344A9',
                                  'children': [
                                      {'id': 'core', 'class': 'bus',
                                       'description': 'Motherboard', },
                                      {'id': 'pci:0', 'class': 'bridge',
                                       'handle': 'PCIBUS:0000:00',
                                       'description': 'Host bridge',
                                       'product': '5500 I/O Hub to ESI Port',
                                       'vendor': 'Intel Corporation',
                                       'children': [
                                           {'id': 'network:1',
                                            'class': 'network',
                                            'handle': 'PCI:0000:02:00.1',
                                            'vendor': 'Intel Corporation',
                                            'configuration': {
                                                'driver': 'vfio-pci'}},
                                           {'id': 'network:2',
                                            'class': 'network',
                                            'handle': 'PCI:0000:02:00.2',
                                            'vendor': 'Intel Corporation',
                                            'configuration': {
                                                'driver': 'igb_uio'}}]}]})

        with mock.patch.object(dpdk, 'execCmd',
                               return_value=(
                                   0, lshw_output.encode('utf-8'), None)):
            expected_ports = {'dpdk0': '0000:02:00.1', 'dpdk1': '0000:02:00.2'}
            self.assertEqual(expected_ports, dpdk.get_dpdk_devices())

    def test_no_dpdk_devices(self):
        lshw_output = json.dumps({'id': 'fake.redhat.com', 'class': 'system',
                                  'vendor': 'HP', 'serial': 'GB803344A9',
                                  'children': [
                                      {'id': 'core', 'class': 'bus',
                                       'description': 'Motherboard', },
                                      {'id': 'pci:0', 'class': 'bridge',
                                       'handle': 'PCIBUS:0000:00',
                                       'description': 'Host bridge',
                                       'product': '5500 I/O Hub to ESI Port',
                                       'vendor': 'Intel Corporation',
                                       'children': [
                                           {'id': 'network:1',
                                            'class': 'network',
                                            'handle': 'PCI:0000:02:00.1',
                                            'vendor': 'Intel Corporation',
                                            'configuration': {
                                                'driver': 'igb'}}]}]})

        with mock.patch.object(dpdk, 'execCmd',
                               return_value=(
                                   0, lshw_output.encode('utf-8'), None)):
            expected_ports = {}
            self.assertEqual(expected_ports, dpdk.get_dpdk_devices())

    def test_is_dpdk_true(self):
        self.assertTrue(dpdk.is_dpdk(dev_name='dpdk0'))

    def test_is_dpdk_false(self):
        self.assertFalse(dpdk.is_dpdk(dev_name='not_dpdk_dev'))
