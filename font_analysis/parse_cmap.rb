#! /usr/bin/ruby -Ku

in_def = false
uni_cid_h = {}

while line = gets
	if line =~ /begincidchar/ || line =~ /begincidrange/
		in_def = true
		next
	elsif line =~ /endcidchar/ || line =~ /endcidrange/
		in_def = false
		next
	end

	if in_def
		if line =~ /^\s*<([0-9a-f]+)>\s+(\d+)/
			uni = $1.to_i(16)
			cid = $2.to_i
			uni_cid_h[uni] = cid
		elsif line =~ /^\s*<([0-9a-f]+)>\s+<([0-9a-f]+)>\s+(\d+)/
			uni1 = $1.to_i(16)
			uni2 = $2.to_i(16)
			cid  = $3.to_i

			cid.upto(cid + uni2 - uni1) do |cid_|
				uni = uni1 + (cid_ - cid)
				uni_cid_h[uni] = cid_
			end
		end
	end
end

uni_cid_h.sort { |(uni1,cid1), (uni2,cid2)| cid1 <=> cid2 || uni1 <=> uni2 }.each do |uni,cid|
	print "#{cid} #{uni} (0x#{uni.to_s(16)})\n"
end
