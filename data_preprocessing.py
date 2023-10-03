import os
import re
import tqdm
import glob
import json
import time
import inspect
import pandas as pd
from extract_source_text import make_sources

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


def make_train_valid_json_txt_file_path_list(json_path_list, txt_path_list, corpus_name):

    train_json_file_path, valid_json_file_path = train_valid_json_file_path_list(json_path_list)
    
    the_number_of_train_json_file  = len(train_json_file_path)
    the_number_of_valid_json_file  = len(valid_json_file_path)
    the_number_of_json_file = the_number_of_train_json_file + the_number_of_valid_json_file
    print("The number of train json file:", the_number_of_train_json_file)
    print("The number of valid json file:", the_number_of_valid_json_file)
    print("The number of json file:", the_number_of_json_file)
    
    train_txt_file_path = txt_file_path_list(train_json_file_path, txt_path_list[0])
    valid_txt_file_path = txt_file_path_list(valid_json_file_path, txt_path_list[1])

    source_file_index_df = pd.DataFrame(train_json_file_path, columns=['source_file_path'])
    source_file_index_df.to_excel("source_file_index/" + corpus_name + "_source_train_file_index.xlsx", index=False)

    source_file_index_df = pd.DataFrame(valid_json_file_path, columns=['source_file_path'])
    source_file_index_df.to_excel("source_file_index/" + corpus_name + "_source_valid_file_index.xlsx", index=False)

    return train_json_file_path, valid_json_file_path, train_txt_file_path, valid_txt_file_path


def make_json_txt_file_path_list(json_path_list, txt_path_list, corpus_name):

    json_file_path = json_file_path_list(json_path_list)
    
    the_number_of_json_file = len(json_file_path) 
    print("The number of json file:", the_number_of_json_file)
    
    text_file_path_list = txt_file_path_list(json_file_path, txt_path_list[0])

    source_file_index_df = pd.DataFrame(json_file_path, columns=['source_file_path'])
    source_file_index_df.to_excel("source_file_index/" + corpus_name + "_source_file_index.xlsx", index=False)

    return json_file_path, text_file_path_list


def make_topic_json_txt_file_path_list(json_folder_list, topic_name_list, txt_path_list, corpus_name):

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

            # train_file_list_variable = "train_json_file_path_list_" + topic_index
            # txt_file_path_list_variable = "train_txt_file_path_list_" + topic_index        
            train_topic_json_list.append(the_number_of_train_topic_json_file)    
            # globals()[train_file_list_variable] = train_file_path
            # globals()[txt_file_path_list_variable] = txt_file_path_list(train_file_path, 
                                                                        # txt_path_list[0] + topic_name_list[i] + "_train_") 
            train_txt_file_path = txt_file_path_list(train_file_path, 
                                               txt_path_list[0] + topic_name_list[i] + "_train_")   
            source_file_index_df = pd.DataFrame({'source_file_path': train_file_path, 
                                                 'txt_file_path': train_txt_file_path})
            source_file_index_df.to_excel("source_file_index/" + corpus_name + "_train" + "_source_file_index.xlsx", index=False)


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

            # valid_file_list_variable = "valid_json_file_path_list_" + topic_index
            # txt_file_path_list_variable = "valid_txt_file_path_list_" + topic_index 
            valid_topic_json_list.append(the_number_of_valid_topic_json_file)    
            # globals()[train_file_list_variable] = valid_file_path
            # globals()[txt_file_path_list_variable] = txt_file_path_list(valid_file_path, 
                                                                        # txt_path_list[1] + topic_name_list[i - (len(json_path_list)) // 2] + "_valid_")
            valid_txt_file_path = txt_file_path_list(valid_file_path, 
                                               txt_path_list[0] + topic_name_list[i] + "_valid_")   
            source_file_index_df = pd.DataFrame({'source_file_path': valid_file_path, 
                                                 'txt_file_path': valid_txt_file_path})
            source_file_index_df.to_excel("source_file_index/" + corpus_name + "_valid" + "_source_file_index.xlsx", index=False)

         
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


def make_pro_post_txt_file_path_list(pro_corpus_path, pro_post_xlsx_path):
    
    pro_total_corpus_path_list = glob.glob(pro_corpus_path)
    pro_total_corpus_path_list = sorted_list(pro_total_corpus_path_list)
    post_total_corpus_path_list = post_txt_file_path_list(pro_total_corpus_path_list)
    pro_post_total_corpus_path_df = pd.DataFrame({'Pro': pro_total_corpus_path_list, 'Post': post_total_corpus_path_list})
    pro_post_total_corpus_path_df.to_excel(pro_post_xlsx_path, index=False)

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

        # pro_total_corpus_path_list_variable = "pro_total_corpus_path_list_" + "train_" + topic_index
        # post_total_corpus_path_list_variable = "post_total_corpus_path_list_" + "train_" + topic_index
            
        # globals()[pro_total_corpus_path_list_variable] = pro_total_corpus_path_list
        # globals()[post_total_corpus_path_list_variable] = post_total_corpus_path_list
        
        if 'summary_and_report_generation_data' in pro_corpus_name:
            pro_post_total_corpus_path_df = pd.DataFrame({'Pro': pro_total_corpus_path_list, 'Post': post_total_corpus_path_list})
            pro_post_xlsx_path = "pro_post_corpus_path/summary_and_report_generation_data_" + "train_" + topic_index + ".xlsx"
            pro_post_total_corpus_path_df.to_excel(pro_post_xlsx_path, index=False)

        if 'web_data_based_korean_corpus_data' in pro_corpus_name:
            pro_post_total_corpus_path_df = pd.DataFrame({'Pro': pro_total_corpus_path_list, 'Post': post_total_corpus_path_list})
            pro_post_xlsx_path = "pro_post_corpus_path/web_data_based_korean_corpus_data_" + "train_" + topic_index + ".xlsx"
            pro_post_total_corpus_path_df.to_excel(pro_post_xlsx_path, index=False)

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

        # pro_total_corpus_path_list_variable = "pro_total_corpus_path_list_" + "valid_" + topic_index
        # post_total_corpus_path_list_variable = "post_total_corpus_path_list_" + "valid_" + topic_index
            
        # globals()[pro_total_corpus_path_list_variable] = pro_total_corpus_path_list
        # globals()[post_total_corpus_path_list_variable] = post_total_corpus_path_list

        if 'summary_and_report_generation_data' in pro_corpus_name:
            pro_post_total_corpus_path_df = pd.DataFrame({'Pro': pro_total_corpus_path_list, 'Post': post_total_corpus_path_list})
            pro_post_xlsx_path = "pro_post_corpus_path/summary_and_report_generation_data_" + "valid_" + topic_index + ".xlsx"
            pro_post_total_corpus_path_df.to_excel(pro_post_xlsx_path, index=False)

        if 'web_data_based_korean_corpus_data' in pro_corpus_name:
            pro_post_total_corpus_path_df = pd.DataFrame({'Pro': pro_total_corpus_path_list, 'Post': post_total_corpus_path_list})
            pro_post_xlsx_path = "pro_post_corpus_path/web_data_based_korean_corpus_data_" + "valid_" + topic_index + ".xlsx"
            pro_post_total_corpus_path_df.to_excel(pro_post_xlsx_path, index=False)


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


def count_number_of_txt_file_with_batch_list(source_file_list, batch_size, corpus_name):

    corpus_type1 = ["summary_and_report_generation_data",
                    "web_data_based_korean_corpus_data"]

    corpus_type2 = ["legal_regulations_(such_as_terms_and_conditions_of_judgment)_text_analysis_data",
                    "summary_of_book_materials"]

    corpus_type3 = ['automatic_patent_classification',
                    'british_korean_data_on_patents_in_major_countries_linked_to_industrial_information',
                    'machine_reading_data_for_administrative_documents',
                    'professional_corpus',
                    'summary_of_thesis_materials',
                    'document_summary_text', 'general_common_sense', 'machine_reading', 
                    'news_article_machine_reading_data', 'reading_books_by_machine',
                    'korean_corpus_data_based_on_large_scale_purchase_books']
    
    source_file_by_batch_df = pd.DataFrame({'File':[0], 'Length of Source List':[0],
                                            'The Number of TXT File':[0], 
                                            'Description':[0]})
    
    if any(corpus in corpus_name for corpus in corpus_type1):
        the_number_of_total_txt_file = 0
        the_number_of_txt_file_list = []
        source_list = []
        
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        name = string[string.find('(') + 1:-1].split(',')[0]
        file_name_number = re.findall(r'\d+', name)[0]

        for i in range(len(source_file_list)):    
            
            source_file = source_file_list[i]   
                
            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file) 

            sources = make_sources(one_json_sample)
            for source in sources:
                source_list.append(source[0])
                
            the_number_of_txt_file = 1

            if len(source_list) >= batch_size:
                source_file_by_batch_df.loc[i] = [source_file,
                                                len(source_list), the_number_of_txt_file, ""]
                
            elif len(source_list) < batch_size:
                source_file_by_batch_df.loc[i] = [source_file,
                                                len(source_list), the_number_of_txt_file,
                                                "not subject of batch. small source list."]
                
            the_number_of_txt_file_list.append(len(source_list))
            the_number_of_total_txt_file += len(source_list) 
            source_list = []

        the_number_of_total_txt_file = the_number_of_total_txt_file // batch_size                 
        print("Batch Size:", batch_size)
        print("The number of txt file:", the_number_of_total_txt_file)

        source_file_by_batch_df = source_file_by_batch_df.astype({'Length of Source List':'int', 
                                                                'The Number of txt File':'int'})
        
        if 'rain' in source_file:
            train_file = "source_file_by_batch/summary_and_report_generation_data_train_" + file_name_number + ".xlsx"
            source_file_by_batch_df.to_excel(train_file, index=False)

        elif 'alid' in source_file:
            valid_file = "source_file_by_batch/summary_and_report_generation_data_valid_" + file_name_number + ".xlsx"
            source_file_by_batch_df.to_excel(valid_file, index=False)

        else:
            plain_file = "source_file_by_batch/summary_and_report_generation_data_" + file_name_number + ".xlsx"
            source_file_by_batch_df.to_excel(plain_file, index=False)


    elif any(corpus in corpus_name for corpus in corpus_type2):
        the_number_of_total_txt_file = 0
        the_number_of_txt_file_list = []
        source_list = []
        
        for i in range(len(source_file_list)):    
            
            source_file = source_file_list[i]   
                
            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file) 

            sources = make_sources(source_file, one_json_sample)
            for source in sources:
                source_list.append(source[0])
                
            the_number_of_txt_file = 1

            if len(source_list) >= batch_size:
                source_file_by_batch_df.loc[i] = [source_file,
                                                len(source_list), the_number_of_txt_file, ""]
                
            elif len(source_list) < batch_size:
                source_file_by_batch_df.loc[i] = [source_file,
                                                len(source_list), the_number_of_txt_file,
                                                "not subject of batch. small source list."]
                
            the_number_of_txt_file_list.append(len(source_list))
            the_number_of_total_txt_file += len(source_list) 
            source_list = []

        the_number_of_total_txt_file = the_number_of_total_txt_file // batch_size                 
        source_file_by_batch_df = source_file_by_batch_df.astype({'Length of Source List':'int', 
                                                                'The Number of txt File':'int'})
        
        print("Batch Size:", batch_size)
        print("The number of txt file:", the_number_of_total_txt_file)
    
        if 'rain' in source_file:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + "_train.xlsx", index=False)
        elif 'alid' in source_file:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + "_valid.xlsx", index=False)
        else:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + ".xlsx", index=False)
        
     
    elif any(corpus in corpus_name for corpus in corpus_type3):
        the_number_of_total_txt_file = 0
        the_number_of_txt_file_list = []
        
        for i in range(len(source_file_list)):    
            
            source_file = source_file_list[i]        

            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file) 

            try:
                source_list = make_sources(one_json_sample)
                
                the_number_of_txt_file = ((len(source_list) // batch_size) + 1) 

                if len(source_list) >= batch_size:
                    source_file_by_batch_df.loc[i] = [source_file,
                                                    len(source_list), the_number_of_txt_file, ""]
                    the_number_of_txt_file_list.append(the_number_of_txt_file)
                    the_number_of_total_txt_file  += the_number_of_txt_file

                elif len(source_list) < batch_size:
                    source_file_by_batch_df.loc[i] = [source_file,
                                                    len(source_list), the_number_of_txt_file,
                                                    "not subject of batch. small source list."]
                    the_number_of_txt_file_list.append(1)
                    the_number_of_total_txt_file  += 1
            except:
                pass  

        print("Batch Size:", batch_size)
        print("The number of txt file:", the_number_of_total_txt_file)
    
        if 'rain' in source_file:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + "_train.xlsx", index=False)
        elif 'alid' in source_file:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + "_valid.xlsx", index=False)
        else:
            source_file_by_batch_df.to_excel("source_file_by_batch/" + corpus_name + ".xlsx", index=False)

    return the_number_of_total_txt_file, the_number_of_txt_file_list



def write_jsontext_to_txt_file_with_batch_list(source_file_list, text_file_path_list,
                                               batch_size, the_number_of_txt_file_list, corpus_name):

    corpus_type1 = ['automatic_patent_classification_data',
                    'british_korean_data_on_patents_in_major_countries_linked_to_industrial_information',
                    'document_summary_text', 
                    'korean_corpus_data_based_on_large_scale_purchase_books',
                    'machine_reading',
                    'news_article_machine_reading_data',
                    'reading_books_by_machine',
                    'summary_of_thesis_materials',
                    'web_data_based_korean_corpus_data']

    corpus_type2 = ['legal_regulations_(such_as_terms_and_conditions_of_judgment)_text_analysis_data',
                    'summary_and_report_generation_data',
                    'summary_of_book_materials']

    corpus_type3 = ['general_common_sense']

    corpus_type4 = ['machine_reading_data_for_administrative_documents']

    corpus_type5 = ['professional_corpus']


    progress_length = sum(the_number_of_txt_file_list)
    print("[Size]")
    print("The number of preprocessing corpus: " + str(progress_length))
    print("\n[Order]")
    pbar = tqdm(range(progress_length))
    num = 0

    if any(corpus in corpus_name for corpus in corpus_type1):
        for i in range(len(source_file_list)):

            source_file = source_file_list[i]
            
            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file)

            try:  
                source_list = make_sources(one_json_sample)
                
                n = batch_size
                source_batch_list = list(divide_source_file_list(source_list, n))
                
                for source_list in source_batch_list:   
                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + ".txt"), "a", encoding='utf-8') as fp:
                        fp.write("\n".join(source_list))           
                    num += 1  
                    pbar.n += 1
                    pbar.refresh()
                    time.sleep(0.01) 
            except:
                pass


    elif any(corpus in corpus_name for corpus in corpus_type2):
        for i in range(len(source_file_list)):

            source_file = source_file_list[i]
                
            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file)
            
            sources = make_sources(source_file, one_json_sample)

            if len(source_list) >= batch_size:
                with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + ".txt"), "a", encoding='utf-8') as fp:        
                    fp.write("\n".join(source_list)) 
                pbar.n += 1
                pbar.refresh()
                time.sleep(0.01)  
        
                source_list = []
                
            elif i == (len(source_file_list) -1): 
                for source in sources:
                    source_list.append(source)
                
                with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + ".txt"), "a", encoding='utf-8') as fp:        
                    fp.write("\n".join(source_list[0])) 
                num += 1  
                pbar.n += 1
                pbar.refresh()
                time.sleep(0.01)
                            
            for source in sources:
                source_list.append(source[0])   


    elif any(corpus in corpus_name for corpus in corpus_type3):
        for i in range(len(source_file_list)):

            source_file = source_file_list[i]     

            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file)

            if 'ko_wiki_v1_squad' in source_file:
                source_list = make_sources(source_file, one_json_sample)
                
                n = batch_size
                source_batch_list = list(divide_source_file_list(source_list, n))
                    
                for source_list in source_batch_list:
                    num += 1
                    print(str(num), end=" ")  
                    
                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + ".txt"), "a", encoding='utf-8') as fp:        
                        fp.write("\n".join(source_list))   
                    
        else:
            source_list = make_sources(source_file, one_json_sample)

            n = batch_size
            source_batch_list = list(divide_source_file_list(source_list, n))
            
            for source_list in source_batch_list:
        
                with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + ".txt"), "a", encoding='utf-8') as fp:        
                    fp.write("\n".join(source_list))    
                num += 1  
                pbar.n += 1
                pbar.refresh()
                time.sleep(0.01)      




    elif any(corpus in corpus_name for corpus in corpus_type4):
        for i in range(len(source_file_list)):

            source_file = source_file_list[i]
            
            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file)
            
            source_list = make_sources(one_json_sample)
            
            n = batch_size
            source_batch_list = list(divide_source_file_list(source_list, n))
            
            for source_list in source_batch_list:
                
                if 'tableqa' in source_file:

                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + "_tableqa.txt"), "a", encoding='utf-8') as fp:        
                        fp.write("\n".join(source_list))   
                    num += 1  
                    pbar.n += 1
                    pbar.refresh()
                    time.sleep(0.01)
        
                else:

                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + ".txt"), "a", encoding='utf-8') as fp:        
                        fp.write("\n".join(source_list))   

                    num += 1  
                    pbar.n += 1
                    pbar.refresh()
                    time.sleep(0.01)


    elif any(corpus in corpus_name for corpus in corpus_type5):

        for i in range(len(source_file_list)):

            source_file = source_file_list[i]

            with open(source_file, 'r', encoding='utf-8') as one_json_file:
                one_json_sample = json.load(one_json_file)

            source_list = make_sources(source_file, one_json_sample)
            
            n = batch_size
            source_batch_list = list(divide_source_file_list(source_list, n))
            
            for source_list in source_batch_list:
                num += 1
                print(str(num), end=" ")  
            
                if '법령' in source_file or '판례' in source_file:
                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + "_legal_text.txt"), "a", encoding='utf-8') as fp:        
                        fp.write("\n".join(source_list))   
                    num += 1  
                    pbar.n += 1
                    pbar.refresh()
                    time.sleep(0.01)  

                else:
                    with open(os.path.join('AIHUB_corpus/' + text_file_path_list[i][:-4] + "_" + str(num) + ".txt"), "a", encoding='utf-8') as fp:        
                        fp.write("\n".join(source_list))   
                    num += 1  
                    pbar.n += 1
                    pbar.refresh()
                    time.sleep(0.01)  

    pbar.close()         