require 'test/unit'
require 'json'

class TestPeople < Test::Unit::TestCase
  @@people = JSON.parse(File.read('_data/people.json'))

  def test_people_has_current_and_former
    assert_includes @@people, 'current'
    assert_includes @@people, 'former'
  end

  n = 0
  (@@people['current'] + @@people['former']).each do |person|
    n += 1
    test "test person #{n} has firstname" do
      assert_includes person, 'firstname'
      assert_kind_of String, person['firstname']
    end

    test "test person #{n} has lastname" do
      assert_includes person, 'lastname'
      assert_kind_of String, person['lastname']
    end

    test "test person #{n} has affiliation string or array" do
      assert_includes person, 'affiliations'
      refute_kind_of Hash, person['affiliations']
    end

    test "test if person #{n} has string url" do
      if person.include? 'url'
        assert_kind_of String, person['url']
      end
    end
  end
end
