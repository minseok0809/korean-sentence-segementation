from sentence_segmentation import preprocessing_text

def reading_txt(pro_coprus_file, line_length, data_type):
    
    line_list = []
    line_num = 0
    with open(pro_coprus_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines() 
        for line in lines:
            line_num += 1
            if line_num <= 1:

                if data_type == "source":
                    line_list.append(line)

                elif data_type == "preprocessing":
                    sentences = preprocessing_text(line, pro_coprus_file)
                    for sentence in sentences:
                        line_list.append(sentence) 

    for line in line_list:
        print(line, end="\n\n")