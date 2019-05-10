import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import Utils


class GrayForecast():
#初始化
    def __init__(self, data, datacolumn=None):
        if isinstance(data, pd.core.frame.DataFrame):
            self.data = data
            try:
                self.data.columns = ['数据']
            except:
                if not datacolumn:
                    raise Exception('您传入的dataframe不止一列')
                else:
                    self.data = pd.DataFrame(data[datacolumn])
                    self.data.columns = ['数据']
        elif isinstance(data, pd.core.series.Series):
            self.data = pd.DataFrame(data, columns=['数据'])
        else:
            self.data = pd.DataFrame(data, columns=['数据'])

        self.forecast_list = self.data.copy()

        if datacolumn:
            self.datacolumn = datacolumn
        else:
            self.datacolumn = None

        # save arg:
        #        data                DataFrame    数据
        #        forecast_list       DataFrame    预测序列
        #        datacolumn          string       数据的含义
#级比校验
    def level_check(self):
        # 数据级比校验
        n = len(self.data)
        lambda_k = np.zeros(n - 1)
        self.orign_list = self.forecast_list.copy()
        for i in range(n - 1):
            lambda_k[i] = self.data.ix[i]["数据"] / self.data.ix[i + 1]["数据"]

            if lambda_k[i] < np.exp(-2 / (n + 1)) or lambda_k[i] > np.exp(2 / (n + 2)):
                flag = False
                # print("false!!!")
            else:
                flag = True

        self.lambda_k = lambda_k

        if not flag:
            print("级比校验失败，请对X(0)做平移变换--------------")
            print("平移变换前 级比为：")
            print(self.lambda_k)
            c = 0
            for j in range(0, 100000):
                c = j
                if_ok = True
                for i in range(n - 1):
                    lambda_k[i] = (self.data.ix[i]["数据"]+c) / (self.data.ix[i + 1]["数据"]+c)
                    if lambda_k[i] < np.exp(-2 / (n + 1)) or lambda_k[i] > np.exp(2 / (n + 2)):
                        if_ok =False
                        break;

                if if_ok==True:
                    print("C ={} ----------------".format(c))
                    for i in range(n - 1):
                        self.data.ix[i]["数据"]+=c
                    break
            for i in range(n - 1):
                lambda_k[i] = self.data.ix[i]["数据"] / self.data.ix[i + 1]["数据"]
                if lambda_k[i] < np.exp(-2 / (n + 1)) or lambda_k[i] > np.exp(2 / (n + 2)):
                    flag = False
                    # print("false!!!")
                else:
                    flag = True

            self.lambda_k = lambda_k
            print("平移变换后C={} , 级比为：".format(c))
            print(self.lambda_k)

            self.forecast_list = self.data.copy()

            return c
        else:
            print("级比校验成功，级比为")
            print(self.lambda_k)
            return 0
        # save arg:
        #        lambda_k            1-d list
    def getorign(self):
        return self.orign_list
    def getLambda_k(self):
        return self.lambda_k

#GM(1,1)建模
    def GM_11_build_model(self, forecast=5):

        if forecast > len(self.data):
            raise Exception('您的数据行不够')
        X_0 = np.array(self.forecast_list['数据'].tail(forecast))
        #       1-AGO
        X_1 = np.zeros(X_0.shape)
        for i in range(X_0.shape[0]):
            X_1[i] = np.sum(X_0[0:i + 1])
        #       紧邻均值生成序列
        Z_1 = np.zeros(X_1.shape[0] - 1)
        for i in range(1, X_1.shape[0]):
            Z_1[i - 1] = -0.5 * (X_1[i] + X_1[i - 1])

        B = np.append(np.array(np.mat(Z_1).T), np.ones(Z_1.shape).reshape((Z_1.shape[0], 1)), axis=1)
        Yn = X_0[1:].reshape((X_0[1:].shape[0], 1))

        B = np.mat(B)
        Yn = np.mat(Yn)
        a_ = (B.T * B) ** -1 * B.T * Yn

        a, b = np.array(a_.T)[0]

        X_ = np.zeros(X_0.shape[0])
        def f(k):
            return (X_0[0] - b / a) * (1 - np.exp(a)) * np.exp(-a * (k))
        self.forecast_list.loc[len(self.forecast_list)] = f(X_.shape[0])

#预测
    def forecast(self, time=5, forecast_data_len=5):
        for i in range(time):
            self.GM_11_build_model(forecast=forecast_data_len)
#打印日志
    def log(self):
        res = self.forecast_list.copy()
        if self.datacolumn:
            res.columns = [self.datacolumn]
        return res
#重置
    def reset(self):
        self.forecast_list = self.data.copy()
#作图
    def plot(self):
        self.forecast_list.plot()
        if self.datacolumn:
            plt.ylabel(self.datacolumn)
            plt.legend([self.datacolumn])
            plt.show()

    def getRes(self):
        return self.forecast_list




