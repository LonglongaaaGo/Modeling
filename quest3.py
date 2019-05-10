
import Utils

def quest3():
    """
    第三题的代码
    对筛选出来的浙江的数据再次整理，找出浙江的历年的选题情况
    :return:
    """
    index_, colums_, list_main = Utils.Excelreaders(path="quest1.xls")
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
        out_list = Utils.multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        que_sum = len(out_list)
        num_list = []
        for j in range(len(search_type)):
            search_name = search_type[j]
            dict_forSeach = {}
            dict_forSeach["题目"] = search_name
            small_out_list = Utils.multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
            temp_ans.append(len(small_out_list))
            num_list.append(len(small_out_list))
        temp_ans.append(que_sum)

        for j in range(len(search_type)):
            temp_ans.append(float(num_list[j]) / que_sum)
        ans.append(temp_ans)

    ans_col = ["省份", "年份", "A", "B", "C", "D", "E", "F", "总和", "A比例", "B比例", "C比例", "D比例", "E比例", "F比例"]
    Utils.Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest3.xls')


if __name__ == "__main__":
    quest3()