import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parameters(self):
        from ezrest.models import Model
        from ezrest.parameters import Parameter, UnsetParameter

        class MyModel(Model):
            foo = Parameter(create=True)
            bar = Parameter(read=True, default='abc')
            baz = Parameter(update=True)
            zee = Parameter(delete=True)
            maz = Parameter(default=56)

        obj = MyModel()
        obj2 = MyModel()

        assert obj.foo == UnsetParameter
        assert obj.bar == 'abc'
        assert obj.baz == UnsetParameter
        assert obj.baz == UnsetParameter
        assert obj.maz == 56

        assert len(obj._meta.all_parameters) == len([MyModel.foo, MyModel.bar, MyModel.baz, MyModel.zee, MyModel.maz])

        assert len(obj._meta.create_parameters) == 1
        assert len(obj._meta.read_parameters) == 1
        assert len(obj._meta.update_parameters) == 1
        assert len(obj._meta.delete_parameters) == 1

        obj.maz = 'this is the light'

        assert obj.maz == 'this is the light'

        serial = obj.parameters('maz')

        assert len(serial.values) == 1
        assert serial.requires_multipart == False
        assert serial.to_get() == 'maz=this%20is%20the%20light', serial.to_get()
        assert serial.to_post() == 'maz=this%20is%20the%20light', serial.to_post() # post vars should look the same as get vars 


        assert obj2.maz == 56, obj2.maz

        obj.foo = 'foo'
        obj.bar = 'foo'
        obj.baz = 'foo'
        obj.zee = 'foo'
        obj.maz = 'foo'

        assert obj.parameters('baz')
        assert obj.all_parameters()
        assert obj.create_parameters()
        assert obj.read_parameters()
        assert obj.update_parameters()
        assert obj.delete_parameters()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_Parameters']
    unittest.main()
