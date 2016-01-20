#!/usr/bin/env ruby

def calc(s)
    posfix=[]
    stack=[]
    con=[]
    i=0
    while i<s.length do
        if s[i]==' ' then i+=1; next end
        if '+-*/()'.include?(s[i])
            con << s[i]
            i+=1
        else
            n = s[i...s.length].to_i
            con << n
            i+=n.to_s.length
        end
    end
    con.each do |c|
        if '*/'.include?(c.to_s)
            while not stack.empty? and stack[-1]!='(' and not '+-'.include?stack[-1] do
                posfix << stack.pop
            end
            stack << c
        elsif '+-'.include?(c.to_s)
            while not stack.empty? and stack[-1]!='(' do
                posfix << stack.pop
            end
            stack << c
        elsif c=='('
            stack << c
        elsif c==')'
            op=stack.pop
            while op and op!='(' do
                posfix << op
                op=stack.pop
            end
        else
            posfix << c
        end
    end
    while not stack.empty? do
        posfix<<stack.pop
    end

    p posfix
    stack.clear
    posfix.each do |c|
        if '+-*/'.include?(c.to_s) 
            r=stack.pop;l=stack.pop
            stack.push(l.send(c.to_sym,r)) 
        else
            stack.push(c)
        end
    end
    return stack[0]
end

p calc ARGV[0]

