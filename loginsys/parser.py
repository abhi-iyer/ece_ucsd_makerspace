def card_parse(input):
	if (input[0] == ';'):
		# magnetic-strip card swiper's rules
		student_pid = input[2:11]
		return student_pid
		
	# else parse with barcode parser's rules 
