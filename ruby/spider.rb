#!/usr/bin/env ruby

require 'fileutils'
require 'socket'
require 'thread'
require 'net/http'

host = 'http://ruby-doc.org/stdlib-2.3.0/libdoc/open-uri/rdoc'     # web服务器
port = 80                           # 默认 HTTP 端口
path = '/index.html'                 # 想要获取的文件地址
url = host + path
max_size = 1000 * 1000 * 20


$total_size = 0
$idx = 0
def download(url)
  content = Net::HTTP.get(URI(url))
  File::open("data/html#{$idx}.html", "w") do |f|
    f.write content
    $total_size += content.size
    $idx += 1
  end
end

que = Queue.new
que.push url

FileUtils.mkdir_p('data') unless File.exists?('data')
while not que.empty? do
  content = Net::HTTP.get(URI(que.pop))
  content.scan(/<a [\s\S]*?href=['"](\S+?)['"][\s\S]*?>/) do |m|
    path = m[0]
    if not (/http:\/\//.match(path))
      path = path[0]=='/' ? path : ('/'+path)
      path = "#{host}#{path}"
    end
    que.push path
    begin
      download path
    ensure
      print("download #{path} error!\n")
    end
    if $total_size > max_size
      print("total size: #{$total_size / 1000 / 1000}mb\n")
      break
    end
  end
end

