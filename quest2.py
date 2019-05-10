import Utils

def quest2():
    """
    第二问的代码
    统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    :return:
    """
    index_, colums_, list_main = Utils.Excelreaders(path="Data.xls")
    search_shool = Utils.schoolList()
    search_year = ["2014", "2015", "2016", "2017", "2018"]
    search_type = ["1", "2", "3", "4"]
    ans = []
    for i in range(len(search_year)):

        # temp_ans.append("浙江省")
        search_year_ = search_year[i]
        dict_forSeach = {}
        dict_forSeach["年份"] = [search_year_]
        out_list = Utils.multiSearchMain(colums_=colums_, Target_list=list_main, multiFinding_dict=dict_forSeach)
        for j in range(len(search_shool)):
            search_name = search_shool[j]
            dict_forSeach = {}
            dict_forSeach["学校"] = [search_name]
            school_out_list = Utils.multiSearchMain(colums_=colums_, Target_list=out_list, multiFinding_dict=dict_forSeach)
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
                small_out_list = Utils.multiSearchMain(colums_=colums_, Target_list=school_out_list,
                                                  multiFinding_dict=dict_forSeach)
                que_sum+=len(small_out_list)
                temp_ans.append(len(small_out_list))
                num_list.append(len(small_out_list))

            temp_ans.append(que_sum)
            for k in range(len(search_type)):
                temp_ans.append(float(num_list[k]) / que_sum)
            ans.append(temp_ans)

    ans_col = ["年份","学校", "一等奖", "二等奖", "三等奖","成功参赛奖", "获奖总数", "一等奖比例", "二等奖比例", "三等奖比例","成功参赛奖比例"]
    Utils.Excelwriter(index_=index_, colums_=ans_col, list_main=ans, path=r'./quest2.xls')

if __name__ == "__main__":
    quest2()
