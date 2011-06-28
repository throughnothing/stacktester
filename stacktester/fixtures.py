IMAGE_FIXTURES = [
    {
        'name': 'ramdisk',
        'disk_format': 'ari',
        'container_format': 'ari',
        'is_public': True,
        'location' : 'http://c625682.r82.cf2.rackcdn.com/ramdisk',
    },
    {
        'name': 'kernel',
        'disk_format': 'aki',
        'container_format': 'aki',
        'is_public': True,
        'location' : 'http://c625682.r82.cf2.rackcdn.com/kernel',
        'properties' : {
            'key1' : 'value1',
            'key2' : 'value2',
        },
    },
    {
        'name': 'image',
        'disk_format': 'ami',
        'container_format': 'ami',
        'is_public': True,
        'location' : 'http://c625682.r82.cf2.rackcdn.com/image',
        'properties' : {
            'key1' : 'value1',
        },
    },
]


FLAVOR_FIXTURES = [
    {"flavorid": 1, "name": "m1.tiny", "ram": 512, "vcpus": 1, "disk": 0},
    {"flavorid": 2, "name": "m1.small", "ram": 2048, "vcpus": 1, "disk": 20},
]


SERVER_FIXTURES = [
    {
        'server' : {
            'name' : 'testserver',
            # This will pull the imageRef for the image 
            # fixture with name 'image'
            'imageRef' : 'image',
            # This will pull the flavorRef for the flavor
            # fixture with name 'm1.tiny'
            'flavorRef' : 'm1.tiny',
        }
    },
]

class BaseFixtures(object):
    def __init__(self, fixtures=None)
        self.os = openstack.Manager()
        self.config = stacktester.config.StackConfig()

        if fixtures:
            self.setUp(fixtures)


class ImageFixtures(BaseFixtures):
    def setUp(image_fixtures):
        self.images = {} for fixture in image_fixtures:
            meta = self.os.glance.add_image(fixture, None)
            self.images[meta['name']] = {'id': meta['id']}

    def tearDown():
        for image in self.images.itervalues():
            self.os.glance.delete_image(image['id'])



class FlavorFixtures(BaseFixtures):
    def setUp(flavor_fixtures):
        pass

    def tearDown():
        pass


class ServerFixtures(BaseFixtures):
    def setUp(server_fixtures):
        pass

    def tearDown():
        pass
