def card_parse(input):
    if (input[0] == ';'): 
    	student_pid = input[2:11] # magnetic-strip card swiper's rules
        return student_pid
    # else parse with barcode parser's rules 
