require 'test/unit'
require 'json-schema'

class TestPeople < Test::Unit::TestCase
  def test_people_schema
    assert_nothing_thrown do
      JSON::Validator.validate!('_schema/people.json', '_data/people.json')
    end
  end
end
