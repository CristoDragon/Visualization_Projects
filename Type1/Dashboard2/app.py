from pickle import TRUE
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import wordcloud



st.title("拓达客户分析")
st.subheader("Author: Runsheng Xu")

# Read in the data from csv file
Customer_data = pd.read_csv("https://raw.githubusercontent.com/CristoDragon/CSE5243/main/TouchdownCustomerInformation.csv", encoding="gbk")
service_data = pd.read_csv("https://raw.githubusercontent.com/CristoDragon/CSE5243/main/serviceData.csv", encoding="gbk")
# Replcace all empty cells with NaN
df_Customer = Customer_data.replace(r'^\s*$', np.nan, regex=True)
if st.checkbox("查看原始数据: TouchdownCustomerInformation.csv"):
    st.write(df_Customer)
df_service = service_data.replace(r'^\s*$', np.nan, regex=True)
df_service['合同价格'] = df_service['合同价格'].apply(np.int64)
# if st.checkbox("查看原始数据: serviceData.csv"):
#     st.write(df_service)


st.subheader("1. 签约学员购买服务分析")

# Create a readial chart 
t = alt.TitleParams("远程背景提升的购买情况", subtitle=["图 1.1 Radial Chart"])
base = alt.Chart(df_Customer, title=t).encode(
    theta = alt.Theta("count(远程背景提升):Q", stack=True),
    radius = alt.Radius("count(远程背景提升)", scale=alt.Scale(type="linear", zero=True, rangeMin=20)),
    color = "远程背景提升:N",
    tooltip = ['远程背景提升','count(远程背景提升)']
)
c1 = base.mark_arc(innerRadius=20, stroke="#fff")
c2 = base.mark_text(radiusOffset=10).encode(text="远程背景提升:N")
st.altair_chart((c1 + c2), use_container_width = True)
st.caption("注1: \"远程背景提升\"包含(PTA/SI/第三方)")
st.caption("注2: 数字对应购买远程实习的数量")
st.write("从图1.1中可以看到有大约三分之二的签约学员都购买了至少1段远程实习的项目,这其中大多数同学购买了1段远程实习, \
    也有一部分同学购买了2段远程实习,只有极少数同学选择购买3段远程实习.基于此现状,我们通过怎样的方式可以促进剩下三分一没有 \
        购买任何远程实习的学员去购买这个服务?对于已经购买1段远程实习的学员如何再让其购买一段实习?我们要结合学员的背景状况 \
            做进一步分析.")



# Calculate the percentage 
count = df_Customer['实地背景提升'].value_counts()
# Create lists to store the percentage results
list_percentage = []
for i in range(0, count.size):
    list_percentage.append(((count.iloc[i] / count.sum()) * 100).round(2).astype(str) + '%')
list_index = count.index[:].tolist()
# Create a dictionary to store the percentage
dic_percentage1 = {"实地背景提升":list_index, "占比":list_percentage}
df_percentage1 = pd.DataFrame.from_dict(dic_percentage1)
# Join df_Customer with df_percentage 
df1 = pd.merge(df_Customer, df_percentage1, how="left", on="实地背景提升")

# Create a readial chart 
t = alt.TitleParams("实地科研/实习的购买情况", subtitle=["图 1.2 Radial Chart"])
base = alt.Chart(df1, title=t).encode(
    theta = alt.Theta("count(实地背景提升):Q", stack=True),
    radius = alt.Radius("count(实地背景提升)", scale=alt.Scale(type="log", zero=True, rangeMin=20)),
    color = "实地背景提升:N",
    tooltip = ['实地背景提升','占比']
)
c1 = base.mark_arc(innerRadius=20, stroke="#fff")
c2 = base.mark_text(radiusOffset=10).encode(text="实地背景提升:N")
st.altair_chart((c1 + c2), use_container_width = True)
st.caption("注: 移动鼠标指针以查看具体比例")
st.write("从图1.2可以看到有超过四分之三的签约学员没有购买实地的背景提升服务,购买这项服务的学员大多以购买1段实地实习经历为主,购买 \
    科研以及2段实习经历的总共仅占约4%. 此外,购买实地实习的学员绝大多数都购买了远程实习,由于缺少其购买的具体时间节点,我们推测这 \
        可能是由于学员在经历了远程实习后对此项服务增加了信任度,认为对自身有价值,随后更倾向于购买实地的实习(相较于没有购买 \
            远程实习的学员来说). 如果这个推测成立,那么进一步转化未购买远程实习的学员购买远程实习则可以提高实地实习的购买比例.")



# Create a barchart 
t = alt.TitleParams("语培服务的金额分布", subtitle=["图 1.3 Top K Items"])
barchart1 = alt.Chart(df_Customer, title=t).mark_bar().encode(
    x = alt.X('语培服务金额:N', sort='-y', axis=alt.Axis(labelAngle=45)),
    y = alt.Y('count(语培服务金额):Q'),
    color = alt.Color('count(语培服务金额):Q'),
    tooltip = ['语培服务金额','count(语培服务金额)']
)
st.altair_chart(barchart1, use_container_width = True)
st.write("从图1.3可以看到没有购买任何语培服务(也就是语培服务金额为0)的学员总共有106人,不到总签约数的一半. 对于剩下购买了语培 \
    服务的学员,最受欢迎的语培套餐对应的金额分别为5800,7800和10800. 仅从这3个套餐来看,金额越高相应的购买人数则越少. 但是 \
        从排名第三的10800套餐往后,我们观察到套餐金额和其购买人数并无相关性. 造成这种现象的原因可能是,对于大家并不常选择的套餐 \
            来说,他们的课程设置满足了一小部分人的个性化需求,但是并不适合大多数考GRE的同学,有可能是其服务与金额的匹配度不够高, \
              或者就是要么便宜的套餐(如1499)无法满足正常人的备考需求,要么贵的套餐(11299,19600)超出了正常人的备考需求. 不过 \
                  总体来说宣传策略应更偏向于5800,7800和10800这三个套餐,对其增添\"附加价值\"(如以区域办公室为核心开展线下活动 \
                      )会大概率提升GRE产品的总体销量.")


# Create a scatterplot
t = alt.TitleParams("远程背景服务与语培服务金额的关系", subtitle=["图 1.4 Scatterplot"])
scatterplot1 = alt.Chart(df_Customer, title = t).mark_circle().encode(
    x = alt.X('远程背景提升:Q'),
    y = alt.Y('语培服务金额:Q'),
    size = 'count()'
).interactive()
st.altair_chart(scatterplot1, use_container_width = True)
st.caption("注: 缩放此图以达到合适比例")
st.write("在图1.4中,如果先忽视散点的大小(也就是购买服务的学员人数),则会发现远程背景提升服务的购买金额和语培服务的购买金额 \
    之间并没有很强的线性相关. 但是如果横向对比不同远程背景提升(0~3段)所对应的散点大小则会发现,语培金额为0(也就是没有购买语培 \
        服务)的学员数量随着远程背景提升购买量的增加而减少,甚至于所有购买了3段远程背景提升的学员无一例外都购买了语培服务.  \
            如果将Y轴固定到10000上下的范围,横向比较散点的大小则会发现,学员购买远程背景提升的段数越多,其购买的语培服务金额也 \
                越高. 总的来说,学员购买远程背景提升不光可以减少其不购买任何语培产品的概率,同时还增加了其购买更高价格语培产品 \
                    的概率.")


# Create a time series line chart
# fig = plt.figure(figsize=(10, 4))
# sns.lineplot(x = "签约时间", y = "远程背景提升", data = df_Customer)
# sns.lineplot(x = "签约时间", y = "Col_2", data = df_Customer)
# plt.ylabel("Col_1 ")
# plt.xticks(rotation = 25)
# st.pyplot(fig)
    

# Calculate the percentage 
count = df_Customer['合同类型'].value_counts()
# Create lists to store the percentage results
list_percentage = []
for i in range(0, count.size):
    list_percentage.append(((count.iloc[i] / count.sum()) * 100).round(2).astype(str) + '%')
list_index = count.index[:].tolist()
# Create a dictionary to store the percentage
dic_percentage2 = {"合同类型":list_index, "占比":list_percentage}
df_percentage2 = pd.DataFrame.from_dict(dic_percentage2)
# Join df_Customer with df_percentage 
df5 = pd.merge(df_Customer, df_percentage2, how="left", on="合同类型")
t = alt.TitleParams("签约合同类型的构成", subtitle=["图 1.5 Donut Chart"])
donut2 = alt.Chart(df5, title=t).mark_arc(innerRadius=100).encode(
    theta = alt.Theta("count(合同类型):Q"),
    color = alt.Color("合同类型:N"),
    tooltip = ['合同类型','占比']
)
st.altair_chart(donut2, use_container_width = True)
st.caption("注: null表示学员的合同数据缺失")
st.write("从图1.5可以看到,虽然我们共有超过10种的合同类型,但是学员最频繁选择的只有4种,按顺序分别是全程Max(36.04%), \
    全程Plus(27.48%),全程VIP(11.71%)和全程(9.91%). 这其中又以全程Max和全程Plus为主导地位,二者之和已经占比过半. 全程Max \
        和全程Plus都是2个专业/12所学校,说明大多数学员认为2个专业/12所学校是比较均衡的选择. 占比稍小的全程VIP和全程分别 \
        对应3个专业/15所和1个专业/8所,满足了一部分学员申请学校数量高于/低于12所的需求. 那么是否可以对全程Max和全程Plus \
            产品完善,进一步增强这两个拳头产品的吸引力以达到更多的签约数量.")



# Calculate 所有合同类型带来的营收金额
df_1 = pd.merge(df_Customer, df_service, how="left", on="合同类型")
df_2 = df_1.groupby(["合同类型"], as_index=False)["合同价格"].sum()
df_2['合同价格'] = df_2['合同价格'].apply(np.int64)
df_2.rename(columns = {'合同价格':'单项合同营收'}, inplace = True)
# Calculate the percentage
list_percentage = []
for i in range(0, df_2.shape[0]):
    list_percentage.append(((df_2.iloc[i,1] / df_2["单项合同营收"].sum()) * 100).round(2).astype(str) + '%')
df_2["营收占比"] = list_percentage
# Create a donut chart
t = alt.TitleParams("签约合同的营收状况", subtitle=["图 1.6 Donut Chart"])
donut3 = alt.Chart(df_2, title=t).mark_arc(innerRadius=100).encode(
    theta = alt.Theta("单项合同营收:Q"),
    color = alt.Color("合同类型:N"),
    tooltip = ['合同类型','营收占比','单项合同营收']
)
st.altair_chart(donut3, use_container_width = True)
st.caption("注1: 单项合同营收的单位为元")
st.caption("注2: 此处合同营收仅按照合同本身的价格进行计算,没有包括任何其他附加服务(如语培,实习等)")
st.write("在图1.6中可以看到,营收占比最大的4种合同类型仍然是全程Max(40.26%),全程Plus(24.61%),全程VIP(16.78%)和全程(7.77%), \
    与学员最频繁选择的4种合同一致. 但是具体比例发生了一定的变化,比如全程Max和全程VIP在营收方面的占比要高于他们在合同数量 \
        上的占比,全程Plus和全程在营收方面的占比要低于其在合同数量上的占比. 这种现象是由于全程Max和全程VIP的合同单价 \
            要高于另外两者,其重要性在营收分析上进一步体现. 对于高端合同来说(此处尤指全程Max和全程VIP),他们在数量上占比的些许 \
               提升便能带来营收上的较高收益.")




st.subheader("2. 签约学员背景概览")

# Create a histogram
t = alt.TitleParams("学员GPA的分布状况(4.0 scale)", subtitle=["图 2.1 Histogram with mean"])
base = alt.Chart(df_Customer, title=t)
histogram1 = base.mark_bar().encode(
    x = alt.X('GPA:Q'),
    y = alt.Y('count()'),
    tooltip = ['GPA','count(GPA)']
)
mean_line = base.mark_rule(color='red').encode(
    x = alt.X('mean(GPA):Q'),
    size = alt.value(3.5),
    tooltip = ['mean(GPA)']
)
st.altair_chart((histogram1 + mean_line).interactive(), use_container_width = True)
st.caption("注: 缩放此图以查看细节或整体走势")
st.write("在图2.1中我们可以看到直方图整体呈现为左偏的正态分布,红线为所有学员GPA的均值(3.428). 对于所有的左偏正态分布来说, \
    中位数都要大于均值,所以签约学员GPA的中位数至少要大于3.428. 另外我们观察到一个极值(outlier),即GPA=3.9所对应的有 \
        9位同学,几乎是所有GPA分数段中包含人数最多的. 考虑到整体样本量偏小,那么可能的解释有2种. 一是员工在手动录入学员GPA \
            的过程中未能将所有的数据都以精确到小数点后二位/三位录入,四舍五入了一些3.9开头的数据(比如将3.91,3.92,3.93等 \
                这样的数据输入为3.9). 如果是这种情况,那么将数据精确还原以后我们将得到一个没有极值的左偏正态分布,即 \
                    大部分学员的GPA都分布在高于均值(3.428)的水平上,极高的GPA(如4.0)和极低的GPA(如0 ~ 3.0)所对应的 \
                        人数都较少. 第二种可能就是数据录入是准确的(也就是确实有9位学员的GPA是3.9),那么则说明拓达所签约 \
                            的高GPA(3.9)学员数量要超出正态分布所预测的数量(拓达拥有高GPA学员的概率要更高?).")



# Create a new column and add it to df_Customer
list1 = []
for i in range(0, df_Customer.shape[0]):
    if(df_Customer.iloc[i, 13] == "无"):
        list1.append(0)
    else:
        list1.append(1)
df_Customer["是否购买语培服务"] = list1
# Create a histogram
t = alt.TitleParams("学员GRE成绩的分布状况", subtitle=["图 2.2 Histogram with mean"])
base = alt.Chart(df_Customer, title=t)
histogram1 = base.mark_bar().encode(
    x = alt.X('GRE:Q'),
    y = alt.Y('count()'),
    color = alt.Color('是否购买语培服务:N', scale=alt.Scale(scheme='dark2')),
    tooltip = ['GRE','count(GRE)']
)
mean_line = base.mark_rule(color='yellow').encode(
    x = alt.X('mean(GRE):Q'),
    size = alt.value(3.5),
    tooltip = ['mean(GRE)']
)
st.altair_chart((histogram1 + mean_line).interactive(), use_container_width = True)
st.caption("注: 0表示没有购买语培服务,1表示购买了至少一项语培服务")
st.write("在图2.2中可以看到,学员GRE的成绩同样呈现出左偏的正态分布,GRE分数的均值约为325.4,大部分学员的成绩都集中在320 ~ 325 \
    这个区间段. 此图还展示了是否购买语培服务对学员GRE成绩的影响,但是由于原始数据中GRE的信息录入并不完善(有的同学还没考,无效 \
        数据,或者录入的成绩并非最终成绩等因素),我们很难就此图得出明显的规律. 但整体来看,是否购买语培服务似乎对学员的GRE成绩 \
            影响不大,并没有显著增加学员考高分的概率. 就目前我们所掌握的成绩样本来看,有两个分数段所对应的学员其购买语培 \
                服务的比例要更高,分别是320 ~ 323以及332 ~ 334. 结合之前所提及的数据本身的缺陷,合理的解释可以是: 320 ~ 323 \
                    分数段的学生对于提高分数有更高的需求,所以购买语培产品的比例也随之升高. 332 ~ 334分数段则可以看作是 \
                        语培服务所能带给大多数学员分数提升的一个上限. 不过数据补齐之后的分布状态可能会发生较大变化,则需 \
                            重新分析语培服务对学员分数的影响.")



# Calculate 学员的本科院校所对应的人数, and store the results in a new column 在读大学的学员数量
df2 = df_Customer.groupby(['在读大学'], as_index=False)['客户'].count()
df3 = pd.merge(df_Customer, df2, how="left", on="在读大学")
df3.rename(columns = {'客户_x':'客户', '客户_y':'在读大学的学员数量'}, inplace = True)
# Replace non-numeric values to NaN
df3['在读大学的学员数量'] = pd.to_numeric(df3['在读大学的学员数量'], errors='coerce')
# Remove all rows with NaN in column 在读大学的学员数量
df3 = df3.dropna(subset=['在读大学的学员数量'])
# Convert column to int
df3['在读大学的学员数量'] = df3['在读大学的学员数量'].apply(np.int64)
# Select a subset of df3
df3 = df3.sort_values(by=['在读大学的学员数量'], ascending=False)
df4 = df3[df3["在读大学的学员数量"] > 4]
# Create a barchart
t = alt.TitleParams("学员本科院校的分布状况", subtitle=["图 2.3 Top K Items"])
barchart2 = alt.Chart(df4, title=t).mark_bar().encode(
    x = alt.X('在读大学:N', sort='-y', axis=alt.Axis(labelAngle=45)),
    y = alt.Y('在读大学的学员数量:Q'),
    color = alt.Color('在读大学的学员数量:Q'),
    tooltip = ['在读大学','在读大学的学员数量']
)
st.altair_chart(barchart2, use_container_width = True)
st.caption("注: 上图展示了学员来源最多的前8名海内外院校")
st.write("从图2.2可以看到签约学员来源最多的前3所学校分别是OSU,上海财经大学和PSU,其中OSU的学员数量又几乎等于后两者之和. 对于除了 \
    这三所学校之外的院校,生源数量基本都在个位数徘徊,区别不是很大. 签约学员的在读学校展现出了很强的不均衡性,即排名前3的学校 \
        汇集了最多的生源,而剩下的学校非常零散且生源数量均较少. 由于缺失学校的地域数据,无法做出准确判断,不过从图2.2学员 \
            数量最多的这8所学校来看,美本的学员占比要远高于其他国家学校的学员. 基于此现状,稳住优势明显的前三个学校 \
                (OSU,上海财经大学和PSU)并在此基础上进一步扩大招生优势(线下办公室的配合)应该是我们下一步重点思考的方向.")



# Calculate 
df2 = df_Customer.groupby(['在读major'], as_index=False)['客户'].count()
df3 = pd.merge(df_Customer, df2, how="left", on="在读major")
df3.rename(columns = {'客户_x':'客户', '客户_y':'在读major的学员数量'}, inplace = True)
# Replace non-numeric values to NaN
df3['在读major的学员数量'] = pd.to_numeric(df3['在读major的学员数量'], errors='coerce')
# Remove all rows with NaN in column 在读大学的学员数量
df3 = df3.dropna(subset=['在读major的学员数量'])
# Convert column to int
df3['在读major的学员数量'] = df3['在读major的学员数量'].apply(np.int64)
# Select a subset of df3
df3 = df3.sort_values(by=['在读major的学员数量'], ascending=False)
df4 = df3[df3["在读major的学员数量"] > 4]
# Create a barchart
t = alt.TitleParams("学员在读专业的分布状况", subtitle=["图 2.4 Top K Items"])
barchart2 = alt.Chart(df4, title=t).mark_bar().encode(
    x = alt.X('在读major:N', sort='-y', axis=alt.Axis(labelAngle=45)),
    y = alt.Y('在读major的学员数量:Q'),
    color = alt.Color('在读major的学员数量:Q', scale=alt.Scale(scheme='teals')),
    tooltip = ['在读major','在读major的学员数量']
)
st.altair_chart(barchart2, use_container_width = True)
st.caption("注1: 上图展示了学员数量最多的前10个专业")
st.caption("注2: 在读major的有一些原始数据较为模糊,无法分清是double major或者是minor或者是其他的情况. 潜在的影响就是 \
    可能造成图2.4中以计算机科学以及统计学为major的学员数量偏少.")
st.write("在图2.4中我们看到经济学和金融以绝对的数量优势排在学员在读major的前2名,而且前10名的专业中还有类似于会计,市场营销 \
    传媒等这种泛商科专业,如果将它们也考虑在内,那么拓达的签约学员有相当多的人是商科及相关专业. 在这10个专业中,理工类的专业 \
        只有数学/金融数学,计算机科学和机械工程,而且占比较低. 值得注意的是,由于原始数据的模糊和录入不规范,计算机科学的 \
            学员人数在此图中有可能被低估,还原此因素会将计算机科学的人数抬升至第三名,略高于数学专业的人数.")



 











