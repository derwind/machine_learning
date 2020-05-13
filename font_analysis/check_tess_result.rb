#! /usr/bin/ruby -Ku

TESS_DATA = "data4tess"

char_hash = {
	"yu"    => "友",
	"jou"   => "情",
	"do"    => "努",
	"ryoku" => "力"
}

order = {
	"ExtraLight" => 0,
	"Light"      => 1,
	"Regular"    => 2,
	"Medium"     => 3,
	"Bold"       => 4,
	"Heavy"      => 5
}

def offset(s)
	default_offset = 20
	if s.size + 2 < default_offset
		" " * (default_offset - (s.size + 2))
	else
		""
	end
end

Dir.glob("#{TESS_DATA}/*.txt").sort{ |a, b|
	a_ = a.split(/_/)
	b_ = b.split(/_/)
	(a_[0] != b_[0]) ? a_[0] <=> b_[0] : order[a_[1]] <=> order[b_[1]]
}.each do |result_path|
	result_name = File.basename(result_path, ".txt").split(/_/)[0 ... -1].join("_")
	expected_char = char_hash[ result_name.split(/_/)[0] ]

	line = nil
	File.open(result_path) { |f|
		begin
			line = f.readline.chomp!
		rescue
		end
	}

	if !line || line.size < 1
		print "[#{result_name}]" + offset(result_name) + "recognition error!\n"
	else
		real_char = line[0]
		if real_char == expected_char
			print "[#{result_name}]" + offset(result_name) + "OK expected char is '#{expected_char}'\n"
		else
			print "[#{result_name}]" + offset(result_name) + "NG '#{real_char}' is got, but expected char is '#{expected_char}'\n"
		end
	end
end
