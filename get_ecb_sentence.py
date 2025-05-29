"""
@Author: xychen
@Date: 2022.10.31
@Description: 抽取ECB+语料库的句子信息，存入.csv文件
"""
import os
import xml.etree.ElementTree as ET
import pandas as pd

exceptions = [('31_10ecbplus.xml', 979),
                  ('9_3ecbplus.xml', 30),
                  ('9_4ecbplus.xml', 32)]


def is_digit(st):
    flag = False
    try:
        flag = (type(eval(st)) == int)
    except Exception:
        return False
    finally:
        return flag

def get_ecb_doc_list(path):
    topic_list = os.listdir(ecb_path)
    # print(topic_list)
    # print(is_digit(topic_list[0]))
    doc_count = 0
    plus_count = 0
    non_plus_count = 0
    ecb_count = {}
    doc_path_list = []
    for topic in topic_list:

        if is_digit(topic):
            topic_count = {}
            doc_path = os.path.join(ecb_path, topic) + '\\'
            # print("topic:", topic)
            cur_topic_docs = os.listdir(doc_path)
            # print("主题：", topic, " 文档数：", len(cur_topic_docs), end=' ')
            doc_count += len(cur_topic_docs)
            cur_plus_count = 0
            cur_non_plus_count = 0
            for doc in cur_topic_docs:
                if "plus" in doc:
                    cur_plus_count += 1
                else:
                    cur_non_plus_count += 1
            # print("plus文档数：", cur_plus_count, " 非plus文档数：", cur_non_plus_count)
            topic_count["doc_count"] = len(cur_topic_docs)
            topic_count["plus"] = cur_plus_count
            topic_count["non_plus"] = cur_non_plus_count
            ecb_count[topic] = topic_count
            plus_count += cur_plus_count
            non_plus_count += cur_non_plus_count
            doc_path_list.extend(cur_topic_docs)
    # print("总plus文档数：", plus_count)
    # print("总非plus文档数：", non_plus_count)
    # print("总文档数：", doc_count)
    print(ecb_count)
    print(doc_path_list)
    for i in range(len(doc_path_list)):
        doc_path_list[i] = os.path.join(ecb_path, doc_path_list[i].split('_')[0], doc_path_list[i])
    print(doc_path_list)
    print(len(doc_path_list))
    return doc_path_list, ecb_count

def ecb_doc_extract(file_name):
    tree = ET.parse(file_name)  # 解析当前的XML文档
    root = tree.getroot()  # 获得根节点
    t_id_list = []
    sentence_number_list = []
    word_position_list = []
    word_list = []
    for token in root.iter('token'):
        t_id = int(token.attrib['t_id'])
        sentence_number = int(token.attrib['sentence'])# 文档中的句子编号
        word_position = int(token.attrib['number'])# 该token在句子中的位置编号
        word = token.text
        t_id_list.append(t_id)
        sentence_number_list.append(sentence_number)
        word_position_list.append(word_position)
        word_list.append(word)
        # print(type(t_id), sentence_number, word_position, word)
    # print(word_list)
    # print(t_id_list)
    # print(sentence_number_list)
    # print(word_position_list)
    # print(len(word_list), len(t_id_list), len(sentence_number_list), len(word_position_list))
    sentences = ['' for i in range(max(sentence_number_list)+1)]
    sentence_word_list = [[] for i in range(max(sentence_number_list)+1)]
    sentence_t_id_list = [[] for i in range(max(sentence_number_list)+1)]
    sentence_word_position_list = [[] for i in range(max(sentence_number_list)+1)]
    # print(sentence_word_list)
    # print(sentence_t_id_list)
    sentence_id = list(range(max(sentence_number_list)+1))
    # print(len(sentences))
    # print(sentences)
    for i in range(len(sentence_number_list)):
        sentences[sentence_number_list[i]] += (word_list[i] + " ")
        sentence_word_list[sentence_number_list[i]].append(word_list[i])
        sentence_t_id_list[sentence_number_list[i]].append(t_id_list[i])
        sentence_word_position_list[sentence_number_list[i]].append(word_position_list[i])
        # print(sentence_word_list)
        # print(sentence_t_id_list)
    # print(sentences)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip()
    # print(sentences)
    # print(sentence_word_list)
    # print(sentence_word_position_list)
    # print(sentence_t_id_list)
    # print(sentence_id)
    # token_list = root.find("token")
    # print(token_list[0])
    doc_list = [file_name.split('\\')[-1]] * len(sentences)
    return doc_list, sentences, sentence_word_list, sentence_word_position_list, sentence_t_id_list, sentence_id

if __name__ == '__main__':
    ecb_path = "ECB+_LREC2014\\ECB+\\"
    doc_path_list, ecb_count = get_ecb_doc_list(ecb_path)# 获取全部文档路径列表
    ecb_doc_extract(doc_path_list[0])
    doc = []
    sentence = []
    word_list = []
    position = []
    token_id = []
    sent_id = []
    for i in range(len(doc_path_list)):
         doc_list, sentences, sentence_word_list, sentence_word_position_list, sentence_t_id_list, sentence_id = ecb_doc_extract(doc_path_list[i])
         doc.extend(doc_list)
         sentence.extend(sentences)
         word_list.extend(sentence_word_list)
         position.extend(sentence_word_position_list)
         token_id.extend(sentence_t_id_list)
         sent_id.extend(sentence_id)
    data_dict = {'doc': doc,
                 'sentence': sentence,
                 'word_list': word_list,
                 'position': position,
                 'token_id': token_id,
                 'sent_id': sent_id}
    df = pd.DataFrame(data_dict)
    df.to_csv("ECB+info_v1(sentence).csv", index=False)# 16314个句子
