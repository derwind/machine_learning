#! /usr/bin/ruby -Ku

FONT_DIR = "font"
BG_COLOR = "000000"
FG_COLOR = "ffffff"

class CharJpEn
	attr_reader :jp, :en
	def initialize(jp, en)
		@jp = jp
		@en = en
	end
end

corpus = [
	CharJpEn.new("友", "yu"),
	CharJpEn.new("情", "jou"),
	CharJpEn.new("努", "do"),
	CharJpEn.new("力", "ryoku"),
]

Dir.glob("#{FONT_DIR}/*.otf") do |font_path|
	font_name = File.basename(font_path, ".otf")
	weight = font_name.split(/-/)[1]

	corpus.each do |c|
		tmp_file = "tmp.png"
		output_file = "#{c.en}_#{weight}.png"
		cmd = "hb-view --font-file=#{font_path} --text=#{c.jp} --font-size=256 --background=#{BG_COLOR} --foreground=#{FG_COLOR} --output-format=png --output-file=#{tmp_file}"
		system(cmd)
		# resize
		#cmd = "convert -resize 288x288 #{tmp_file} #{output_file}"
		cmd = "convert -crop 288x288+0+0 #{tmp_file} #{output_file}"
		system(cmd)
	end
end
