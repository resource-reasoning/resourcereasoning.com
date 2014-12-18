require 'html/proofer'

task :default => :build

desc "Build the site"
task :build do
  sh "bundle exec jekyll build"
end

desc "Build the site and test output for dead links, invalid html etc."
task :test => :build do
  ignore = [/issues\/new/] # GitHub 400s when we poke it
  HTML::Proofer.new("./_site", {:validate_html => true, :href_ignore => ignore}).run
end

desc "Build the site, rebuild when files are edited, and serve via a local http server"
task :serve do
  sh "bundle exec jekyll serve"
end
