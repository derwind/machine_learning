#! /usr/bin/ruby -Ku

TESS_DATA = "data"
RESULT_DIR = "result"

Dir.glob("#{TESS_DATA}/*.png") do |img_path|
	img_name = File.basename(img_path, ".png")

	output_file = "#{RESULT_DIR}/#{img_name}_result"
	cmd = "tesseract #{img_path} #{output_file} -l jpn -psm 6 japan.config"
	system(cmd)
end
