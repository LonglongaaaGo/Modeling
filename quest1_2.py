import Utils


def quest1_2():
    """
    第一问的进阶代码
    将筛选出来的表格再次进行整理，整理出历年的浙江高校的1，2，3，4等奖的获奖人数情况
    :return:
    """
    index_, colums_, list_main = Utils.Excelreaders(path="quest1.xls")
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
        out_list = Utils.multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        # que_sum = len(out_list)
        # num_list = []
        que_sum = 0
        for j in range(len(search_type)):
            search_name = search_type[j]
            dict_forSeach = {}
            dict_forSeach["获奖等级"] = [search_name]
            small_out_list = Utils.multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
            temp_ans.append(len(small_out_list))
            que_sum+=len(small_out_list)
            # num_list.append(len(small_out_list))
        temp_ans.append(que_sum)

        # for j in range(len(search_type)):
        #     temp_ans.append(float(num_list[j]) / que_sum)
        ans.append(temp_ans)

    ans_col = ["省份", "年份", "一等奖", "二等奖", "三等奖","四等奖","获奖总数"]
    Utils.Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest1_2.xls')

if __name__ == "__main__":
    quest1_2()
