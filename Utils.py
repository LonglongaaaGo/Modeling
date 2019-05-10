#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer

def Excelreaders(path ="Data.xls" ):
    """
    :param path: 读取文件的数据
    :return:index_，colums_,list_main 对应的excel的行名，列名，二维的list
    """
    data = pd.read_excel(path);
    colums_ = data.columns
    index_ = data.index
    list_main =[]
    for i in range(len(index_)):
        templist = []
        for j in range(len(colums_)):
            templist.append(data[colums_[j]][i])
        # print(templist)
        list_main.append(templist)
    return index_,colums_,list_main

def Excelwriter(index_,colums_,list_main,path = r'./1output.xls'):
    """
    :param index_: 行名
    :param colums_: 列名
    :param list_main: 二维list
    :param path:写入的路径
    :return: void
    """
    out = pd.DataFrame(list_main, columns=colums_)
    writer = pd.ExcelWriter(path)
    out.to_excel(writer,columns=colums_,index=False,encoding='utf-8',sheet_name='Sheet')
    writer.save()
    print("Excelwriter is "+path+" ok!")

def findDictId(colums_,findDict={}):
    """
    实际上就是把列明转化成对应的index字段
    :param colums_:dataformat 的 colums
    :param findDict:对应的列明和其搜索的内容 {"题目":["A","B"],"学校":["同济大学","浙江大学"]}
    :return:对应的列明的index和其搜索的内容{'1': ['A', 'B'], '2': ['同济大学', '浙江大学']}
    """
    assert len(findDict) >0
    outDict = {}
    keys = list(findDict.keys())
    for i in range(len(colums_)):
        if (len(keys) == 0):
            break;
        for j in range(len(keys)):
            if (keys[j] == colums_[i]):
                outDict[str(i)] = findDict[keys[j]]
                del keys[j]
                break;
    return outDict

def findColId(colums_,findCols=[]):
    """
    根据列名，找到对应的检索index col_index_list = findColId(colums_, findCols=["题目","学校"])
    :param colums_: 初始列明 如: ["xxx","题目","xxsadsa","学校"]
    :param findCols: findCols=["题目","学校"]
    :return:outIndex index[1,3]
    """
    outIndex = []
    if(len(findCols)==0):
        for i in range(len(colums_)):
            outIndex.append(i)
        return outIndex

    findCols = list(set(findCols))
    for i in range(len(colums_)):
        if(len(findCols)==0):
            break;
        for j in range(len(findCols)):
            if(findCols[j]==colums_[i]):
                outIndex.append(i)
                del findCols[j]
                break;
    return outIndex

def multiSearch(Target_list,multiFinding_list=[[]],col=[]):
    """
    多列，多条件查找
    :param Target_list: 被查找的目标二维list
    :param multiFinding_list: 检索的内容[["A","B"],["同济大学","浙江大学"]]
    :param col: 检索的内容，对应的列[1,2]
    :return: 最终检索出来的第一列包含 ["A","B"] 且 第二列包含["同济大学","浙江大学"]  的最终list
    """
    assert len(col) >= 0
    assert len(multiFinding_list) > 0
    assert len(Target_list) > 0
    assert len(col) == len(multiFinding_list)

    out_list = Target_list
    for i in range(len(multiFinding_list)):
        col_index = col[i]
        out_list = baseSearch(Target_list=out_list,Finding_list=multiFinding_list[i],col=col_index)
    return out_list

def multiSearchByDict(Target_list,multiFinding_dict={}):
    """
    :param Target_list:被查找的目标二维list
    :param multiFinding_dict:被检索的 字典内容如 ：{'1': ['A', 'B'], '2': ['同济大学', '浙江大学']}
    :return: 最终检索出来的内容
    """
    assert len(multiFinding_dict) > 0
    assert len(Target_list) > 0

    out_list = Target_list
    keys = list(multiFinding_dict.keys())
    for i in range(len(keys)):
        out_list = baseSearch(Target_list=out_list,Finding_list=multiFinding_dict[keys[i]],col=int(keys[i]))
    return out_list

def multiSearchMain(colums_,Target_list,multiFinding_dict={}):
    """
    :param colums_: DataFrame 结构的colums
    :param Target_list: 目标的二维list
    :param multiFinding_dict: {"题目":["A","B"],"学校":["同济大学","浙江大学"]}
    :return: 返回最终筛选的二维list
    """
    assert len(multiFinding_dict)>0
    assert len(Target_list)>0
    dict_ = findDictId(colums_ = colums_, findDict=multiFinding_dict)
    out_list = multiSearchByDict(Target_list = Target_list,multiFinding_dict = dict_)
    return out_list


def baseSearch(Target_list,Finding_list=[],col =0):
    """
    单列查询，对应的查询字段可以是一个列表
    :param Target_list: 被搜索的二维list
    :param Finding_list: 查找的关键字
    :param col: 查找的第几列
    :return: 返回符合的二维list，并不改变原先顺序
    """
    assert col>=0
    assert len(Finding_list)>0
    assert len(Target_list)>0
    out_list = []
    for i in range(len(Target_list)):
        for j in range(len(Finding_list)):
            if(str(Finding_list[j]) == str(Target_list[i][col])):
                out_list.append(Target_list[i])
                break;
    return out_list


def reader(label_col = -1):
    ''' 读出文件信息，并把某一列作为label
    :param label_col: 要选作为label 的列，默认-1
    :return: numpy for trainingdata and label
    '''
    data = pd.read_excel("2018_A.xlsx");
    df_li = data.values.tolist()
    train_data = []
    label = []
    for i in range(3,len(df_li)):
        ss = df_li[i]
        label.append(df_li[i][label_col])
        del df_li[i][label_col]
        # print i
        temp = []
        for j in range(len(df_li[i])):
            if pd.isnull(df_li[i][j]) or df_li[i][j]==" ":
                df_li[i][j] = 0
            # print "--------"+str(df_li[i][j])
            temp.append(float(df_li[i][j]))

        train_data.append(temp)

    train_data = np.array(train_data).astype(np.float32)
    label = np.array(label).astype(np.float32)
        # print(train_data)
        #  print(label)
    return train_data,label


def reader_del_nan(label_col = -1):
    ''' 读出文件信息，并把某一列作为label
    :param label_col: 要选作为label 的列，默认-1
    :return: numpy for trainingdata and label
    '''
    data = pd.read_excel("data.xlsx");
    df_li = data.values.tolist()
    train_data = []
    label = []
    for i in range(3,len(df_li)):
        ok = False
        for j in range(len(df_li[i])):
            if pd.isnull(df_li[i][j]) or df_li[i][j]==" ":
                ok = True
                break;
        if(ok==True):
            continue;

        label.append(df_li[i][label_col])
        del df_li[i][label_col]
        # print i
        temp = []
        for j in range(len(df_li[i])):
            if pd.isnull(df_li[i][j]) or df_li[i][j]==" ":
                df_li[i][j] = 0
            # print "--------"+str(df_li[i][j])
            temp.append(float(df_li[i][j]))

        train_data.append(temp)

    train_data = np.array(train_data).astype(np.float32)
    label = np.array(label).astype(np.float32)
        # print(train_data)
        #  print(label)
    return train_data,label





def reader_add_data(label_col = 58):
    # 先复制一份爱怎么玩怎么玩
    df = pd.read_excel("data.xlsx");
    # df_li = df.values.tolist()
    new_data = df.copy()

    for i in range(1,60):
        name = "a"+str(i)
        for j in range(0,len(new_data[name])):
            if(new_data[name][j]==" " or new_data[name][j]==""):
                new_data[name][j] = np.nan

    # 增加有NaN的布尔列（True/False）
    cols_with_missing = (col for col in new_data.columns
                         if new_data[col].isnull().any())
    for col in cols_with_missing:
        new_data[col + '_was_NaN'] = new_data[col].isnull()
    print (new_data)
    new_data = new_data.drop([0, 1])

    # new_data = new_data.drop(df.isin([" ",""]))
    # print (new_data)
    # Imputation
    my_imputer = Imputer()
    new_data_imputed = my_imputer.fit_transform(new_data)
    # array转换成df
    df_new_data_imputed = pd.DataFrame(new_data_imputed, columns=new_data.columns)
    # print (df_new_data_imputed)

    df_li = df_new_data_imputed.values.tolist()
    train_data = []
    label = []
    for i in range(0, len(df_li)):

        label.append(df_li[i][label_col])
        del df_li[i][label_col]
        # print i
        temp = []
        for j in range(len(df_li[i])):
            if pd.isnull(df_li[i][j]) or df_li[i][j] == " ":
                df_li[i][j] = 0
            # print "--------"+str(df_li[i][j])
            temp.append(float(df_li[i][j]))

        train_data.append(temp)

    train_data = np.array(train_data).astype(np.float32)
    label = np.array(label).astype(np.float32)
    # print(train_data)
    # print(label)
    return train_data, label



def Normalization(train):
    """
    :param train:
    :param label:
    :return:

    """
    for i in range(train.shape[1]):
        mean = np.mean(train[:,i])
        std = np.std(train[:,i])

        train[:,i] = (train[:,i] - mean)/float(std+1)

    return train


def shuffle(feature,label):
    ''' get the shuffle feature and label
    :param feature: the input data (num, feature)
    :param label: the lable (num, 1)
    :return: shuffle_feature(num,feature),shuffle_label(num,1)
    '''
    m = feature.shape[0]
    permutation = list(np.random.permutation(m))
    shuffle_feature = feature[permutation,:]
    shuffle_label = label[permutation,:]
    return shuffle_feature,shuffle_label


def shuffle2(feature,label):
    ''' get the shuffle feature and label
    :param feature: the input data (num, feature)
    :param label: the lable (num, 1)
    :return: shuffle_feature(num,feature),shuffle_label(num,1)
    '''
    m = feature.shape[0]
    # print np.random.permutation(m)
    permutation = list(np.random.permutation(m))
    shuffle_feature = feature[permutation,:]
    shuffle_label = label[permutation]
    return shuffle_feature,shuffle_label


def getData_name():
    # 先复制一份爱怎么玩怎么玩
    df = pd.read_excel("data.xlsx");
    # df_li = df.values.tolist()
    new_data = df.copy()
    name_list=[]
    for i in range(1,59):
        name = "a"+str(i)
        for j in range(3):
            if(new_data[name][j]==" "):
                continue
            if (new_data[name][j] == ""):
                continue
            if(pd.isnull(new_data[name][j])):
                continue
            name_list.append(new_data[name][j])
            break;
    return name_list


def stripList(list_Name):
    out_list_name = []
    for i in range(len(list_Name)):
        # .split(" ")
        out_list_name.append(list_Name[i][0].strip())
    return out_list_name


def quest1():
    """
    将表格中的浙江的大学筛选出来保存到quest1.xls
    :return:
    """
    index_, colums_, list_main = Excelreaders(path="Data.xls")
    index_Name, colums_Name, list_Name = Excelreaders(path="zhejiangName.xlsx")

    out_list_name = stripList(list_Name)

    # print(out_list_name)
    dict_forSeach = {}
    dict_forSeach["学校"] = out_list_name
    # # dict_forSeach = {"题目":["A","B","C"],"学校":["同济大学","浙江大学"],"获奖等级":["1"]}
    out_list = multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
    Excelwriter(index_=index_, colums_=colums_, list_main=out_list, path=r'./quest1.xls')
    # print(out_list)
    # dict_ = findDictId(colums_, findDict=dict_forSeach)
    # print(dict_)
    # col_index_list = findColId(colums_, findCols=["题目","学校"])
    # out_list = multiSearch(Target_list = list_main, multiFinding_list=[["A","B"],["同济大学","浙江大学"]], col=col_index_list)
    # # out_list = baseSearch(Tagrget_list=list_main,Finding_list=["A","B"],col=1)
    # # out_list = sarchList(Finding_list="B", Tagrget_list = list_main, col=index_list)


def quest1_2():
    """
    将筛选出来的表格再次进行整理，整理出历年的浙江高校的1，2，3，4等奖的获奖人数情况
    :return:
    """
    index_, colums_, list_main = Excelreaders(path="quest1.xls")
    search_year = ["2014", "2015", "2016", "2017", "2018"]
    search_type = ["1", "2", "3","4"]
    ans = []
    for i in range(len(search_year)):
        temp_ans = []
        temp_ans.append("浙江省")
        search_name = search_year[i]
        temp_ans.append(search_name)
        dict_forSeach = {}
        dict_forSeach["年份"] = [search_name]
        out_list = multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        # que_sum = len(out_list)
        # num_list = []
        que_sum = 0
        for j in range(len(search_type)):
            search_name = search_type[j]
            dict_forSeach = {}
            dict_forSeach["获奖等级"] = [search_name]
            small_out_list = multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
            temp_ans.append(len(small_out_list))
            que_sum+=len(small_out_list)
            # num_list.append(len(small_out_list))
        temp_ans.append(que_sum)

        # for j in range(len(search_type)):
        #     temp_ans.append(float(num_list[j]) / que_sum)
        ans.append(temp_ans)

    ans_col = ["省份", "年份", "一等奖", "二等奖", "三等奖","四等奖","获奖总数"]
    Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest1_2.xls')



def quest3():
    """
    对筛选出来的浙江的数据再次整理，找出浙江的历年的选题情况
    :return:
    """
    index_, colums_, list_main = Excelreaders(path="quest1.xls")
    search_year = ["2014", "2015", "2016", "2017", "2018"]
    search_type = ["A", "B", "C", "D", "E", "F"]
    ans = []
    for i in range(len(search_year)):
        temp_ans = []
        temp_ans.append("浙江省")
        search_name = search_year[i]
        temp_ans.append(search_name)
        dict_forSeach = {}
        dict_forSeach["年份"] = [search_name]
        out_list = multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        que_sum = len(out_list)
        num_list = []
        for j in range(len(search_type)):
            search_name = search_type[j]
            dict_forSeach = {}
            dict_forSeach["题目"] = search_name
            small_out_list = multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
            temp_ans.append(len(small_out_list))
            num_list.append(len(small_out_list))
        temp_ans.append(que_sum)

        for j in range(len(search_type)):
            temp_ans.append(float(num_list[j]) / que_sum)
        ans.append(temp_ans)

    ans_col = ["省份", "年份", "A", "B", "C", "D", "E", "F", "总和", "A比例", "B比例", "C比例", "D比例", "E比例", "F比例"]
    Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest3.xls')


def schoolList():
    """
    获取所有学校名单
    :return:
    """
    index_, colums_, list_main = Excelreaders(path="Data.xls")
    col_index = findColId(colums_, findCols=["学校"])
    schoollist = []
    for i in range(len(list_main)):
        schoollist.append(list_main[i][col_index[0]])
    schoollist = list(set(schoollist))
    # print(schoollist)
    # print(len(schoollist))
    return schoollist




def quest2():
    """
    统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    :return:
    """
    index_, colums_, list_main = Excelreaders(path="Data.xls")
    search_shool = schoolList()
    search_year = ["2014", "2015", "2016", "2017", "2018"]
    search_type = ["1", "2", "3", "4"]
    ans = []
    for i in range(len(search_year)):

        # temp_ans.append("浙江省")
        search_year_ = search_year[i]
        dict_forSeach = {}
        dict_forSeach["年份"] = [search_year_]
        out_list = multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        for j in range(len(search_shool)):
            search_name = search_shool[j]
            dict_forSeach = {}
            dict_forSeach["学校"] = [search_name]
            school_out_list = multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
            if len(school_out_list) == 0:
                print(search_name + "is not in "+search_year_)
                continue
            temp_ans = []
            temp_ans.append(search_year_)
            temp_ans.append(search_name)
            num_list = []
            que_sum = 0
            for k in range(len(search_type)):
                search_name = search_type[k]
                dict_forSeach = {}
                dict_forSeach["获奖等级"] = [search_name]
                small_out_list = multiSearchMain(colums_=colums_, Target_list=school_out_list,
                                                  multiFinding_dict=dict_forSeach)
                que_sum+=len(small_out_list)
                temp_ans.append(len(small_out_list))
                num_list.append(len(small_out_list))

            temp_ans.append(que_sum)
            for k in range(len(search_type)):
                temp_ans.append(float(num_list[k]) / que_sum)
            ans.append(temp_ans)

    ans_col = ["年份","学校", "一等奖", "二等奖", "三等奖","成功参赛奖", "获奖总数", "一等奖比例", "二等奖比例", "三等奖比例","成功参赛奖比例"]
    Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest2.xls')


def quest2_2():
    """
    统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    的基础上，计算出排名分数指标
    score1 = 4*list_main[i][2]+3*list_main[i][3]+2*list_main[i][4]+1*list_main[i][5]
    score2 = 4 * list_main[i][7] + 3 * list_main[i][8] + 2 * list_main[i][9] + 1 * list_main[i][10]
    :return:
    """
    # 层次分析法，获得权重
    ahp_np = AHP()
    index_, colums_, list_main = Excelreaders(path="quest2.xls")
    out_list=[]
    for i in range(len(list_main)):
        temp_list = []
        temp_list.append(list_main[i][0])
        temp_list.append(list_main[i][1])
        score1 = 4*list_main[i][2]+3*list_main[i][3]+2*list_main[i][4]+1*list_main[i][5]
        score2 = 4 * list_main[i][7] + 3 * list_main[i][8] + 2 * list_main[i][9] + 1 * list_main[i][10]
        score3 = ahp_np[0] * list_main[i][2] + ahp_np[1] * list_main[i][3] + ahp_np[2] * list_main[i][4] + ahp_np[3] * list_main[i][5]
        score4 = ahp_np[0] * list_main[i][7] + ahp_np[1] * list_main[i][8] + ahp_np[2] * list_main[i][9] + ahp_np[3] * list_main[i][10]
        temp_list.append(score1)
        temp_list.append(score2)
        temp_list.append(score3)
        temp_list.append(score4)
        out_list.append(temp_list)
    ans_col = ["年份","学校", "第一指标值", "第二指标值", "第三指标值", "第四指标值"]
    Excelwriter(index_=index_, colums_=ans_col, list_main=out_list, path=r'./quest2_2.xls')

def quest2_3():
    """统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    的基础上，计算出排名分数指标
    的基础上，对浙江省进行筛选
   """

    index_, colums_, list_main = Excelreaders(path="quest2_2.xls")
    index_Name, colums_Name, list_Name = Excelreaders(path="zhejiangName.xlsx")

    out_list_name = stripList(list_Name)

    dict_forSeach = {}
    dict_forSeach["学校"] = out_list_name
    # # dict_forSeach = {"题目":["A","B","C"],"学校":["同济大学","浙江大学"],"获奖等级":["1"]}
    out_list = multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
    Excelwriter(index_=index_, colums_=colums_, list_main=out_list, path=r'./quest2_3.xls')


def AHP():
    """
    层次分析法
    :return: 返回重要的四个指标 np.array()
    """
    X=[[1,3,5,7],
        [1/3,1,3,5],
        [1/5,1/3,1,3],
        [1/7,1/5,1/3,1]]
    X=np.array(X)
    eigenvalue, featurevector = np.linalg.eig(X)
    featurevector = np.around(featurevector, decimals=5).astype(np.float32)
    # print(X)
    # print(eigenvalue)
    print(featurevector)
    outList = []
    for i in range(len(featurevector)):
        outList.append(featurevector[i][0])
    # print(outList)
    out_np = np.array(outList)
    # print(out_np)
    return out_np

if __name__ == "__main__":
    quest1()
    quest1_2()
    quest3()
    quest2()
    quest2_2()
    quest2_3()



