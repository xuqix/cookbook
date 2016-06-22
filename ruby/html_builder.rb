#!/usr/bin/env ruby

require 'fileutils'

module Builder
  @@depth = -1
  @@indent = 0
  @@out = $stdout

  def self.out=(s)
    @@out = s
  end

  def self.write(str, **format)
    depth = @@depth + (format[:depth] or 1)
    @@out << " " * @@indent * depth << str
  end

  Tag = [:html, :head, :title, :body, :h1, :h2, :h3, :h4, :h5]

  def self.method_missing(methId, **args, &block)
    if not respond_to? methId
      if Tag.include? methId
        define_singleton_method(methId) do |para = {}, &b|
          @@depth += 1
          write "#{para[:front]}\n", depth: 0  if para[:front]
          write "<#{methId}>\n", depth: 0
          if not b.nil?
            ret = b.call(self)
            write ret if ret.class == String
          end
          write "</#{methId}>\n", depth: 0
          write "#{para[:back]}\n", depth: 0 if para[:back]
          @@depth -= 1
          self
        end
        send(methId, args, &block)
      else
        super
      end
    end
  end

  def self.to_html(**format, &block)
    @@indent = format[:indent] or 0
    @@depth = -1
    module_eval(&block)
  end
end

Builder.to_html indent: 2 do
  html do
    head.title{"this is html builder\n"}.body do
      write "this is body\n"
      h1 { "ruby meta programe\n" }
      h2 { "test hhhhh\n" }
    end
  end
end

