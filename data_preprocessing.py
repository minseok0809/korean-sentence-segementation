import glob
import pandas as pd

def sorted_list(path_list):
    
    path_list = sorted(path_list, reverse=False)
    path_list = sorted(path_list, key=len)
    
    return path_list

def divide_source_file_list(l, n): 
    
  for i in range(0, len(l), n): 
    yield l[i:i + n] 

def json_file_path_list(path_list):
    
    json_file_path  = [glob.glob(i, recursive = True) for i in path_list][0]
    json_file_path = sorted_list(json_file_path)
    
    return json_file_path    

def train_valid_json_file_path_list(path_list):

  train_json_file_path, valid_json_file_path = [glob.glob(i, recursive = True) if 'rain' in i
                                      else glob.glob(i, recursive = True)
                                      for i in path_list]

  train_json_file_path = sorted_list(train_json_file_path)
  valid_json_file_path = sorted_list(valid_json_file_path)
    
  return train_json_file_path, valid_json_file_path

def txt_file_path_list(file_path, folder_corpus_type_path):
  
  txt_file_path = [folder_corpus_type_path + str(i) + ".txt"
                              for i in range(len(file_path))]
    
  return txt_file_path

def make_train_valid_json_txt_file_path_list(json_path_list, txt_path_list):

    train_json_file_path, valid_json_file_path = train_valid_json_file_path_list(json_path_list)
    
    the_number_of_train_json_file  = len(train_json_file_path)
    the_number_of_valid_json_file  = len(valid_json_file_path)
    the_number_of_json_file = the_number_of_train_json_file + the_number_of_valid_json_file
    print("The number of train json file:", the_number_of_train_json_file)
    print("The number of valid json file:", the_number_of_valid_json_file)
    print("The number of json file:", the_number_of_json_file)
    
    train_txt_file_path = txt_file_path_list(train_json_file_path, txt_path_list[0])
    valid_txt_file_path = txt_file_path_list(valid_json_file_path, txt_path_list[1])

    return train_json_file_path, valid_json_file_path, train_txt_file_path, valid_txt_file_path


def make_json_txt_file_path_list(json_path_list, txt_path_list):

    json_file_path = json_file_path_list(json_path_list)
    
    the_number_of_json_file = len(json_file_path) 
    print("The number of json file:", the_number_of_json_file)
    
    text_file_path_list = txt_file_path_list(json_file_path, txt_path_list[0])

    return json_file_path, text_file_path_list


def make_topic_json_txt_file_path_list(json_folder_list, topic_name_list, txt_path_list):

    # summary_and_report_generation_data
    # web_data_based_korean_corpus_data

    json_path_list = []
    train_topic_json_list = []
    valid_topic_json_list = []
    the_number_of_train_file = 0
    the_number_of_valid_file = 0
    the_number_of_file = 0
    the_numer_of_txt_file = 0
    
    for json_folder in json_folder_list:
        for topic_name in topic_name_list:
            json_path_list.append(json_folder + topic_name + '/**/*.json')

    for i in range(len(json_path_list)):
        
        json_path = json_path_list[i]
        
        if 'train'[1:] in json_path:
            train_file_path = glob.glob(json_path, recursive = True) 
            the_number_of_train_topic_json_file = len(train_file_path)
            the_number_of_train_file += len(train_file_path)
            the_number_of_file += len(train_file_path)
            
            if i < 9:
                topic_index = "0" + str(i + 1)
                
            elif i >= 9:
                topic_index = str(i + 1)

            train_file_list_variable = "train_json_file_list_" + topic_index
            txt_file_path_list_variable = "train_txt_file_path_list_" + topic_index        
            train_topic_json_list.append(the_number_of_train_topic_json_file)    
            globals()[train_file_list_variable] = train_file_path
            globals()[txt_file_path_list_variable] = txt_file_path_list(train_file_path, 
                                                                        txt_path_list[0] + topic_name_list[i] + "_train_")   


        elif 'valid'[1:] in json_path:
            valid_file_path = glob.glob(json_path, recursive = True)
            the_number_of_valid_topic_json_file = len(valid_file_path)
            the_number_of_valid_file += len(valid_file_path) 
            the_number_of_file += len(valid_file_path)
            
            if '요약문 및 레포트 생성 데이터' in json_path:
                if i - 10 < 9:
                    topic_index = "0" + str(i + 1 - 10)
                    
                elif i - 10>= 9:
                    topic_index = str(i + 1 - 10)
            
            elif '웹데이터 기반 한국어 말뭉치 데이터' in json_path:
                if i - 17 < 9:
                    topic_index = "0" + str(i + 1 - 17)
                    
                elif i - 17 >= 9:
                    topic_index = str(i + 1 - 17)

            valid_file_list_variable = "valid_json_file_list_" + topic_index
            txt_file_path_list_variable = "valid_txt_file_path_list_" + topic_index
            valid_topic_json_list.append(the_number_of_valid_topic_json_file)  
            globals()[valid_file_list_variable] = valid_file_path
            globals()[txt_file_path_list_variable] = txt_file_path_list(valid_file_path, 
                                                                        txt_path_list[1] + topic_name_list[i - (len(json_path_list)) // 2] + "_valid_")  
            
    the_number_of_topic_json_file_df = pd.DataFrame({'Topic':topic_name_list,
                                                     'The number of train topic json file':train_topic_json_list,
                                                     'The number of valid topic json file':valid_topic_json_list})

    the_number_of_topic_json_file_df.loc['Total', : ] = the_number_of_topic_json_file_df.loc[topic_name_list[0]:topic_name_list[-1], :].sum(axis=0)
    the_number_of_topic_json_file_df.loc[:, 'Total'] = the_number_of_topic_json_file_df.loc[:, 'The number of train topic json file':'The number of valid topic json file'].sum(axis=1)

    print()
    print("The number of train json file: ", the_number_of_train_file)  
    print("The number of valid json file: ", the_number_of_valid_file)  
    print("The number of json file: ", the_number_of_file)  

    return the_number_of_topic_json_file_df

def post_txt_file_path_list(corpus_path_list):
   
  post_corpus_path_list = [corpus_file.replace("pro", "post")
                      for corpus_file in corpus_path_list]

  return post_corpus_path_list


def make_pro_post_txt_file_path_list(pro_corpus_path):
    
    pro_total_corpus_path_list = glob.glob(pro_corpus_path)
    pro_total_corpus_path_list = sorted_list(pro_total_corpus_path_list)
    post_total_corpus_path_list = post_txt_file_path_list(pro_total_corpus_path_list)

    return pro_total_corpus_path_list, post_total_corpus_path_list

def make_topic_pro_post_txt_file_name_list(pro_corpus_name, topic_name_list):

    # summary_and_report_generation_data
    # web_data_based_korean_corpus_data

    for i in range(len(topic_name_list)):

        pro_total_corpus_path_list = sorted_list(glob.glob(pro_corpus_name + topic_name_list[i] + "_train" + "*.txt"))
        post_total_corpus_path_list = post_txt_file_path_list(pro_total_corpus_path_list)
        
        if i < 9:
            topic_index = "0" + str(i + 1)
        
        elif i >= 9:
            topic_index = str(i + 1)

        pro_total_corpus_path_list_variable = "pro_total_corpus_path_list_" + "train_" + topic_index
        post_total_corpus_path_list_variable = "post_total_corpus_path_list_" + "train_" + topic_index
            
        globals()[pro_total_corpus_path_list_variable] = pro_total_corpus_path_list
        globals()[post_total_corpus_path_list_variable] = post_total_corpus_path_list
            
            
        pro_total_corpus_path_list = sorted_list(glob.glob(pro_corpus_name + topic_name_list[i] + "_valid" + "*.txt"))
        post_total_corpus_path_list = post_txt_file_path_list(pro_total_corpus_path_list)
        
        if 'summary_and_report_generation_data' in pro_corpus_name:
            if i - 10 < 9:
                topic_index = "0" + str(i + 1 - 10)
            
            elif i - 10 >= 9:
                topic_index = str(i + 1 - 10)

        elif 'web_data_based_korean_corpus_data' in pro_corpus_name:
            if i - 17 < 9:
                topic_index = "0" + str(i + 1 - 17)
            
            elif i - 17 >= 9:
                topic_index = str(i + 1 - 17)

        pro_total_corpus_path_list_variable = "pro_total_corpus_path_list_" + "valid_" + topic_index
        post_total_corpus_path_list_variable = "post_total_corpus_path_list_" + "valid_" + topic_index
            
        globals()[pro_total_corpus_path_list_variable] = pro_total_corpus_path_list
        globals()[post_total_corpus_path_list_variable] = post_total_corpus_path_list


def merge_and_deduplicate_corpus_txt(preprocessing_corpus_path, merge_corpus_path,
                                      deduplicate_corpus_path):
    
    corpus_list = glob.glob(preprocessing_corpus_path)
    corpus_list = sorted_list(corpus_list)
    
    with open(merge_corpus_path, 'w', encoding='utf-8') as f:
        for corpus in corpus_list:
            with open(corpus, encoding='utf-8') as text:
                for line in text:
                    f.write(line)
                    
    with open(deduplicate_corpus_path, 'w', encoding='utf-8') as f1:
        with open(merge_corpus_path, encoding='utf-8') as f2:
            lines = f2.read().splitlines()
            single_sentence_dict = dict.fromkeys(lines)
            single_sentence_list = list(single_sentence_dict)
            f1.write("\n".join(single_sentence_list))        

def merge_and_deduplicate_topic_corpus_txt(preprocessing_corpus_path, merge_corpus_path,
                                           deduplicate_corpus_path, topic_name_list):

    # summary_and_report_generation_data
    # web_data_based_korean_corpus_data

    corpus_list = glob(preprocessing_corpus_path)
    corpus_list = sorted_list(corpus_list)
    
    merge_corpus_list = glob(merge_corpus_path + "*.txt")
    
    for i in range(len(topic_name_list)):
        with open(merge_corpus_path + topic_name_list[i] + '.txt', 'w', encoding='utf-8') as f:
            topic_corpus_list_with_none = [j if topic_name_list[i] in j else None for j in corpus_list]
            topic_corpus_list = list(filter(None, topic_corpus_list))
            for corpus in topic_corpus_list:
                with open(corpus, encoding='utf-8') as text:
                    for line in text:
                        f.write(line)
                    
    with open(deduplicate_corpus_path, 'w', encoding='utf-8') as f1:
        for corpus in merge_corpus_list:
            with open(corpus, encoding='utf-8') as f2:
                lines = f2.read().splitlines()
                single_sentence_dict = dict.fromkeys(lines)
                single_sentence_list = list(single_sentence_dict)
                f1.write("\n".join(single_sentence_list))                                 
                     