#! /usr/bin/ruby -Ku

TESS_DATA = "data4tess"

Dir.glob("#{TESS_DATA}/*.png") do |img_path|
	img_name = File.basename(img_path, ".png")

	output_file = "#{TESS_DATA}/#{img_name}_result"
	cmd = "tesseract #{img_path} #{output_file} -l jpn"
	system(cmd)
end
