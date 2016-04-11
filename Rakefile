require 'html-proofer'
require 'rake/testtask'

task :default => :build

desc "Build the site"
task :build do
  sh "bundle exec jekyll build"
end

Rake::TestTask.new do |t|
  t.test_files = FileList['_tests/*.rb']
  t.verbose = true
end

htmlproofer_config = {
  :file_ignore => [/_site\/edit/],
  :href_ignore => [/issues\/new/], # GitHub 400s when we poke it
  :disable_external => true,
  :check_html => true,
  :parallel => { :in_processes => 4 }
}

desc "Build the site and test output for dead links, invalid html etc."
task :test => :build do
  HTMLProofer.check_directory("./_site", htmlproofer_config).run
end

desc "Test dead external links"
task :testlinks => :build do
  HTMLProofer.check_directory("./_site", htmlproofer_config.merge({
    :disable_external => false,
    :typhoeus => { :ssl_verifypeer => false, :ssl_verifyhost => 0 },
  })).run
end


desc "Build the site, rebuild when files are edited, and serve via a local http server"
task :serve do
  sh "bundle exec jekyll serve"
end
