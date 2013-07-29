from mock import *
from nose.tools import *
from xblock.core import *

def test_list_field_access():
    # Check that values that are deleted are restored to their default values
    class FieldTester(XBlock):
        """Test XBlock for field access testing"""
        field_a = List(scope=Scope.settings)
        field_b = List(scope=Scope.content, default=[1, 2, 3])
        field_c = List(scope=Scope.content, default=[4, 5, 6])

    field_tester = FieldTester(MagicMock(), {'field_a': [200], 'field_b': [11, 12, 13]})

    print 'm_d:', field_tester._model_data
    print 'CHECK INITIAL VALUES HAVE BEEN SET PROPERLY'
    # Check initial values have been set properly
    assert_equals([200], field_tester.field_a)
    assert_equals([11, 12, 13], field_tester.field_b)
    assert_equals([4, 5, 6], field_tester.field_c)

    print 'cache:', field_tester._model_data_cache
    print 'm_d:', field_tester._model_data
    # Update the fields
#    from pudb import set_trace; set_trace()
    print 'UPDATING THE FIELDS'
    field_tester.field_a.append(1)
    field_tester.field_b.append(14)
    field_tester.field_c.append(7)
#    print field_tester.field_a
    
    print 'cache:', field_tester._model_data_cache
    print 'm_d:', field_tester._model_data
    print 'DIRTY FIELDS:', field_tester._dirty_fields

    # The fields should be update in the cache, but /not/ in the underlying kvstore.
    print 'THE FIELDS SHOULD BE UPDATE IN THE CACHE, BUT /NOT/ IN THE UNDERLYING KVSTORE.'
    assert_equals([200, 1], field_tester.field_a)
    assert_equals([11, 12, 13, 14], field_tester.field_b)
    assert_equals([4, 5, 6, 7], field_tester.field_c)

    print 'LOOKING AT _MODEL_DATA DIRECTLY'
    assert_equals([200], field_tester._model_data['field_a'])
    assert_equals([11, 12, 13], field_tester._model_data['field_b'])
    assert_not_in('field_c', field_tester._model_data)

    # Now save - after save, the values should be the same in the cache and the model data
    print 'SAVING'
    field_tester.save()
    print 'cache:', field_tester._model_data_cache
    print 'm_d:', field_tester._model_data
    print 'DIRTY FIELDS:', field_tester._dirty_fields
    
    assert_equals([200, 1], field_tester.field_a)
    assert_equals([11, 12, 13, 14], field_tester.field_b)
    assert_equals([4, 5, 6, 7], field_tester.field_c)

    print 'LOOKING AT _MODEL_DATA DIRECTLY'
    assert_equals([200, 1], field_tester._model_data['field_a'])
    assert_equals([11, 12, 13, 14], field_tester._model_data['field_b'])
    assert_equals([4, 5, 6, 7], field_tester._model_data['field_c'])


def test_field_access():
    class FieldTester(XBlock):
        """Test XBlock for field access testing"""
        field_a = Integer(scope=Scope.settings)
        field_b = Integer(scope=Scope.content, default=10)
        field_c = Integer(scope=Scope.user_state, default='field c')

    field_tester = FieldTester(MagicMock(), {'field_a': 5, 'field_x': 15})
    # Verify that the fields have been set
    print 'm_d:', field_tester._model_data
    print "CHECK INITIAL VALUES"
    assert_equals(5, field_tester.field_a)
    assert_equals(10, field_tester.field_b)
    assert_equals('field c', field_tester.field_c)
    assert not hasattr(field_tester, 'field_x')

    print 'SET NEW FIELD VALUES'
    # Set one of the fields.
    field_tester.field_a = 20
    field_tester.field_b = 200
    field_tester.field_c = 2000
    field_tester.field_x = 20000
    print 'cache:', field_tester._model_data_cache
    print 'm_d:', field_tester._model_data

    # field_a should be updated in the cache, but /not/ in the underlying kvstore
    assert_equals(20, field_tester.field_a)
    assert_equals(5, field_tester._model_data['field_a'])
    # save the XBlock
    print 'SAVE'
    field_tester.save()
    print 'cache:', field_tester._model_data_cache
    print 'm_d:', field_tester._model_data
    # verify that the fields have been updated correctly
    assert_equals(20, field_tester.field_a)
    # Now, field_a should be updated in the underlying kvstore
    assert_equals(20, field_tester._model_data['field_a'])
    assert_equals(10, field_tester.field_b)
    assert_equals('field c', field_tester.field_c)

    del field_tester.field_a
    assert_equals(None, field_tester.field_a)
    assert hasattr(FieldTester, 'field_a')

if __name__ == "__main__":
    test_list_field_access()
#    test_field_access()
