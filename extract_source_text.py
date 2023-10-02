import pandas as pd




def make_sources(json_sample, source_file):

            
    corpus_type1 = ['machine_reading_data_for_administrative_documents', 'machine_reading_pro']

    if 'automatic_patent_classification' in source_file:
        sources = list(pd.DataFrame(json_sample['dataset'])['abstract'].dropna())


    elif 'british_korean_data_on_patents_in_major_countries_linked_to_industrial_information' in source_file:
        sources = list(pd.DataFrame(json_sample['labeled_data'])['astrt_cont_kor'])


    elif 'document_summary_text' in source_file:
        source_df = pd.DataFrame(json_sample['documents'])
        source_dict = dict(source_df['text'].explode())
        source_json = pd.json_normalize(source_dict)  

        sources = []
        for source_index in source_json:
            for source_nested_list in source_json[source_index]:
                for source_single_list in source_nested_list:
                    source_sentence = ""
                    for source_single in source_single_list:
                        if type(source_single) == dict:
                            for key, value in source_single.items():
                                if key == "sentence":
                                    source_sentence += " " + value
                    if len(source_sentence) > 0:
                        sources.append(source_sentence)

    elif 'general_common_sense' in source_file: 
        if 'ko_wiki_v1_squad' in source_file:
            source_df = pd.DataFrame(json_sample['data'])
            source_dict = dict(source_df['paragraphs'].explode())
            source_json = pd.json_normalize(source_dict)
            sources = list(source_json.filter(regex='context').values[0])
            
        else:
            sources = (pd.DataFrame(json_sample['sentence'])['text'])

    elif 'korean_corpus_data_based_on_large_scale_purchase_books' in source_file:        
        source_df = pd.DataFrame(json_sample['paragraphs'])
        source_dict = dict(source_df['sentences'].explode())
        source_json = pd.json_normalize(source_dict)  
        
        sources = []
        for source_index in source_json:
            for source_nested_list in source_json[source_index]:

                try:
                    for source_single_list in source_nested_list:
                        try:
                            for key, value in source_single_list.items():
                                if key == 'text':
                                    sources.append(value)
                        except:
                            pass
                except:
                    pass 

    elif 'legal_regulations_(such_as_terms_and_conditions_of_judgment)_text_analysis_data' in source_file:   
        if '판결문' in source_file:
            source_df = pd.DataFrame(json_sample)
            sources = source_df.loc['disposalcontent']['disposal'] + \
                source_df.loc['rqestObjet']['mentionedItems'] + \
                source_df.loc['acusrAssrs']['assrs'] + \
                source_df.loc['dedatAssrs']['assrs'] + \
                source_df.loc['bsisFacts']['facts'] + \
                source_df.loc['courtDcss']['dcss'] + \
                source_df.loc['cnclsns']['close']

        elif '유리' in source_file:
            source_df = pd.DataFrame.from_dict(json_sample, orient='index')
            source_df = source_df.transpose()
            sources = [source_df['clauseArticle'][0], source_df['comProvision'][0]]

        elif '불리' in source_file:
            source_df = pd.DataFrame.from_dict(json_sample, orient='index')
            source_df = source_df.transpose()
            sources = [source_df['clauseArticle'][0][0], source_df['illdcssBasiss'][0][0],
                            source_df['relateLaword'][0][0]]

    elif any(corpus in source_file for corpus in corpus_type1): 
        source_df = pd.DataFrame(json_sample['data'])
        source_dict = dict(source_df['paragraphs'].explode())
        source_json = pd.json_normalize(source_dict)
        sources = list(source_json.filter(regex='context').values[0])

    elif 'professional_corpus' in source_file: 
       
        if '논문_' in source_file:
            sources = list(pd.DataFrame(json_sample['data'])['text'])
            
        elif '특허_z' in source_file:
            source_df = pd.DataFrame(json_sample['data'])
            sources = list(source_df[source_df['attr'] == 'abs']['text'])

        elif '특허_0' in source_file or '특허_1' in source_file:
            source_df = pd.DataFrame(json_sample['data'])
            source_dict = dict(source_df[source_df['attr'] == '초록']['sentence'].explode())
            source_json = pd.json_normalize(source_dict)
            sources = list(source_json.filter(regex='text').values[0])

        elif '법령' in source_file or '판례' in source_file:
            source_df = pd.DataFrame(json_sample['data'])
            source_dict = dict(source_df['sentence'].explode())
            source_json = pd.json_normalize(source_dict)
            sources = list(source_json.filter(regex='text').values[0])

    elif 'reading_books_by_machine' in source_file: 

        source_df = pd.DataFrame(json_sample['data'])
        source_dict = dict(source_df['paragraphs'].explode())
        source_json = pd.json_normalize(source_dict)
        sources = list(source_json.filter(regex='context').values[0])

        source_filter_02 = source_json.filter(regex='[0123456789]').values[0]
        source_df_02 = pd.DataFrame(source_filter_02)
        
        for source_df_02_value in source_df_02.values:
            for value in source_df_02_value[0]:
                try:
                    sources.append(value['context'])
                except:
                    pass

    elif 'summary_and_report_generation_data' in source_file: 
        sources = json_sample['Meta(Refine)']['passage']


    elif 'summary_of_book_materials' in source_file: 
        passage = json_sample["passage"]  
        summary = json_sample["summary"]
        sources = [passage, summary]


    elif 'summary_of_thesis_materials' in source_file: 

        source_df = pd.DataFrame(json_sample['data'])

        if '논문/논문요약' or '특허섹션' in source_file:
                
            try:
                summary_entire_source_dict = dict(source_df['summary_entire'].explode())
                summary_entire_source_json = pd.json_normalize(summary_entire_source_dict)
                summary_entire_source_list = list(summary_entire_source_json.filter(regex='orginal_text').values[0])

                summary_section_source_dict = dict(source_df['summary_section'].explode())
                summary_section_source_json = pd.json_normalize(summary_section_source_dict)
                summary_section_source_list = list(summary_section_source_json.filter(regex='orginal_text').values[0])

                sources = summary_entire_source_list + summary_section_source_list

            except:
                summary_section_source_dict = dict(source_df['summary_section'].explode())
                summary_section_source_json = pd.json_normalize(summary_section_source_dict)
                sources = list(summary_section_source_json.filter(regex='orginal_text').values[0])
                    
        else:
            summary_section_source_dict = dict(source_df['summary_section'].explode())
            summary_section_source_json = pd.json_normalize(summary_section_source_dict)
            sources = list(summary_section_source_json.filter(regex='orginal_text').values[0])

    elif 'web_data_based_korean_corpus_data' in source_file:
        sources = list(pd.DataFrame(json_sample['SJML']['text'])['content'])

    return sources
