import Gray_Pred as GP
import Utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def quest4():
    # f = open("电影票房.csv", encoding="utf8")
    index_, colums_, list_main = Utils.Excelreaders("quest3.xls")
    # del list_main[-1]
    df = pd.DataFrame(list_main, columns=colums_)

    # df = pd.read_csv(f)
    df.tail()
    forsee_num = 5
    gf = GP.GrayForecast(df, '总和')
    sum_c_num = gf.level_check()
    lamba_k = gf.getLambda_k()
    # print("level_check_总数{}".format(lamba_k))
    gf.forecast(forsee_num)
    gf.getCheck()
    # gf.log()
    # gf.plot()
    list_forSum = gf.getRes().values.tolist()
    print(list_forSum)

    name = ["年份", "参赛人数", "一等奖", "二等奖", "三等奖"]
    list_for_type = []
    c_numList = []
    list_for_orign = []
    for i in range(3):
        index_, colums_, list_main = Utils.Excelreaders("quest1_2.xls")
        # del list_main[-1]
        df = pd.DataFrame(list_main, columns=colums_)
        # df = pd.read_csv(f)
        df.tail()
        gf = GP.GrayForecast(df, name[2 + i])
        c_num = gf.level_check()
        c_numList.append(c_num)
        lamba_k = gf.getLambda_k()
        # print("level_check_{}:{}".format(name[2+i],lamba_k))
        gf.forecast(forsee_num)
        gf.getCheck()
        list_for_type.append(gf.getRes().values.tolist())
        list_for_orign.append(gf.getorign().values.tolist())
    # gf.log()
    # gf.plot()

    ans = []
    startNum = 2014

    for i in range(5):
        temp_ans = []
        temp_ans.append(str(i + startNum))
        temp_ans.append(int(list_forSum[i][0]))
        temp_ans.append(int(list_for_orign[0][i][0]))
        temp_ans.append(int(list_for_orign[1][i][0]))
        temp_ans.append(int(list_for_orign[2][i][0]))
        ans.append(temp_ans)

    for i in range(5, 5 + forsee_num):
        temp_ans = []
        temp_ans.append(str(i + startNum))
        temp_ans.append(int(list_forSum[i][0]))
        temp_ans.append(int(list_for_type[0][i][0]-c_numList[0]))
        temp_ans.append(int(list_for_type[1][i][0]-c_numList[1]))
        temp_ans.append(int(list_for_type[2][i][0]-c_numList[2]))
        ans.append(temp_ans)

    #
    # for i in range(0, 5 + forsee_num):
    #     temp_ans = []
    #     temp_ans.append(str(i + startNum))
    #     temp_ans.append(int(list_forSum[i][0]))
    #     temp_ans.append(int(list_for_type[0][i][0]))
    #     temp_ans.append(int(list_for_type[1][i][0]))
    #     temp_ans.append(int(list_for_type[2][i][0]))
    #     ans.append(temp_ans)


    Utils.Excelwriter(index_, colums_=name, list_main=ans, path=r'./quest4.xls')

    return ans
def quest4_2(ans_list):
    """
    相对残差检验
    :return:打印相对残差检验值
    """
    print(ans_list)
    out_list = []
    for i in range(1, len(ans_list[0])):
        temp_list = []
        for j in range(1,len(ans_list)-1):
            e_k = float(ans_list[j][i])/ans_list[j+1][i]
            temp_list.append(e_k)
        out_list.append(temp_list)

    print(out_list)




if __name__ == "__main__":
    ans_list = quest4()
    # quest4_2(ans_list)