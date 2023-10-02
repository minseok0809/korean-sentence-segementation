import pandas as pd

def make_sources(json_sample, source_file):
            
    corpus_type1 = ['행정 문서 대상 기계독해 데이터', '기계독해']

    if '특허 분야 자동분류 데이터' in source_file:
        sources = list(pd.DataFrame(json_sample['dataset'])['abstract'].dropna())


    elif '산업정보 연계 주요국 특허 영-한 데이터' in source_file:
        sources = list(pd.DataFrame(json_sample['labeled_data'])['astrt_cont_kor'])


    elif '문서요약 텍스트' in source_file:
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


    elif '일반상식' in source_file: 
        if 'ko_wiki_v1_squad' in source_file:
            source_df = pd.DataFrame(json_sample['data'])
            source_dict = dict(source_df['paragraphs'].explode())
            source_json = pd.json_normalize(source_dict)
            sources = list(source_json.filter(regex='context').values[0])
            
        else:
            sources = (pd.DataFrame(json_sample['sentence'])['text'])


    elif '대규모 구매도서 기반 한국어 말뭉치 데이터' in source_file:        
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


    elif '법률 규정 (판결서 약관 등) 텍스트 분석 데이터' in source_file:   
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


    elif '전문분야 말뭉치' in source_file: 
       
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


    elif '도서자료 기계독해' in source_file: 

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


    elif '요약문 및 레포트 생성 데이터' in source_file: 
        sources = json_sample['Meta(Refine)']['passage']


    elif '도서자료 요약' in source_file: 
        passage = json_sample["passage"]  
        summary = json_sample["summary"]
        sources = [passage, summary]


    elif '논문자료 요약' in source_file: 

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


    elif '웹데이터 기반 한국어 말뭉치 데이터' in source_file:
        sources = list(pd.DataFrame(json_sample['SJML']['text'])['content'])


    return sources
