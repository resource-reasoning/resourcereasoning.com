require 'test/unit'
require 'yaml'

class TestPapers < Test::Unit::TestCase
  @@papers = YAML.load_file('_data/papers.yaml')

  n = 0
  @@papers.each do |paper|
    n += 1
    test "test paper #{n} has title" do
      assert_includes paper, 'title'
      assert_kind_of String, paper['title']
    end
    test "test paper #{n} has authors" do
      assert_includes paper, 'authors'
      assert_kind_of String, paper['authors']
    end
    test "test paper #{n} has venue" do
      assert_includes paper, 'venue'
      assert_kind_of String, paper['venue']
    end
    test "test paper #{n} has abstract" do
      assert_includes paper, 'abstract'
      assert_kind_of String, paper['abstract']
    end

    test "warn if paper #{n} has no link" do
      unless ['pdf','ps','pdflong','pslong'].any? { |field| paper.include? field }
        STDERR.puts "\nWARNING: '#{paper['title']}' is missing a document URL"
      end
    end

    test "warn if paper #{n} has no pubdate" do
      unless paper.include? 'pubdate'
        STDERR.puts"\nWARNING: '#{paper['title']}' is missing a pubdate"
      end
    end
  end
end
