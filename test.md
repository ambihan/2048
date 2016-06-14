### 基于PageRank的改进算法在游戏反作弊中的应用

作者：向浩

单位：Tencent

---
### 前言

为了粘住用户，游戏设计者通常会在游戏中设置各种游戏币奖励，玩家可以通过登录、保持在线等方式领取游戏币，对于游戏币可以在各个玩家之间流通的棋牌类端游、手游而言，会存在这样一个“刷游戏币”的问题：一个玩家创建许多账号（俗称“小号”），然后使用打牌等方式把“小号”的游戏币汇聚到若干个账号（俗称“大号”），当汇聚到一定的量之后，然后低价（低于官方价格）兜售游戏币（以输给买家的方式），获取收益。“刷游戏币”现象会极大影响游戏的经济系统平衡，导致游戏币贬值，严重情况下甚至会弄垮整个游戏。

---
### 一、PageRank算法

#### 1.简介

PageRank，网页排名，又称网页级别、Google左侧排名或佩奇排名，是一种由搜索引擎根据网页之间相互的超链接计算的技术，而作为网页排名的要素之一，以Google公司创办人拉里·佩奇（Larry Page）之姓来命名。Google用它来体现网页的相关性和重要性，在搜索引擎优化操作中是经常被用来评估网页优化的成效因素之一。

PageRank通过网络浩瀚的超链接关系来确定一个页面的等级。Google把从A页面到B页面的链接解释为A页面给B页面投票，Google根据投票来源（甚至来源的来源，即链接到A页面的页面）和投票目标的等级来决定新的等级。简单的说，一个高等级的页面可以使其他低等级页面的等级提升。

PagePank算法除了在网页排名中有重要的应用之外，也可以用于学术论文重要程度排名、个人社交影响力排名等类似场景。

#### 2.算法

对于某个互联网网页A来说，该网页PageRank的计算基于以下两个基本假设： 
* 数量假设：在Web图模型中，如果一个页面节点接收到的其他网页指向的入链数量越多，那么这个页面越重要。
* 质量假设：指向页面A的入链质量不同，质量高的页面会通过链接向其他页面传递更多的权重。所以越是质量高的页面指向页面A，则页面A越重要。

假设一个由4个网页组成的群体：A，B，C和D。如果所有页面都只链接至A，那么A的PR（PageRank）值将是B，C及D的Pagerank总和。

`${\displaystyle PR(A)=PR(B)+PR(C)+PR(D)}$`

继续假设B也有链接到C，并且D也有链接到包括A的3个页面。一个页面总共只有一票。所以B给每个页面半票。以同样的逻辑，D投出的票只有三分之一算到了A的PageRank上。

`${\displaystyle PR(A)={\frac {PR(B)}{2}}+{\frac {PR(C)}{1}}+{\frac {PR(D)}{3}}}$`

换句话说，根据连出总数平分一个页面的PR值。

`${\displaystyle PR(A)={\frac {PR(B)}{L(B)}}+{\frac {PR(C)}{L(C)}}+{\frac {PR(D)}{L(D)}}}$`

最后，所有这些被换算为一个百分比再乘上一个系数 `${\displaystyle d}$` 。由于“没有向外链接的页面”传递出去的PageRank会是0，所以通过数学系统给了每个页面一个最小值 `${\displaystyle (1-d)/N} $`：

`${\displaystyle PR(A)=\left({\frac {PR(B)}{L(B)}}+{\frac {PR(C)}{L(C)}}+{\frac {PR(D)}{L(D)}}+\,\cdots \right)d+{\frac {1-d}{N}}}$`

要注意在Sergey Brin和Lawrence Page的1998年原文中给每一个页面设定的最小值是 `${\displaystyle 1-d}$` ，而不是这里的 `${\displaystyle (1-d)/N}$` 。 所以**一个页面的PageRank是由其他页面的PageRank计算得到。不断的重复计算可以得到所有网页的PageRank。如果给每个网页一个随机PageRank值（非0），那么经过不断的重复计算，这些页面的PR值会趋向于稳定，也就是收敛的状态**。这就是搜索引擎使用它的原因。

---
### 二、PageRank改进算法

棋牌游戏中，各个玩家之间的游戏币输赢关系就是一张巨大的有向图，图中节点表示各个玩家，边表示输赢结果，对应于PageRank的两个假设，“刷游戏币”玩家的可疑度也满足以下两个假设： 
* 数量假设：一个玩家，他赢玩家的数量越多，该玩家的可疑度越大。
* 质量假设：其他条件相同，一个玩家的可疑度越大，赢他的玩家的可疑度也会越大。

在上面两个假设的基础上，正常的“骨灰级”玩家和“刷游戏币”玩家的区别并不明显！“骨灰级”玩家跟“刷游戏币”玩家一个致命的不同点是：“刷游戏币”玩家输给的玩家是他的上级号，一般只有一个或几个；而“骨灰级”玩家输给的玩家远远不只几个。

于是在此基础上研究了第三种假设，以区分“骨灰级”玩家和“刷游戏币”玩家，这个假设也是改进的核心：
* **出度假设：其他条件相同，一个玩家输给的玩家数量越小，可疑度越大。**

考虑到实际情况，在使用PageRank算法反作弊时，做了以下2个方面的调整：
##### PageRank值的分配
对于PageRank算法而言，PR值的分配是平均的，对于A->B, A->C链接关系而言，PR值分配情况是：贡献给B、C的PR值都是`${\displaystyle PR(A)/2}$`。如果A输给B 3000游戏币，A输给C 6000游戏币， 则调整后的PageRank值分配情况是：贡献给B的PR值为`${\displaystyle PR(A) \times {1}/3}$`， 贡献给C的PR值为`${\displaystyle PR(A) \times {2}/3}$`。用TotalLoseCoin(TLC)代表输的游戏币总量，LoseCoinTo(LCT)代表输给对方的游戏币数，则A分配给X的PR值为`${\displaystyle \frac {LCT(X)} {TLC(A)} \times PR(A)}$`
##### PageRank值的有效传播
PageRank算法对于PR值的传播都是100%的，即传递给所有指向节点的PR值之和等于该节点的PR值。但是，在我们的应用中，需要考虑一种情况：玩家输的游戏币远小于赢的游戏币，例如玩家A赢了10000000游戏币，输了1000游戏币，这时候把A的PR值全部贡献出去显然不合理，用TotalWinCoin(TWC)，TotalLoseCoin(TLC)分别代表赢和输的游戏币总量，将 `${\displaystyle \frac {TLC(A)} {Max(TWC(A), TLC(A))} \times PR(A)}$`作为传递的有效值更合理。
##### 进一步优化
结合第三个假设，为了“稀释”正常骨灰玩家的PR传播值，我们在此基础上，最终将`${\displaystyle \frac {TLC(A)} {Max(TWC(A), TLC(A))\times L(A)} \times PR(A)}$`作为传递的有效值，然后再按照`${\displaystyle \frac {LCT(X)} {TLC(A)}}$`比例分配。
##### 最终得到的PageRank算法公式为：
`${\displaystyle PR(X) = \left(\frac {LCT(X) \times PR(A)} {Max(TWC(A), TLC(A))\times L(A)} + \frac {LCT(X) \times PR(B)} {Max(TWC(B), TLC(B))\times L(B)} + \frac {LCT(X) \times PR(C)} {Max(TWC(C), TLC(C))\times L(C)} + \,\cdots\right) \times d + \left( 1-d\right)}$`

---
### 三、改进算法在游戏反作弊中的应用

按照改进的PageRank算法，跑过去一天的对局日志数据，结果喜人。
#### 欢乐系列游戏
```sql
CREATE TABLE lab_pagerank_uinrank_happyseries(
    imp_date BIGINT COMMENT '数据时间',
    game_id INT COMMENT '游戏ID',
    uin STRING COMMENT 'UIN',
    total_win BIGINT COMMENT '赢游戏币总量',
    in_degree INT COMMENT '赢的玩家数',
    total_lose BIGINT COMMENT '输游戏币总量',
    out_degree INT COMMENT '输给的玩家数',
    uin_rank FLOAT COMMENT 'PR值',
    total_round INT COMMENT '总对局数',
    winning_rate FLOAT COMMENT '胜率',
    average_roundtime INT COMMENT '平均对局时间',
    ipaddr STRING COMMENT 'IP',
    clienttype STRING COMMENT '客户端类型',
    chghappyenergy BIGINT COMMENT '游戏币变化值',
    happyenergy BIGINT COMMENT '游戏币存量',
    time BIGINT COMMENT '最后对局时间'
)
COMMENT '欢乐系列玩家可疑度排名'
```

##### 欢乐斗地主
```sql
SELECT  * FROM hy_audit::lab_pagerank_uinrank_happyseries WHERE imp_date = 20160613 AND game_attributes = 105 ORDER BY uin_rank DESC
```

##### 视频斗地主

```sql
SELECT  * FROM hy_audit::lab_pagerank_uinrank_happyseries WHERE imp_date = 20160613 AND game_attributes = 131 ORDER BY uin_rank DESC
```

##### 闷抓斗地主

```sql
SELECT  * FROM hy_audit::lab_pagerank_uinrank_happyseries WHERE imp_date = 20160613 AND game_attributes = 218 ORDER BY uin_rank DESC
```

##### 欢乐四人麻将

```sql
SELECT  * FROM hy_audit::lab_pagerank_uinrank_happyseries WHERE imp_date = 20160613 AND game_attributes = 224 ORDER BY uin_rank DESC
```
结果截图：
![image](http://note.youdao.com/yws/public/resource/6b9902948d8d5e585de18ecc1297d9ff/C8B0C78122904ED684013B6628B2B21E)

#### 天天德州
```sql
CREATE TABLE lab_pagerank_uinrank_ttdz(
    imp_date BIGINT COMMENT '数据时间',
    uin STRING COMMENT 'UIN',
    total_win BIGINT COMMENT '赢游戏币总量',
    in_degree INT COMMENT '赢的玩家数',
    total_lose BIGINT COMMENT '输游戏币总量',
    out_degree INT COMMENT '输给的玩家数',
    uin_rank FLOAT COMMENT 'PR值',
    total_round INT COMMENT '总对局数',
    winning_rate FLOAT COMMENT '胜率',
    total_changecoin BIGINT COMMENT '游戏币变化值',
    realcoin BIGINT COMMENT '游戏币存量',
    gentime STRING COMMENT '最后对局时间'
)
COMMENT '天天德州玩家可疑度排名'
```
```sql
SELECT  * FROM hy_audit::lab_pagerank_uinrank_ttdz WHERE imp_date = 20160613 ORDER BY uin_rank DESC
```
结果截图：
![image](http://note.youdao.com/yws/public/resource/6b9902948d8d5e585de18ecc1297d9ff/5D377CC50E2645918B8C925003FBEEB3)

---
### 总结

改进后的PageRank算法适用于各个玩家之间有道具、游戏币输赢关系的游戏：
* 1.判断是否存在刷道具行为；
* 2.根据排名反推游戏作弊特征；
* 3.高效准确地筛选出游戏币、道具“向上汇聚”顶端的“大号”。
