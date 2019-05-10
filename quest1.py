import Utils

def quest1():
    """
    第一问的代码
    将表格中的浙江的大学筛选出来保存到quest1.xls
    :return:
    """
    index_, colums_, list_main = Utils.Excelreaders(path="Data.xls")
    index_Name, colums_Name, list_Name = Utils.Excelreaders(path="zhejiangName.xlsx")

    out_list_name = Utils.stripList(list_Name)

    # print(out_list_name)
    dict_forSeach = {}
    dict_forSeach["学校"] = out_list_name
    # # dict_forSeach = {"题目":["A","B","C"],"学校":["同济大学","浙江大学"],"获奖等级":["1"]}
    out_list = Utils.multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
    Utils.Excelwriter(index_=index_, colums_=colums_, list_main=out_list, path=r'./quest1.xls')
    # print(out_list)
    # dict_ = findDictId(colums_, findDict=dict_forSeach)
    # print(dict_)
    # col_index_list = findColId(colums_, findCols=["题目","学校"])
    # out_list = multiSearch(Target_list = list_main, multiFinding_list=[["A","B"],["同济大学","浙江大学"]], col=col_index_list)
    # # out_list = baseSearch(Tagrget_list=list_main,Finding_list=["A","B"],col=1)
    # # out_list = sarchList(Finding_list="B", Tagrget_list = list_main, col=index_list)

if __name__ == "__main__":
    quest1()