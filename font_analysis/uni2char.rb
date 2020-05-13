#! /usr/bin/ruby -Ku

while line = gets
	line.chomp!
	cid, uni = line.split(/\s+/).map { |n| n.to_i }
	char = [uni].pack("U*")
	print "#{uni} #{char}\n"
end
