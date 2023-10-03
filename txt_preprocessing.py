import ray
import time
import argparse
import pandas as pd
from tqdm import tqdm
from itertools import chain
from sentence_segmentation import preprocessing_text
from data_preprocessing import make_topic_pro_post_txt_file_name_list
 
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_cpus', type=int, default=4)
    parser.add_argument('--pro_post_xlsx_path', type=str, default='pro_post_xlsx_path')
    parser.add_argument('--start_index', type=int, default=0)
    args = parser.parse_args('')   

    pro_post_xlsx_path = args.pro_post_xlsx_path
    start_index = args.start_index

    ray.init(num_cpus = args.num_cpus)

    @ray.remote
    def ray_preprocessing_text(source, corpus_path):

        preprocessing_sentence_list = preprocessing_text(source, corpus_path)

        return preprocessing_sentence_list
    

    def preprocessing_corpus_txt(pro_post_xlsx_path, start_index):

        pro_post_total_corpus_path_df = pd.read_excel(pro_post_xlsx_path, engine='openpyxl')
        pro_total_corpus_path_list = pro_post_total_corpus_path_df['Pro'].values.tolist()
        post_total_corpus_path_list = pro_post_total_corpus_path_df['Post'].values.tolist()

        progress_length = len(pro_total_corpus_path_list[start_index:])   
        print("[Size]")
        print("The number of preprocessing corpus: " + str(progress_length))
        print("\n[Order]")
        pbar = tqdm(range(progress_length))
        num = 0
        process_num = 10    

        for pro, post in zip(pro_total_corpus_path_list[start_index:], post_total_corpus_path_list[start_index:]):

            sentence_list = []

            with open(pro, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines() 
                nested_lines_num = len(lines) // process_num
                for i in range(nested_lines_num - 1):
                    start_line = process_num * i
                    end_line = process_num * (i+1)
                    futures = [ray_preprocessing_text.remote(lines[start_line:end_line][j], pro) for j in range(process_num)]
                    results = ray.get(futures)

                    if i == nested_lines_num - 2:
                        futures = [ray_preprocessing_text.remote(lines[end_line:][j], pro) for j in range(len(lines) - end_line)]
                        results = ray.get(futures)

                    sentences = list(chain.from_iterable(results))
                    sentence_list.append(sentences)

            sentence_list = list(chain.from_iterable(sentence_list))
            
            with open(post, 'a', encoding='utf-8') as fp:
                fp.write("\n".join(sentence_list))

            pbar.n += 1
            pbar.refresh()
            time.sleep(0.01)

        pbar.close() 

        
    preprocessing_corpus_txt(pro_post_xlsx_path, start_index)

if __name__ == '__main__':
    main()    



