import re
import kss

def preprocessing_text(source, corpus_path):

    corpus_type1 = ['automatic_patent_classification', 
                    'british_korean_data_on_patents_in_major_countries_linked_to_industrial_information',
                    'machine_reading_data_for_administrative_documents',
                    'professional_corpus',
                    'summary_of_thesis_materials']

    corpus_type2 = ['document_summary_text', 'general_common_sense', 'machine_reading_pro', 
                    'news_article_machine_reading_data', 'reading_books_by_machine']

    corpus_type3 = ['korean_corpus_data_based_on_large_scale_purchase_books',
                    'summary_and_report_generation_data',
                    'summary_of_book_materials']
    
    corpus_type4 = ['web_data_based_korean_corpus_data']

    corpus_type5 = ['legal_regulations_(such_as_terms_and_conditions_of_judgment)_text_analysis_data']

    corpus_type6 = ['professional_corpus', 'legal_text']

    corpus_type7 = ['machine_reading_data_for_administrative_documents', 'tableqa']

    if any(corpus in corpus_path for corpus in corpus_type1) and \
        not 'tableqa' in corpus_path and 'legal_text' not in corpus_path:
        preprocessing_sentence_list = preprocessing_type1(source)

    if any(corpus in corpus_path for corpus in corpus_type2):
        preprocessing_sentence_list = preprocessing_type2(source)

    if any(corpus in corpus_path for corpus in corpus_type3):
        preprocessing_sentence_list = preprocessing_type3(source)

    if any(corpus in corpus_path for corpus in corpus_type4):
        preprocessing_sentence_list = preprocessing_type4(source)

    if any(corpus in corpus_path for corpus in corpus_type5):
        preprocessing_sentence_list = preprocessing_type5(source)

    if all(corpus in corpus_path for corpus in corpus_type6):
        preprocessing_sentence_list = preprocessing_type6(source)

    if all(corpus in corpus_path for corpus in corpus_type7):
        preprocessing_sentence_list = preprocessing_type7(source)

    return preprocessing_sentence_list


def preprocessing_type1(source):

    """
    유형 1
    공통 전처리 코드에서 KSS 1번
    <산업정보 연계 주요국 특허 영-한 데이터>, <특허 분야 자동분류 데이터>,
    <행정 문서 대상 기계독해 데이터>, <전문분야 말뭉치>, <행정 문서 대상 기계독해 데이터>, <논문자료 요약>
    """
    
    preprocessing_sentence_list = []
    
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거

    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거 
        
    for sentence in kss.split_sentences(source, use_heuristic=False,
                                        num_workers=32):
    # KSS(Korean Sentence Segmentation)로 문장 분리 
    # Formal articles (wiki, news, essays): recommend to False

        if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
            bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
            len(sentence.split()) > 5:
            # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, + 제외
            # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
            # 다섯 어절 이하 문장 제외


            if ']' in sentence and '[' not in sentence:
                sentence  = re.sub(r".*?]", "", sentence)    
            # 중괄호 앞에 있는 '성명/직함]' 형태 제거


            sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
            # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

            sentence = sentence.strip()
            # strip으로 앞뒤 공백 제거

            total_length = len(sentence.replace(" " , ""))
            hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
            hangeul_ratio = hangeul_length / total_length
            if hangeul_ratio >= 0.5:
            # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외

                for sentence2 in kss.split_sentences(sentence, use_heuristic=False,
                                        num_workers=32):
                    for sentence3 in kss.split_sentences(sentence2, use_heuristic=False,
                                                         num_workers=32):
                        preprocessing_sentence_list.append(sentence3)

            # 마지막에 KSS(Korean Sentence Segmentation)로 문장 분리 2번 실행

    return preprocessing_sentence_list


def preprocessing_type2(source):

    """
    유형 2
    공통 전처리 코드에서 KSS 1번 + 따옴표 제거
    - 문장의 시작과 끝이 따옴표("")이면 따옴표 제거
    <기계독해>, <뉴스 기사 기계독해 데이터>, <도서자료 기계독해>, <일반상식>, <문서요약 텍스트>
    """

    preprocessing_sentence_list = []
    
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거

    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거 
    
    for sentence in kss.split_sentences(source, use_heuristic=False,
                                        num_workers=32):
    # KSS(Korean Sentence Segmentation)로 문장 분리 
    # Formal articles (wiki, news, essays): recommend to False
    
        if source[0] == '"':
            del(source[0])
        elif source[-1] == '"':
            del(source[0])
        elif source[0] == '"' and source[-1] == '"':
            del(source[0])
            del(source[-1])
        # 문장의 시작과 끝이 따옴표("")이면 따옴표 제거    

        if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
            bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
            len(sentence.split()) > 5:
            # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, + 제외
            # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
            # 다섯 어절 이하 문장 제외


            if ']' in sentence and '[' not in sentence:
                sentence  = re.sub(r".*?]", "", sentence)    
            # 중괄호 앞에 있는 '성명/직함]' 형태 제거


            sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
            # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

            sentence = sentence.strip()
            # strip으로 앞뒤 공백 제거

            total_length = len(sentence.replace(" " , ""))
            hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
            hangeul_ratio = hangeul_length / total_length
            if hangeul_ratio >= 0.5:
            # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외
                preprocessing_sentence_list.append(sentence)

    return preprocessing_sentence_list


def preprocessing_type3(source):

    """
    유형 3
    공통 전처리 코드에서 KSS 3번 + 따옴표 제거
    - 문장의 시작과 끝이 따옴표("")이면 따옴표 제거
    <요약문 및 레포트 생성 데이터>, <대규모 구매도서 기반 한국어 말뭉치 데이터>, <도서자료 요약>
    """

    preprocessing_sentence_list = []
    
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거


    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거 
    
    for sentence in kss.split_sentences(source, use_heuristic=False,
                                        num_workers=32):
    # KSS(Korean Sentence Segmentation)로 문장 분리 
    # Formal articles (wiki, news, essays): recommend to False
    
        if source[0] == '"':
            del(source[0])
        elif source[-1] == '"':
            del(source[0])
        elif source[0] == '"' and source[-1] == '"':
            del(source[0])
            del(source[-1])
        # 문장의 시작과 끝이 따옴표("")이면 따옴표 제거
        
        if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
            bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
            len(sentence.split()) > 5:
            # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, + 제외
            # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
            # 다섯 어절 이하 문장 제외


            if ']' in sentence and '[' not in sentence:
                sentence  = re.sub(r".*?]", "", sentence) 
            # 중괄호 앞에 있는 '성명/직함]' 형태 제거


            sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
            # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

            sentence = sentence.strip()
            # strip으로 앞뒤 공백 제거

            total_length = len(sentence.replace(" " , ""))
            hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
            hangeul_ratio = hangeul_length / total_length
            if hangeul_ratio >= 0.5:
            # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외

                for sentence2 in kss.split_sentences(sentence, use_heuristic=False,
                                        num_workers=32):
                    for sentence3 in kss.split_sentences(sentence2, use_heuristic=False,
                                                         num_workers=32):
                        preprocessing_sentence_list.append(sentence3)

            # 마지막에 KSS(Korean Sentence Segmentation)로 문장 분리 2번 실행

  
    return preprocessing_sentence_list


def preprocessing_type4(source):

    """
    유형 4
    공통 전처리 코드에서 KSS 1번 + 따옴표 제거 + 추가사항
    - 구두점 ". . .", ". .", ".."을 온점 "."으로 교체
    <웹데이터 기반 한국어 말뭉치 데이터>
    """
    
    preprocessing_sentence_list = []
    
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거


    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거  
        
    for sentence in kss.split_sentences(source, use_heuristic=False,
                                        num_workers=32):
    # KSS(Korean Sentence Segmentation)로 문장 분리 
    # Formal articles (wiki, news, essays): recommend to False
    
        if source[0] == '"':
            del(source[0])
        elif source[-1] == '"':
            del(source[0])
        elif source[0] == '"' and source[-1] == '"':
            del(source[0])
            del(source[-1])
        # 문장의 시작과 끝이 따옴표("")이면 따옴표 제거
        
        if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
            bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
            len(sentence.split()) > 5:
            # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, + 제외
            # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
            # 다섯 어절 이하 문장 제외


            if ']' in sentence and '[' not in sentence:
                sentence  = re.sub(r".*?]", "", sentence)    
            # 중괄호 앞에 있는 '성명/직함]' 형태 제거


            sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
            # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

            sentence = sentence.strip()
            # strip으로 앞뒤 공백 제거

            total_length = len(sentence.replace(" " , ""))
            hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
            hangeul_ratio = hangeul_length / total_length
            if hangeul_ratio >= 0.5:
            # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외
               
                sentence = sentence.replace(". . .", ".")
                sentence = sentence.replace(". .", ".")
                sentence = sentence.replace("..", ".")
                
            # 구두점 ". . .", ". .", ".."을 온점 "."으로 교체

                for sentence2 in kss.split_sentences(sentence, use_heuristic=False,
                                        num_workers=32):
                    for sentence3 in kss.split_sentences(sentence2, use_heuristic=False,
                                                         num_workers=32):
                        preprocessing_sentence_list.append(sentence3)

            # 마지막에 KSS(Korean Sentence Segmentation)로 문장 분리 2번 실행
            
  
    return preprocessing_sentence_list

def preprocessing_type5(source):

    """
    유형 5
    공통 전처리 코드에서 KSS 1번 + 추가사항
    - 숫자.(1. 2. ...), 원숫자(①, ②, ③, ..., ⑭, ⑮)를 기준으로 문장 분리. 그 이후 KSS 실행
    <법률 규정 (판결서 약관 등) 텍스트 분석 데이터>
    """

    preprocessing_sentence_list = []
    
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거


    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거   
    
    sources = re.split(r"[0-9]+[.]|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮", source)
    # 숫자.(1. 2. ...), 원숫자(①, ②, ③, ...)를 기준으로 문장 분리

    for source in sources:
        
        for sentence in kss.split_sentences(source, use_heuristic=False,
                                            num_workers=32):
        # KSS(Korean Sentence Segmentation)로 문장 분리 
        # Formal articles (wiki, news, essays): recommend to False
        
            if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
                bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
                len(sentence.split()) > 5:
                # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, + 제외
                # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
                # 다섯 어절 이하 문장 제외


                if ']' in sentence and '[' not in sentence:
                    sentence  = re.sub(r".*?]", "", sentence)    
                # 중괄호 앞에 있는 '성명/직함]' 형태 제거


                sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
                # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

                sentence = sentence.strip()
                # strip으로 앞뒤 공백 제거

                total_length = len(sentence.replace(" " , ""))
                hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
                hangeul_ratio = hangeul_length / total_length
                if hangeul_ratio >= 0.5:
                # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외
                    preprocessing_sentence_list.append(sentence)

    return preprocessing_sentence_list


def preprocessing_type6(source):

    """
    유형 6
    공통 전처리 코드에서 KSS 1번 + 추가사항
    - '제n조의n항(text)', '제n조(text)' 꼴 제거
    - 숫자.(1. 2. ...), 원숫자(①, ②, ③, ..., ⑭, ⑮)를 기준으로 문장 분리
    - 문장의 시작이 특수문자인 문장(원문자 - ①, ②, ③, ..., ⑭, ⑮ 제외) 제외
    <전문분야 말뭉치>의 법령 및 판례 텍스트
    """

    preprocessing_sentence_list = []
    source = source.strip()
    # strip으로 앞뒤 공백 제거

    source = re.sub(r"\[.*?\]|\{.*?\}", "", source)
    # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거

    try:
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(source)
    
    
        if type(text_in_small_bracket) == str:

            text = text_in_small_bracket

            text_size = len(text)
            last_index = source.find(text) + len(text)
            if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

            if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                small_bracket = "(" + text + ")"
                source = source.replace(small_bracket, " " + text + " ")    

        elif type(text_in_small_bracket) == list:

            for text in text_in_small_bracket:

                text_size = len(text)
                last_index = source.find(text) + len(text)
                if len(source) >= last_index+1 and source[last_index-text_size-1] == '(' and source[last_index+1] == '.':
                    source = source.replace(source[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    source = source.replace(small_bracket, " " + text + " ")    

    except:
        pass

        # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
        # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
    
    if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', source[:2])) == True:
        source = source.replace(source[:2], "")
        
    source = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", source)
    # '가.', '나.', ... 형태의 문자열 제거 
   
    source = re.sub(r'제\d{1,}조의\d{1,}\([^)]+\)', "", source)
    source = re.sub(r'제\d{1,}조\([^)]+\)', "",source)
    sources = re.split(r"[0-9]+[.]|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮", source)
    # '제n조의n항(text)', '제n조(text)' 꼴 제거
    # 숫자.(1. 2. ...), 원숫자(①, ②, ③, ...)를 기준으로 문장 분리
    
    for source in sources:
    
        for sentence in kss.split_sentences(source, use_heuristic=False,
                                            num_workers=32):
        # KSS(Korean Sentence Segmentation)로 문장 분리 
        # Formal articles (wiki, news, essays): recommend to False

            if re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮]", sentence[0]) is not None and \
                bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and \
                len(sentence.split()) > 5:
                # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, +, 
                # ①, ②, ③, ④, ⑤, ⑥, ⑦, ⑧, ⑨, ⑩, ⑪, ⑫, ⑬, ⑭, ⑮ 제외) 제외
                # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
                # 다섯 어절 이하 문장 제외

                sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
                # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표, 제외)

                sentence = sentence.strip()
                # strip으로 앞뒤 공백 제거

                total_length = len(sentence.replace(" " , ""))
                hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
                hangeul_ratio = hangeul_length / total_length
                if hangeul_ratio >= 0.5:
                # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외
                    preprocessing_sentence_list.append(sentence)

    return preprocessing_sentence_list

def preprocessing_type7(source):
    

    """
    유형 7
    - KSS를 사용하지 않고 HTML 언어('br', 'tr', 'td', 'table', 'tbody', 'rowspan')를 기준으로 문장 분리
    <행정 문서 대상 기계독해 데이터>의 ##_tableqa.json
    """

    preprocessing_sentence_list = []
    source_split = re.split('br|tr|td|table|tbody|rowspan', source)
    # 문자열 'br', 'tr', 'td', 'table', 'tbody'를 기준으로 문장 분리

    for source in source_split:
        sentence = re.sub('(br|tr|td|table|tbody|rowspan|<|>|/)', '', source)
        # 문자열 'br', 'tr', 'td', 'table', 'tbody' 특수기호 '<', '>', '/'를 제외
            
        sentence = sentence.strip()
        # strip으로 앞뒤 공백 제거
        
        sentence = re.sub(r"\[.*?\]|\{.*?\}", "", sentence)
        # 기타 괄호 제거할 시 괄호 내부에 모든 텍스트 제거
        
       
        
        bracket_form = re.compile('\(([^)]+)')
        text_in_small_bracket = bracket_form.findall(sentence)
        
        
        try:

            if type(text_in_small_bracket) == str:

                text = text_in_small_bracket

                text_size = len(text)
                last_index = sentence.find(text) + len(text)
                if len(sentence) >= last_index+1 and sentence[last_index-text_size-1] == '(' and sentence[last_index+1] == '.':
                    sentence = sentence.replace(sentence[last_index-text_size-1 : last_index+1] + ".", ".")

                if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                    small_bracket = "(" + text + ")"
                    sentence = sentence.replace(small_bracket, " " + text + " ")    

            elif type(text_in_small_bracket) == list:

                for text in text_in_small_bracket:

                    text_size = len(text)
                    last_index = sentence.find(text) + len(text)
                    if len(sentence) >= last_index+1 and sentence[last_index-text_size-1] == '(' and sentence[last_index+1] == '.':
                        sentence = sentence.replace(sentence[last_index-text_size-1 : last_index+1] + ".", ".")

                    if len(text.split()) > 5 and bool(re.match(r'[.]|[!]|[?]', text[-1])) == True:
                        small_bracket = "(" + text + ")"
                        sentence = sentence.replace(small_bracket, " " + text + " ")    

        except:
            pass

            # 마침표(.) 앞에 소괄호')'가 있을시 소괄호 제거와 함께 소괄호 내부 텍스트 제거
            # 소괄호 내부 텍스트가 5어절 이상이고 끝이 온점(.). 느낌표(!). 물음표(?)일 떼 소괄호 제거
        
        

        if bool(re.match(r'[가나다라마바사아자차카타파하]+[.]', sentence[:2])) == True:
            sentence = source.replace(source[:2], "")

        sentence = re.sub(r' [가나다라마바사아자차카타파하]+[.]', "", sentence)
        # '가.', '나.', ... 형태의 문자열 제거 


        if len(sentence) > 1 and \
        re.search("^[A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎]", sentence[0]) is not None and \
        bool(re.match(r'[.]|[!]|[?]', sentence[-1])) == True and  \
        len(sentence.split()) > 5:
         # 문장의 시작이 특수문자인 문장(영어 대소문자, 한글, 한자, 숫자, -, +, 
        # 문장의 끝이 온점(.). 느낌표(!). 물음표(?)가 아닌 문장 제외
        # 다섯 어절 이하 문장 제외

            sentence = re.sub(r"[^A-Za-z0-9ㄱ-ㅎ가-힣一-鿕㐀-䶵豈-龎()+-.,]", " ", sentence)
            # 특수문자 제거(영어 대소문자, 한글, 한자, 숫자, -, +, 소괄호, 마침표, 쉼표 제외)

            sentence = sentence.strip()
            # strip으로 앞뒤 공백 제거

            total_length = len(sentence.replace(" " , ""))
            hangeul_length = len(re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", sentence.replace(" " , "")))
            hangeul_ratio = hangeul_length / total_length
            if hangeul_ratio >= 0.5:
            # 한글이 아닌 문자열이 50% 이상이 넘은 문장 제외
                preprocessing_sentence_list.append(sentence)

    return preprocessing_sentence_list



