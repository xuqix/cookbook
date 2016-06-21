#!/usr/bin/env ruby

require 'fileutils'

module Builder
  @@out = $stdout
  def self.set_out(s)
    @@out = s
  end

  def self.write(str)
    @@out << str
  end

  Tag = [:html, :head, :title, :body, :h1, :h2, :h3, :h4, :h5]

  def self.method_missing(methId, **args, &block)
    if not respond_to? methId
      if Tag.include? methId
        define_singleton_method(methId) do |para = {}, &b|
          write "#{para[:front]}" if para[:front]
          write "<#{methId}>\n"
          if not b.nil?
            ret = b.call(self)
            write ret if ret.class == String
          end
          write "</#{methId}>\n"
          write "#{para[:back]}" if para[:back]
          self
        end
        send(methId, args, &block)
      else
        super
      end
    end
  end

  def self.to_html(&block)
    module_eval(&block)
  end
end

Builder.to_html do
  html do
    head.title{"this is html builder\n"}.body do
      write "this is body\n"
      h1 { "ruby meta programe\n" }
      h2 { "test <h2>\n" }
    end
  end
end

