# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import json

import unittest2 as unittest

from stacktester import openstack


class ServersMetadataTest(unittest.TestCase):

    def setUp(self):
        self.os = openstack.Manager()
        self.image_ref = self.os.config.env.image_ref
        self.flavor_ref = self.os.config.env.flavor_ref

        body = json.dumps({
            'server' : {
                'name' : 'testserver',
                'imageRef' : self.image_ref,
                'flavorRef' : self.flavor_ref,
                'metadata' : {
                    'testEntry' : 'testValue',
                },
            },
        })

        response, body = self.os.nova.request('POST', '/servers', body=body)

        data = json.loads(body)
        self.server_id = data['server']['id']
    
    def tearDown(self):
        self.os.nova.request('DELETE', '/servers/%s' % self.server_id)

    def test_get_server_metadata(self):
        """Test that we can retrieve metadata for a server"""

        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        self.assertEqual(200, response.status)

        result = json.loads(body)
        expected = {
            'metadata' : { 
                'testEntry' : 'testValue',
            },
        }
        self.assertEqual(expected, result)

    def test_update_server_metadata(self):
        """Test that we can update metadata for a server"""

        post_metadata = {
            'metadata' : {
                'new_entry1' : 'new_value1',
                'new_entry2' : 'new_value2',
            },
        }
        post_body = json.dumps(post_metadata)

        url = '/sirvers/%s/meta' % self.server_id
        response, body = self.os.nova.request('POST', url, body=post_body)
        # KNOWN-ISSUE lp:804067
        #self.assertEqual(201, response.status)

        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        self.assertEqual(200, response.status)

        result = json.loads(body)
        expected = post_metadata
        expected['testEntry'] = 'testValue'
        self.assertEqual(expected, result)

    def test_replace_server_metadata(self):
        """
        Test that we can update metadata for a server, 
        removing unspecified entries
        """

        expected = {
            'metadata' : {
                'new_entry1' : 'new_value1',
                'new_entry2' : 'new_value2',
            },
        }

        url = '/servers/%s/meta' % self.server_id
        post_body = json.dumps(expected)
        response, body = self.os.nova.request('POST', url, body=post_body)
        # KNOWN-ISSUE lp:804067
        #self.assertEqual(201, response.status)

        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        self.assertEqual(200, response.status)

        result = json.loads(body)
        # We want to make sure 'testEntry' was removed
        self.assertEqual(expected, result)

    def test_get_server_metadata_key(self):
        """Test that we can retrieve specific metadata key for a server"""

        url = '/servers/%s/meta/testEntry' % self.server_id
        response, body = self.os.nova.request('GET', url)
        self.assertEqual(200, response.status)

        result = json.loads(body)
        expected = {
            'meta':{
                'testEntry':'testValue',
            },
        }
        self.assertDictEqual(expected, result)

    def test_add_server_metadata_key(self):
        """Test that we can add specific metadata key to a server"""

        expected_metadata = {
            'metadata' : {
                'testEntry' : 'testValue',
                'new_meta1' : 'new_value1', 
            },
        }

        expected_meta = {
            'meta' : {
                'new_meta1' : 'new_value1', 
            },
        }

        put_body = json.dumps(expected_meta)

        url = '/servers/%s/meta/new_meta1' % self.server_id
        response, body = self.os.nova.request('PUT', url, body=put_body)
        # KNOWN-ISSUE lp:804067
        #self.assertEqual(201, response.status)
        result = json.loads(body)
        self.assertDictEqual(expected_meta, result)

        # Now check all metadata to make sure the other values are there
        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        result = json.loads(body)
        self.assertDictEqual(expected_metadata, result)

    def test_update_server_metadata_key(self):
        """Test that we can update specific metadata key for a server"""

        expected_meta = {
            'meta' : {
            'testEntry' : 'testValue2',
            },
        }
        put_body = json.dumps(expected_meta)

        url = '/servers/%s/meta/testEntry' % self.server_id
        response, body = self.os.nova.request('PUT', url, body=put_body)
        # KNOWN-ISSUE lp:804067
        #self.assertEqual(201, response.status)
        result = json.loads(body)
        self.assertEqual(expected_meta, result)

        # Now check all metadata to make sure the other values are there
        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        result = json.loads(body)
        expected_metadata = {}
        expected_metadata['metadata'] = expected_meta['meta']
        self.assertDictEqual(expected_metadata, result)

    def test_delete_server_metadata_key(self):
        """Test that we can delete metadata for a server"""

        url = '/servers/%s/meta/testEntry' % self.server_id
        response, body = self.os.nova.request('DELETE', url)
        # KNOWN-ISSUE lp:804067
        #self.assertEquals(204, response.status)


        url = '/servers/%s/meta' % self.server_id
        response, body = self.os.nova.request('GET', url)
        self.assertEquals(200, response.status)

        result = json.loads(body)
        self.assertDictEqual({'metadata':{}}, result)
