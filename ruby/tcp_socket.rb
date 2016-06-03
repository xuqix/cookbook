#!/usr/bin/env ruby

require 'thread'
require 'socket'

interval = 15
count = 1024

port = 2000
hostname = 'localhost'

threads = []
count.times do |idx|
  threads << Thread.new do |t|
    print "start thread #{idx}\n"
    begin
      s = TCPSocket.open(hostname, port)
      while true do
        print "write data by thread #{idx}\n"
        s.write("\x00" * 16)
        sleep interval
      end
    rescue
      print "thread #{idx} connect exception, exit\n"
    end
  end
end

threads.each { |t| t.join }

