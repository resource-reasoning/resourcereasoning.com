require 'test/unit'
require 'json-schema'

class TestPeople < Test::Unit::TestCase
  Dir.foreach('_data') do |x|
    if x.end_with? '.json'
      if File.exist? "_schema/#{x}"
        test "#{x} is valid" do
          assert_nothing_thrown do
            JSON::Validator.validate!("_schema/#{x}", "_data/#{x}")
          end
        end
      end
    end
  end
end
