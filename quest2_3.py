import Utils

def quest2_3():
    """
    第二问的代码，对浙江省再进行筛选
    统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    的基础上，计算出排名分数指标
    的基础上，对浙江省进行筛选
   """

    index_, colums_, list_main = Utils.Excelreaders(path="quest2_2.xls")
    index_Name, colums_Name, list_Name =  Utils.Excelreaders(path="zhejiangName.xlsx")

    out_list_name = Utils.stripList(list_Name)

    dict_forSeach = {}
    dict_forSeach["学校"] = out_list_name
    # # dict_forSeach = {"题目":["A","B","C"],"学校":["同济大学","浙江大学"],"获奖等级":["1"]}
    out_list =  Utils.multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
    Utils.Excelwriter(index_=index_, colums_=colums_, list_main=out_list, path=r'./quest2_3.xls')


if __name__ == "__main__":
    quest2_3()