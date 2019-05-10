import Utils


def quest2_2():
    """
    第二题的进阶，利用层次分析法求出权重分值数据
    统计出所有学校，所有年份分别对应的1，2，3，等奖的数量和比例以及总数
    的基础上，计算出排名分数指标
    score1 = 4*list_main[i][2]+3*list_main[i][3]+2*list_main[i][4]+1*list_main[i][5]
    score2 = 4 * list_main[i][7] + 3 * list_main[i][8] + 2 * list_main[i][9] + 1 * list_main[i][10]
    :return:
    """
    # 层次分析法，获得权重
    ahp_np = Utils.AHP()
    index_, colums_, list_main = Utils.Excelreaders(path="quest2.xls")
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
    Utils.Excelwriter(index_=index_, colums_=ans_col, list_main=out_list, path=r'./quest2_2.xls')

if __name__ == "__main__":
    quest2_2()