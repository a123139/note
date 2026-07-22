## 资料

小林coding ClaudeCode从入门到精通

#图解Claude code

### 优先级建议

00-09 课全套（上手 + Git + 调试 + 安全 + 项目记忆）10-13课多代理协作架构→ 19/20/21 课团队落地、外部工具集成；

次要学习（看懂思路即可，不用死记语法）14-18 课 Skills、Hook、MCP、SubAgent 配置文件；只理解「技能包、事件自动化」的设计思想，不用背诵 Claude 独有的配置写法。

### 省钱技巧

1.上下文范围

错用法：（加载整个目录所有文件）claude .

正确用法：（只加载你要修改的 2-3 个核心文件）claude main.cpp student.h gradeManager.h。加.`gitignore`排除无用文件：避免编译产物、配置文件被自动读取。启动时只加载必要文件

2.关闭自动执行

不要开启 A全自动模式，每次请求修改文件、运行命令、读取新文件时，都手动审核，只允许必要操作。学习阶段自己手动编译，把精简后报错信息粘贴给 AI，而不是让 AI 反复自动运行、自动改 bug。

3.多会话

一个功能（增删改查，接 CSV 导入），一个会话

4.模型

简单需求（写注释、解释基础语法、改小 bug、生成单函数）Haiku

复杂需求（架构梳理、难排查的编译错误、整体重构）Sonnet

5.优化提问方式

一次把需求说全、报错先自己精简、减少 `/context`、`/help` 工具命令频繁调用，每次调用重新加载系统提示与工具链





## 1.2.

### 新手实验

用C++做一个命令行成绩管理工具。

功能要求:

1.启动后显示菜单，用户通过数字选择操作;

2.能添加学生成绩(输入姓名和分数);

3.能查看所有学生成绩，按分数从高到低排序;

4.能计算并显示平均分、最高分、最低分;

5.数据保存到文件，下次启动自动加载。

项目结构上，分多个文件，不要写在一个main.cpp里。

用CMake构建，编译运行，测试。

增加两个功能:

1.能按姓名搜索某个学生的成绩;

2.能删除某个学生的记录。



按标准 C++ 工程规范生成项目，严格遵循以下要求：

1. 目录分层：src 源码、include 头文件、build 编译目录、CMakeLists 顶层配置；
2. CMake 规范写法，适配 MinGW，完整注释；
3. 代码分文件封装，避免全部写在 main；
4. 输出完整可直接编译运行代码，附带全套构建命令，禁止简化工程结构。

### 按键 命令

A 键

<img src="./assets/image-20260713083620283.png" alt="image-20260713083620283" style="zoom:50%;" />

<img src="./assets/image-20260713083818736.png" alt="image-20260713083818736" style="zoom:50%;" />

<img src="./assets/image-20260713084842314.png" alt="image-20260713084842314" style="zoom:50%;" />



### 基础须知

VS 插件内置独立二进制，**不会调用你 PATH 里的 `claude` CLI 程序**，两者是两套独立进程；

**同一个项目：CLI 和 VS 插件会话互通，历史记录双向可见**。但两者**共用同一套本地存储目录**：Windows `%USERPROFILE%\.claude\`，所有会话、全局配置、API 密钥、代理设置都存在这里。



具体、完整（上下文）描述目标  （不用规定步骤）---->迭代

@引用文件

/model      模型切换

<img src="./assets/image-20260713094844467.png" alt="image-20260713094844467" style="zoom:50%;" />

`extended thinking`:深入推理 alt+t切换开关 首次需要运行/terminal-setup来安装快捷键  ctrl+o详细过程  

多线程相关的bug(竞态条件、死锁)。复杂的类型推导或模板元编程问题。性能分析:为什么这段代码比预期慢。架构决策:A方案和B方案哪个更好。简单任务(比如 帮我写个for循环)Extended Thinking没什么意义。



shift+tab (/plan )  模式切换  

Plan模式：计划分析（不修改） 学习理解阶段，需求大修改多先看方案，复杂难多种解决路径不确定(你会怎么做？列出方案解决步骤)       先规划后执行

帮我看看这个项目的结构，给我一个简要概述:用了什么语言和框架、主要的源文件都是做什么的、入口在哪里。这个项目怎么编译和运行?哪些 TODO或者FIXME没有处理? main.cpp里的函数在做什么?



上下文窗口（session）

/context 查看使用情况

/compact   压缩  重点关键信息（细节丢失）    /compat 保留.....      对话时间长20分钟/出现遗忘/响应慢/新的子任务不需要之前的细节

**claude -new  开启新对话**



/clear  清空

右键粘贴



同一个项目目录下可以创建多条会话，每条对话有唯一`session-id`存储为单独`.jsonl`日志文件。

全局共享信息：

CLAUDE.md (claude.md)：  项目全局规则，所有会话启动都会自动读取。

自动记忆（Auto Memory）：项目级长期摘要，新会话会加载过往会话(提取架构、技术栈、约定规则等精简摘要)作为背景参考，不会完整读取另一条会话。

使用：

`claude`直接启动 / `/new`命令  全新空白会话（会话1系统菜单开发，会话2单独调试 CMake 编译）

`/branch` / `claude --fork-session`  分支会话（基于当前会话**复制完整历史**生成一条全新独立会话；

分叉后两条会话彻底隔离，后续操作互不影响；适合 “试错方案”：原会话保留稳定代码思路，分支会话尝试重构、换算法。）

所有会话文件路径：

```
~/.claude/projects/【项目目录哈希值】/session-【唯一UUID】.jsonl
```

| 文件        | 归属                       | 给谁看       | Claude 读取逻辑                                              |
| :---------- | :------------------------- | :----------- | :----------------------------------------------------------- |
| `README.md` | 通用项目文档（所有人标准） | 人类开发者   | Claude 只会**被动参考**，不会强制遵守；仅当作参考资料，不约束 AI 行为 |
| `CLAUDE.md` | Claude CLI 专属配置文件    | 仅 Claude AI | 强制全局规则，**本项目所有会话自动加载**，约束 AI 编码规范、项目架构、禁止操作、代码风格，多条会话共享同一套约束 |

约束AI   所有 Claude 会话统一编码风格、项目目录结构、禁止踩坑写法 等

教/提示人    写教程、给别人教怎么编译运行项目 → 写进 `README.md`

`/btw` 快速旁问

<img src="./assets/image-20260713100411244.png" alt="image-20260713100411244" style="zoom:50%;" />

### 总结

迭代优化---报错信息直接贴---给claude看现象不是猜测---会话长就新开---超3个(多)文件的修改先Plan

<img src="./assets/image-20260713103750827.png" alt="image-20260713103750827" style="zoom:50%;" />

<img src="./assets/image-20260713110402526.png" alt="image-20260713110402526" style="zoom:50%;" />







## 3.权限版本

### 权限

<img src="./assets/image-20260713133925883.png" alt="image-20260713133925883" style="zoom:50%;" />

<img src="./assets/image-20260713134024694.png" alt="image-20260713134024694" style="zoom:50%;" />

#### `/permission `    允许

''`allow/ask/deny`":  [Bash(命令 可包含*)/Read(路径)/Edit(路径)]

系统会按**deny（最高） > ask > allow（最低）**依次匹配，匹配到任意一条，立刻终止判断，后面列表不再检查。（默认 ask ）

<img src="./assets/image-20260713134855469.png" alt="image-20260713134855469" style="zoom:50%;" />

<img src="./assets/image-20260713134833080.png" alt="image-20260713134833080" style="zoom:50%;" />

<img src="./assets/image-20260713135003166.png" alt="image-20260713135003166" style="zoom:50%;" />

#### 例子：

<img src="./assets/image-20260713184301402.png" alt="image-20260713184301402" style="zoom:50%;" />

<img src="./assets/image-20260713190605290.png" alt="image-20260713190605290" style="zoom:50%;" />

### 版本checkpoint

只跟踪Claude用文件编辑工具(write/Edit)修改的文件。Bash命令不追踪

`claude -c`或`claude--resume`继续对话后，仍然可以回退 。默认30天后自动清理(可配置)



回退: 按`Esc`两次(或输入`/rewind`)打开回退菜单。

会话历史消息列表，选择消息，选择操作

<img src="./assets/image-20260713172217151.png" alt="image-20260713172217151" style="zoom:50%;" />

#### 例子：

![image-20260713183136516](./assets/image-20260713183136516.png)

按下回车键选择 `Restore code and conversation` 回退到**这条指令执行之前** 的状态。**代码层面**撤销本次 `README.md` 的 `+19 -4` 修改，**README 恢复成旧版本**。

Claude Code 的Rewind(回退)没有原生 撤销回退 功能。A→ B → C → D（最新 current），回退到B那么B、 C、D 全部清空。



### git

<img src="./assets/image-20260713172330096.png" alt="image-20260713172330096" style="zoom: 50%;" />



Claude Code 能参与Git工作流（Bash命令）`git diff` `git add``git commit`

一般情况会在权限配置里**禁止**`git push`

做比较大改动时，建议让Claude先创建一个新分支



`git checkout -b 分支名 ` 创建分支 + 切换到新分支

`checkout`：切换分支的基础指令

`-b`：参数含义 **create new branch**

`git branch `      查看本地所有分支,带`*`标记的是当前正在工作的分支。

废弃分支：切回主分支后删除

 `git checkout main ``git branch -D feature/import-csv`

分支开发成功：切回主分支后合并到主分支

`git checkout main ``git merge feature/import-csv`

补充事项：

项目根目录必须提前初始化 Git（执行过`git init`），否则该命令会执行失败；

分支创建前，把当前未保存修改提交：`git add . && git commit -m "保存当前稳定版本"`；

开启 A 自动全部允许编辑后，Claude 会自动修改头文件、源文件、CMake 配置。



**Git worktree** 

1. 普通分支（`git checkout -b`）

不能同时打开「原版代码」和「修改版分支代码」，想同时看两个版本，只能复制整个项目文件夹。

2.Git worktree在同一个 Git 仓库，**创建多个独立文件夹（工作区）**，每个文件夹绑定一个专属分支。

多分支**同时打开、同时编辑、同时编译运行**，互不干扰；共用一套 Git 仓库元数据（`.git`），不重复存储源码省空间；主目录完全干净，实验性改动全部隔离在新文件夹不会污染原项目。

`git worktree add ../grade-manager-experiment -b experiment/sqlite-storage`：创建新独立工作区（和原项目同级目录），自动新建专属分支并绑定到这个新文件夹。（执行后没切换，在旧的目录工作区)

删除废弃 worktree：

`git worktree remove ../grade-manager-experiment`

`git branch -d experiment/sqlite-storage`

`claude --worktree 路径`  打开已经提前建好的 worktree 工作区。

**同时打开 两个终端、进入两个不同的文件夹、分别编译**

独立对话 Session：互相隔离，新 worktree 默认看不到旧分区的会话

项目全局记忆(auto-memory、CLAUDE.md、项目全局配置):同一个Git仓库所有 worktree 全部共享

#### 例子：

```
git worktree add ../grade-manager-experiment -b experiment/sqlite-storage

cd ../grade-manager-experiment
# 进行相关改动操作
# 全部改动提交到实验分支
git add .
git commit -m "完成SQLite存储新功能开发"
# 切回原版主目录（main分支）
cd ../project1_grade-manger
# 把实验分支代码合并进main
git merge experiment/sqlite-storage
# 删除实验worktree关联+本地文件夹
git worktree remove ../grade-manager-experiment
# 功能稳定,合并完成后这个分支使命结束，手动删除本地分支：
git branch -d experiment/sqlite-storage
#后续还需要复用分支迭代,保留分支只删除worktree文件夹，下次要重新创建 worktree
git worktree add ../grade-manager-experiment experiment/sqlite-storage
```



### 小结

Claude大规模修改前，先发一条简单的消息，Checkpoint记录改动前状态。可以回退。

敏感操作用`deny `保护，至少要配这两条禁止`Bash(git push *)``Bash(rm -rf *)`

Checkpoint 不覆盖 Bash ，只覆盖Claude的文件编辑工具Write/Edit的操作

<img src="./assets/image-20260713191307477.png" alt="image-20260713191307477" style="zoom:50%;" />





## 4.工具

### agentic loop

agentic loop  思考一执行一看结果一修复一再执行

三阶段划分:收集上下文----采取行动----验证结果

Claude Code是一个**agentic harness(智能体执行框架)**。本身不是AI模型，是套在模型外面的**一层执行环境**一一提供工具、管理上下文、处理权限、驱动循环。

模型负责**推理**，工具负责**行动**。

### 内置工具

完整工具列表  `/config`-->`Settings`

工具权限可在`/permissions`里设置

##### 文件操作

`Read`  

`Edit`   

`Write`  

 `NotbookEdit`  编辑Jupyter Notebook单元格,用Python做数据分析。

##### 搜索类

`Glob`   **文件名**模式搜索（text_开头/.cpp结尾）

`Grep`   **内容正则**搜索（找出所有包含TODO的行）

##### 执行类

`Bash ` shell命令（CLI命令行可执行的命令）

`EnterPlanMode/ExitPlanMode `  进入/退出  Plan 模式
`EnterWorktree/EnterWorktree`   创建和退出 Git Worktree  

##### Web类

`WebSreash`  搜索互联网（询问一些信息  可能会联网查找最新消息）

`WebFetch`   抓取URL内容（新消息 抓取下来）

##### 代码智能类

`LSP`  通过语言服务器获取代码智能信息一类型错误、编译警告、跳转到定义、查找引用、符号列表等。Claude每次编辑文件后会自动检查有没有引入新的类型错误。这个工具需要安装对应代码智能插件去能用。

##### 其他工具

`agent`  子代理，独立上下文窗口
`TaskCreate / TaskList / TaskUpdate / Taskstop / Taskoutput `    管理后台任务
`AskuserQuestion`   向你提问。遇到需要用户决定的情况(比如  函数要用方案A还是方案B?)，用这个工具向你提问。



### 扩展层

##### `CLAUDE.md `   

**Markdown文件**，**每次启动**会话都会**读取**（项目的技术栈、编码规范、构建命令、注意事项）

有一套分层的记忆体系。

企业策略级(Managed Policy)

项目级(./CLAUDE.md 或./.claude/CLAUDE.md）团队共享，提交到git

用户级(~/.claude/cLAuDE.md) 个人偏好，所有项目共享

规则目录(.claude/rules/*.md):按文件路径加载不同规范


##### `Skills`

**按需加载**的知识和流程。本质上是一个**Markdown文件**

会话开始时只看到Skill的名字和简短描述，只有被用到时才加载完整内容
**手动触发/自动触发**

Claude Code自带了一些内置 Skill，` /simplify`(简化代码)、`/batch`(批量操作)、`/debug`(调试辅助)，也可以自己创建，通过`/skills`命令看自己创建的

OpenClaw的Skill市场一ClawHub。一个社区驱动的Skill仓库，覆盖编码、DevOps、浏览器自动化、搜索调研、生产力工具等各种场景。可以用一条命令直接**安装别人写好的Skill**:
`clawhub install @author/skill-name`



##### `Sub-Agents`

Sub-Agents(子代理)是**隔离执行的工作单元**。

拥有**独立上下文窗口**，不能嵌套创建，可以在前台或后台运行，只**返回结果**给主Claude不保留中间过程（可以指定子代理 工具权限）

Claude Code内置子代理：

Explore:探索代码库结构。适合「帮我看看这个项目的目录结构和核心模块」这类任务。

Plan:制定方案。适合「分析一下怎么重构这个模块」这类需要深入思考的任务。

General-purpose:通用子代理。可以通过提示词让Claude 创建临时子代理。



##### `Hooks`

事件驱动的**自动化脚本**（纯确定性）

shell 脚本(也支持HTTP端点和 LLM prompt)，**特定事件发生自动执行。**

官方18种Hook事件，常用几种:

PreTooluse:使用某个工具之前触发。比如每次Edit 前先格式检查。

`PostTooluse`:使用某个工具之后触发。

`Notification`:发出通知时触发。比如收到通知后转发到飞书或钉钉。

`stop`:完成任务(停止循环)时触发。比如任务结束后自动生成一份报告。

`Sessionstart/SessionEnd`:会话开始和结束时触发。

`Subagentstart/subagentstop`:子代理启动和完成时触发。

`InstructionsLoaded`:用来排查指令加载问题。

**Hooks不走AI推理，不耗费token，执行结果确定。**



##### `MCP`

Model Context Protocol模型上下文协议，**连接外部服务**（**扩充工具**）

本质是一个协议标准，定义了Claude怎么和外部工具通信。配置一个MCP Server告诉Claude「有一个数据库，你可以用这些命令查询它」Claude就多了一个工具。

MCP Server可以配在项目级(对项目生效)或用户级(所有项目共用)

现象：MCP工具的定义(名称、描述、参数schema、示例)都要**占用模型上下文窗口**token，接多了token消耗大。不如使用传统的API和 CLI。



##### `Agent Teams`

组一个团队大家各干各的互相交流。每个Agent都是**独立的Claude Code会话**，之间可以**互相**发消息、共享任务列表、自主协调分工。

**任务复杂**到需要**多个视角同时**推进、且需要互相讨论的时候。

比如三个Agent 安全审查、性能分析、代码风格检查，互相交流 安全审查的Agent发现可疑点，性能分析的Agent说 确实有问题我这边看到了性能瓶颈

功能目前是实验性的，默认关闭，需要手动开启。



##### `Plugins`

一种**打包机制**![image-20260714151929247](./assets/image-20260714151929247.png)

Plugin支持版本化和分发。

发布方式: 创建一个「Marketplace目录」，本质上是托管在GitHub 上的**Git 仓库**，里面有一个marketplace.json 文件，列出你所有的Plugin及其来源。在地验证没问题推上GitHub，团队成员用一条命令即可添加` /plugin marketplace add your-org/team-plugins`
就能浏览和安装你的Plugin。你更新Plugin后推送到GitHub，成员用`/plugin marketplace update `就能同步最新版本。



##### 总结

<img src="./assets/image-20260714152843611.png" alt="image-20260714152843611" style="zoom:50%;" />

判断: **是否需要AI判断** 和 **加载频率**

需要AI判断+每次都用写进CLAUDE.md 。

需要AI判断+按需Skills或Sub-Agents。

不需要AI判断+固定触发Hooks。

需要连外部系统MCP。

需要多视角讨论Agent Teams。

需要打包分享Plugins。

<img src="./assets/image-20260714153609334.png" alt="image-20260714153609334" style="zoom:50%;" />

<img src="./assets/image-20260714153707386.png" alt="image-20260714153707386" style="zoom:50%;" />



### 小结

Claude 说没有某个工具，可能版本太旧或者某些工具需要额外配置(比如LSP 需要安装代码智能插件)。用/doctor 诊断一下。

简单任务用了很多步骤，你觉得不必要在提示词「直接改就行，不用先分析整个项目」

<img src="./assets/image-20260714163854024.png" alt="image-20260714163854024" style="zoom: 50%;" />



## 5.记忆系统 

![image-20260714165655105](./assets/image-20260714165655105.png)

### CLAUDE.md

（给新人的入职手册）

##### 作用域 层级

**企业**  `C:\Program Files\claudecode\cLAUDE.md` 安装的地方

**项目**  项目根目录`./CLAUDE.md`或`./.claude/CLAUDE.md`  团队共享的项目知识应该提交到Git团队成员共用，是最常用的一层。

**个人**   `~\.claude\CLAUDE.md`  ~当用户家目录（用户根文件夹`C:\Users\.claude`\CLAUDE.md）

在项目的子**目录里启动**ClaudeCode，自动加载CLAUDE.md，**向上加载上所有**，**向下读到**子目录文件**时按需加载**。

##### 示例：

![image-20260714170500911](./assets/image-20260714170500911.png)

##### .claude/rules/

拆分多个`专项.md`文件（path[ 多个文件名]），**读到** 匹配文件 时**才加载**对应`专项.md`。没设path和主CLAUDE.md一样启动时加载

<img src="./assets/image-20260714171513245.png" alt="image-20260714171513245" style="zoom:50%;" />

<img src="./assets/image-20260714171732592.png" alt="image-20260714171732592" style="zoom:50%;" />

<img src="./assets/image-20260714171829869.png" alt="image-20260714171829869" style="zoom:50%;" />

##### 符号链接

<img src="./assets/image-20260714172103874.png" alt="image-20260714172103874" style="zoom:50%;" />

##### @引用

`@path ` 引用文件，**用到时才加载**（path：绝对路径/相对路径）

```
CLAUDE.md
[...团队规范...]

#1.项目中包含的
参考 @README.md了解项目概况
参考 @package.json了解可用的 npm命令
API 规范见 @docs/api-spec.md

#2.个人偏好中的
#CLAUDE.md提交到git上时，没有这一条（只在我电脑上有）
@~/.claude/my-project-notes.md
```

##### 编写规则

**Less** is More，官方建议每个CLAUDE.md 文件控制在**200行以内**。

**具体**优于泛泛。

why/what/how 为啥这样做/什么能做什么不能做/怎样步骤做。

结合  **@引用 和   .claude/rules/**(条件规则 用到path内才加载）

<img src="./assets/image-20260714195003987.png" alt="image-20260714195003987" style="zoom:50%;" />

##### 排除不想要的

![image-20260714195643079](./assets/image-20260714195643079.png)

### Auto Memory

(新人工作一周后自己的经验总结）

Auto Memory完全**由Claude管理**（判断哪些信息值得记录，**自动**保存）

存储位置 : `~/.claude/projects/<project>/memory/多个.md`，\<project>由Git仓库推导来，**同一个Git** 下的所有worktree和子目录**共享一个**记忆目录。如果没Git仓库，则用项目根目录路径。

**`MEMORY.md`入口文件**，会话开始时**自动加载前200行**，后续的按需取加载

**子代理**也可以维护自己的Auto Memory。

界面有"Writing memory" 或"Recalled memory" 提示，说明 Claude
正在写入或读取自动记忆。

可以手动触发去记忆到Auto Memory。对话中说[ 记住某件事 ]

### /init

自动**生成CLAUDE.md**。分析代码库，扫描项目结构、识别技术栈、找到构建命令和测试命令，然后把这些信息整理成CLAUDE.md。

已**有**CLAUDE.md，给出**建议改进**。

### /memory

列出当前会话**加载的**所有记忆文件  

所有层级`CLAUDE.md `、`rules `文件(不一定会显示)、`Auto Memory`。

查看加载的文件，**直接打开编辑**，开/关Auto Memory

提示:如果需要排查哪些指令文件被加载、什么时候加载、为什么加载，可以用`InstructionsLoaded `Hook来记录日志。

<img src="./assets/image-20260714173808829.png" alt="image-20260714173808829" style="zoom:50%;" />

### 总结

**CLAUDE.md 放规则，Auto Memory 放经验**

写Claude不可能自己猜到的信息（项目用什么框架、构建命令是什么、团队有什么特殊约定）

只要某条规则不是每次都需要，扔到.claude/rules/里加个 paths 条件。

新项目第一步就跑/init，能给你一个框架。

定期审查你的记忆文件（过时规则比没有更糟糕会误导 Claude）

![image-20260714200238342](./assets/image-20260714200238342.png)



## 6.调试

### 调试

编译、运行后  出现bug  然后才去调试  **修bug（被动的）**

Claude code调试 核心步骤：**描述现象---Claude 定位---修复---验证**

1.完整报错信息，no猜测

2.read grep bash复现错误  分析

3.edit 

4.重新编译、运行    **给出验证方法**（通过测试、截图、预期输出）好提示词会给出**验证步骤**（`Prompt`:xxx，定位并修复，修完之后重新编译运行，确认不再崩溃）

### 错误

##### 1.编译错误

最好处理报错信息明确、位置精准、修起来快。

**给完整**编译输出不要只截关键，模板展开、调用链上下文在上面几行。有多个编译错误**先修第一个**，后续错误可能是连锁反应。告诉Claude编译命令(cmake--build build)，修完后直接编译**验证结果**。

`Prompt`:

编译报错了，帮我修改。修完之后运行cmake --build build 确认编译通过。完整报错如下[粘贴编译输出]

##### 2.运行时崩溃

常见表现Segmentation fault、Abort、未捕获的异常等。

能稳定**重现**的操作、原始报错、如何编译运行。重现步骤尽量具体，把你做过的操作都列来。有核心转储(core dump)，可以把相关信息给Claude分析。对C/C++程序，**Debug 构建， -g，Address Sanitizer** (-fsanitize=address )能让崩溃原因更清晰。

`Prompt`:

编译正常，运行到一半崩溃。重现步骤:  运行 `./build/grade_manager`，输入3个学生信息后「删除学生」输入不存在学生ID，程序崩溃。报错：`Segmentation fault(coredumped)`。修完之后用同样的步骤验证不再崩溃。编译命令:` cmake -B build -DCMAKE_BUILD TYPE=Debug && cmake --build build`。

`Prompt`:(进阶)

在` cMakeLists.txt` 里加上 `Address Sanitizer (-fsanitize=address)`重新编译后运行,根据ASan报告定位并修复问题。

##### 3.逻辑错误

最难调程序不崩溃、不报错，但结果不对。

说清 期望输出 和 实际输出。要说「**我期望X，实际Y**」给够业务上下文，让Claude**加打印**逐步缩小范围

`Prompt`:

grade_manager 平均分计算有问题。输入了90,85,78三个成绩，平均分应该是84.33，但程序显示0。不崩溃，也没有报错。帮我在计算平均分的相关函数里加调试输出，看中间变量的值，定位问题后修复，并用上面的输入去验证输出是否正确。

##### 4.复杂bug

`Extended Thinking` 默认开启，Ctrl+o看思考过程，复杂bug建议开着盯着看（简单问题可 alt+A关闭/cofig调整）

推理深度effort level  Iow、medium、high等（ultrathink一次high）

切模型 opus、opusplan、sonnet

### 总结

完整报错（片段）、原始现象（猜测）、问题能重现步骤（bug不能稳定重现，可能是未初始化、竞态、依赖外部状态等问题）、用@缩小范围、/btw旁问、用管道把日志给claude（报错在文件中 终端 `cat build-error.txt|claude-p "帮我分析这个编译错误，给出修复建议"`）、一个bug一个会话（卡了三四轮没解决，总结（常试、排除），`/clear`开新会话写入总结）、加调试日志、缩小范围、追踪调用链、大范围搜读一>子代理、知道文件@、修完bug要验证  、opusplan先分析再改、善用Checkpoint。

`Prompt`:修完后用 某某命令 编译/运行/跑测试验证

`Prompt`: 跑测试(cmake --build build && cd build && ctest)，把失败测试修到全部通过。

`Prompt`:帮我在 processGrades 函数的每个**关键步骤加上调试输出**，打印输入参数、中间变量、返回值。运行一遍看输出，再根据输出**定位问题**，修复后删掉调试日志。

`Prompt`:calculateAverage 返回了0，但我不确定是它算错了还是调用方传参不对。请从main开始**追踪**到calculateAverage 的**调用链**，标出每一步的关键变量值是否合理。

`Prompt`:用子代理调查calculateAverage在项目里的所有调用方，看有没有可能传入空容器或未初始化数据的情况，把结论汇总给我。



![image-20260714234023811](./assets/image-20260714234023811.png)

## 7.测试

#### 基础知识

**黑盒**：**不看代码内部逻辑**，只测输入输出、业务功能是否符合需求。

等价类划分、边界值分析、场景法、错误推测法

例：单元测试以外大部分场景。接口测试、页面功能、业务流程、系统整体验收

**白盒**：**完全看源码、程序内部逻辑、分支、循环、变量**，基于代码路径设计用例。

语句覆盖 → 判定覆盖 → 条件覆盖 → 判定条件覆盖 → 路径覆盖

例：单元测试（GTest 就是白盒）、底层核心模块、安全审计

**灰盒**：**看部分**代码 / 接口文档，不完整细读源码。

例：后端接口测试，看接口参数文档，但不看底层 C++ 实现代码。

#### 测试

功能性能测试 提前发现问题 **防bug（主动的）**

claude 写测试的流程：

找没被测试覆盖的代码

生成测试的框架结构

补上有意义测试用例(边界条件)

跑测试修改失败的**直到测试成功**



**测试行为而非内部实现。**

**正常路径、边界情况、异常情况。**

**先写测试再写代码。**测试驱动开发(TDD)的思路  先定义行为，再写代码让它变成对的。官方推荐的`Writer/Reviewer`双会话模式：一个会话写测试，一个会话写代码让测试通过。

测试驱动修复: 发现bug---先写测试复现bug---Claude修---测
试自动验证。（跑全部测试才能确保没有回归，没引入新bug）



新建的CLAUDE.md中写上（测试相关）

<img src="./assets/image-20260719112030355.png" alt="image-20260719112030355" style="zoom:50%;" />

可以在项目的 CLAUDE.md里加一条规则，自动遵守：

```
##工作流规则
-代码修改后必须运行 cd build && ctest --output-on-failure 确认测试全过
-新增功能必须添加对应的测试
```

给已有代码补测试，先找覆盖缺口，按优先级分批补测试、考虑未覆盖到/边界/异常 情况。



测试颗粒度及策略

<img src="./assets/image-20260719133003725.png" alt="image-20260719133003725" style="zoom:50%;" />

EXPECT_EQ 断言，失败了**继续跑**后面的测试。

ASSERT_EQ 断言，失败了直接**终止**当前测试函数。



#### 总结

让 Claude参照已有测试的风格。

把 跑测试 **写进 CLAUDE.md**。每次改完自动跑测试。

一次只测一批代码。

测试要能在CI里跑（测试必须是自动化的、不依赖人工交互的、不要手动输入的测试。）

提示词：

完成一个目标立即测试，测试通过后再进行下一目标，**循序渐进**。

关联的类完成后，立即进行一组测试，检查某个类、功能接口的测试是否覆盖了所有接口、边界情况，如果存在边界条件模糊时提醒我，由我评估后确定约束边界，并确定测试方式。

![image-20260719142244411](./assets/image-20260719142244411.png)



## 8.阅读和重构

代码阅读过程  Claude先用**`Glob `**看目录结构搞清楚项目布局，再用**`Grep`** 搜索关键词定位到具体文件，然后用**`Read `**读取文件内容理解逻辑。如果需要了解代码演变，还会用 **`Bash`** 跑`git log``  git blame`。

用 @ 引用文件/目录（**自动加载**该文件所在目录及父目录中的CLAUDE.md，自动获得相关**约定**）

`/plugin`安装代码智能插件。（纯文本搜索搞混，插件能区分`init() `调用`AuthManager::init()`, 不是` DatabasePool::init()`）

#### 阅读

**1.项目概览。全局--局部**

代码库整体概览，用了什么技术栈，做什么，目录结构组织，入口，
追问更具体的方向:架构模式、核心的数据模型、之间关系、项目特有的概念及含义的术语表、编码规范、构建工具、
**2.定位关键代码。（局部里面按优先级找重点核心）**

功能 ：找到用户登录相关文件，配合调用关系图。

文件：引用

错误：错误信息中函数名和文件名，定位问题的代码

关键词： 

**3.追踪执行流程**

正向追踪: 从入口到结果，追踪函数调用链。追踪 用户提交订单 完整流程。

反向追踪: 从结果到原因。数据库里多了脏数据，反向追踪。

跨模块追踪：

**4.理解设计决策**

为什么这么做？ git历史看版本演变，理解技术选型、设计决策。

**5.建立心智模型**
Prompt:基于刚才讨论，用简洁文字描述，给我项目架构总结。包括:核心模块、依赖关系、数据流向、关键设计决策。（术语表、重要文件职责、模块依赖图）

##### 技巧

`/btw`，子代理，大型项目（分模块、分会话、`/compact`、`/init`）

#### 重构

命名优化、函数拆分、模块抽取消、除重复代码、现代化改造

**探索---计划---实现---验证**

**先Plan**模式下探索分析（要重构的代码）分析报告

计划方案，不断讨论调整，**`Ctrl+G`可编辑**修改**计划**。

**分批执行**，每一步都编译或跑测试

跑一遍完整的测试套件（现加测试在重构代码）

##### 技巧


小规模重构(改名字、拆一个函数)直接做就行。

大规模重构（十几个文件、几百行改动），**有测试再重构、先Plan、分批提交改动并验证**(可精确回退)、用Worktree隔离工作区(实验)、Checkpoint回退。

#### 审查

审查当前改动 `git diff`

审查整个文件 @文件

用子代理做批量审查

自动化代码审查(进阶)

#### 总结

<img src="./assets/image-20260719155832960.png" alt="image-20260719155832960" style="zoom:50%;" />

## 9.git

#### PR

PR（Pull Request）是代码审核协作流程，是一套上线审核流程。

已经 `git push` 把分支传到远程了，**PR** 是**上传之后额外的流程**。

1. 本地 merge 后 push（单人自用 / 个人仓库适合）。没有审核流程

2. PR 的标准团队流程  在dev写完代码，推远程，创建PR，申请把dev合进main。团队人在线查看你的全部改动，提修改意见，改完再推送 dev，审核通过后，在网页端合并。

<img src="./assets/image-20260719162103952.png" alt="image-20260719162103952" style="zoom:50%;" />

#### Worktree

**Worktree** 提供Git级别隔离实验环境。同一个Git历史，多个独立工作目录有自己的文件和分支。一个worktree开发新功能，一个worktree  修bug。

启动时加参数`claude --worktree feature-auth` (`.claude/worktrees/feature-auth/`)

注意:--worktree要求仓库至少有一次commit。如果刚跑完 git init，还没提交过会报错，先`git add .&&git commit -m"initial commit"`

提示: 建议在`.gitignore` 里加上`.claude/worktrees/`。

#### 项目

<img src="./assets/image-20260719164247908.png" alt="image-20260719164247908" style="zoom:50%;" />

##### 初始化搭建

创建目录结构、配置构建工具、写README、配置CI、设置gitignore。

Prompt:帮我创建一个C++项目，要求:项目名task-tracker；

用CMake 构建；集成 Google Test;

目录结构src/include/tests/docs/；添加 .gitignore(忽略build/目录和IDE配置文件);

写一份基础的 README.md；初始化Git仓库，做一个initial commit。

##### 已有项目补齐配置

##### 生成CI配

#### 会话管理

会话命名 `/rename`、恢复历史会话`claude -resume [会话名称]`、一个任务一个会话、多任务同时推进(worktree)

#### 总结

commit 规范写进CLAUDE.md、分批commit提交、会话起名字、worktree实验

<img src="./assets/image-20260719164455480.png" alt="image-20260719164455480" style="zoom:50%;" />

## 10.Sub-Agents

### 特点

独立上下文窗口、不能嵌套生成

隔离、约束、复用（软件工程命题:内存管理、安全边界、组织效率）

隔离  **记得更少，但记得对**

约束  精确**工具权限控制**

<img src="./assets/image-20260722160656620.png" alt="image-20260722160656620" style="zoom:50%;" />
复用   子代理**配置保存在文件**Markdown(YAMLfrontmatter +Markdown 系统提示词)
<img src="./assets/image-20260722160841329.png" alt="image-20260722160841329" style="zoom:50%;" />

### 内置类型

Explore（探索者）  只读Read、Grep、Glob，没有写权限

Plan（规划者） 多步骤任务的规划  只读

General-purpose（通用型） 读写都有

### 适用场景
**高噪声输出**— 会产生大量中间输出，丢给子代理避免污染主对话

角色**边界必须明确**— 例如"只做安全审查，别改代码"

可**并行**展开的研究型任务 — 同时探索多个模块，互不干扰

可拆成**流水线**任务 — 规划→实现→审查，每个阶段交给不同的子代理

不适用子代理场景：简单的单步操作，启动子代理本身有开销。需要频繁来回确认需求、不断调整方向的任务。各个阶段高度耦合的任务。延迟敏感的场景，每次启动要从头收集上下文有启动时间。
（/btw+子代理配合用效果最好）

### 子代理配置文件

子代理**配置文件Markdown** 文件。

**YAML frontmatter定义元数据，系统提示词。**

YAML frontmatter三条短横线---包起来，YAML格式键值对，定义了子代理**是什么+能做什么**。系统提示词决定**怎么做**

#### 例子：

<img src="./assets/image-20260722162330467.png" alt="image-20260722162330467" style="zoom:50%;" />

#### 字段

<img src="./assets/image-20260722163024075.png" alt="image-20260722163024075" style="zoom:50%;" />

**description  做什么+什么时候用**。proactively--这个词鼓励Claude在合适的时机主动委派任务。

tools / disallowedTools 允许和禁用的工具列表 

permissionMode 权限模式控制

skills 预加载技能包  **要显示列出在md中**

### 存放位置

![image-20260722163902733](./assets/image-20260722163902733.png)

### 创建方式

1.交互式创建

Claude Code里输入/agents，Create new agent，选存放位置，Generate with Claude，描述子代理功能，Claude帮你生成系统提示词（按e编辑器里微调），工具权限，模型，背景色(方便在UI里区分)，保存。

2.手写配置文件
` .claude/agents/`或`~/.claude/agents/`下创建 Markdown 文件。
手动添加了文件需要重启会话或/agents 命令重新加载。

3.CLI参数临时创建
`--agents`参数传JSON，启动时定义子代理,仅当前会话有效会话结束消失。

<img src="./assets/image-20260722164501122.png" alt="image-20260722164501122" style="zoom:50%;" />

### 运行模式

前台会阻塞主对话。（好处确认权限或回答问题，可以直接交互）

后台不阻塞主对话。（启动前一次性请求所有可能需要的权限）

直接说:在后台跑这个任务

已经在前台运行，按ctrl+B 切到后台

### Resume

子代理完成后有agent ID。如果需要在之前的基础上工作，可以恢复。

子代理的会话记录持久化存储在
`~/.claude/projects/{project}/{sessionId}/subagents/` 目录下,默认保留30天，之后自动清理。

### 小结

<img src="./assets/image-20260722165229546.png" alt="image-20260722165229546" style="zoom:50%;" />

## 11.子代理设计

![image-20260722170522702](./assets/image-20260722170522702.png)

### 代码审查

<img src="./assets/image-20260722170838145.png" alt="image-20260722170838145" style="zoom:50%;" />

<img src="./assets/image-20260722170859228.png" alt="image-20260722170859228" style="zoom:50%;" />

### 影响面分析

<img src="./assets/image-20260722171322894.png" alt="image-20260722171322894" style="zoom:50%;" />


PpermissionMode:plan 提供双重保障。

Skill预加载领域知识 chain-knowledge(链路拓扑和SLA约束)和recent-incidents(近期事故记录)。

### memory字段

类似于子代里中用于保留记忆的（CLAUDE.md/auto.md)

Agent 独立内存域

内存作用：子代理长期沉淀经验，记住项目规范、常见错误、代码风格。

三种内存模式

- `memory: session` 会话内存：仅当前对话有效，关闭清空
- `memory: project` 项目内存：**永久绑定当前项目目录，所有会话共享**
- `memory: global` 全局内存：本机所有项目通用

<img src="./assets/image-20260722172728865.png" alt="image-20260722172728865" style="zoom:50%;" />

### 小结

![image-20260722172925417](./assets/image-20260722172925417.png)

## 12.多代理协作

接手新的大型项目---并行

修复辅助bug---流水线

信噪比

### 并行

多个子代理**互不依赖、同步启动**，各自**独立**执行任务，互不等待。

 能否独立完成？

遗漏跨模块关联是否可接受（主对话综合补充）？

子任务的输出粒度是否匹配（模块级概览，还是混着文件级和函数级）?

##### 测试运行器

<img src="./assets/image-20260722190904210.png" alt="image-20260722190904210" style="zoom:50%;" />

##### 日志分析器

<img src="./assets/image-20260722191126661.png" alt="image-20260722191126661" style="zoom:50%;" />

### 流水线

被切分成前后依赖有序步骤，上一个代理输出作下一个代理输入依次执行。

主对话是编排者负责：触发每个阶段子代理，审查每个阶段输出，判断任务是否继续推进，在阶段之间插入人工判断、人工审批

#### Bug修复流水线

把任务拆分成有序阶段：**定位 → 分析 → 修复 → 验证**

<img src="./assets/image-20260722191952650.png" alt="image-20260722191952650" style="zoom:50%;" />

示例链路：`Locator（问题定位） → bug-analyzer（根因分析） → bug-fixer（代码修复） → bug-verifier（验证测试）`

<img src="./assets/image-20260722192355200.png" alt="image-20260722192355200" style="zoom:50%;" />

<img src="./assets/image-20260722192815876.png" alt="image-20260722192815876" style="zoom:50%;" />

<img src="./assets/image-20260722192845613.png" alt="image-20260722192845613" style="zoom:50%;" />

<img src="./assets/image-20260722193002118.png" alt="image-20260722193002118" style="zoom:50%;" />

#### 交接

阶段之间的信息传递。每个子代理的输出里都有一个「Handoff」部分，提供足够的信息，让下一阶段无需重复上一阶段的工作。
<img src="./assets/image-20260722193554698.png" alt="image-20260722193554698" style="zoom:50%;" />
<img src="./assets/image-20260722193635704.png" alt="image-20260722193635704" style="zoom:50%;" />

#### 编排策略

1.全自动

Locator → Analyzer → Fixer → Bug-verifier，自动流转全程无人干预。

2.关键阶段审批

Analyzer（根因分析）后，人工确认没问题，再启动 Fixer 修改代码。

`Analyzer → Fixer` 只读→写，一旦 Fixer 开始改动回滚成本高

3.逐阶段审批

每完成一个阶段审批一次。

4.回退重试

修复方案出错时，退回【分析阶段】重新推导根因，复用前面定位结果。

#### Resume 

流水线越长，中断风险越高。Claude Code通过 `agent ID` 实现**断点续跑**。

会话中断后，执行 `claude --resume` 恢复会话，前面 Locator、Analyzer 的历史结果会保留在主对话，直接从中断的 Fixer 阶段继续执行，不用全部重来。

### 混合

并行+流水线

<img src="./assets/image-20260722193823195.png" alt="image-20260722193823195" style="zoom:50%;" />

<img src="./assets/image-20260722193916355.png" alt="image-20260722193916355" style="zoom:50%;" />

<img src="./assets/image-20260722194019790.png" alt="image-20260722194019790" style="zoom:50%;" />

### 输出格式设计原则


结论先行（第一眼就知道结果）

可操作性（每条信息都能直接指导下一步行动）

分层详略（全通过极简，少量失败展开每一项,大量失败按类别归组）

为下游消费设计（输出可能被下一个子代理用来做后续决策，想好拿到这个输出后能不能直接用？如果拿到报告后还得重搜一遍，说明输出格式设计不好）


### 选择

![image-20260722194109243](./assets/image-20260722194109243.png)

### 小结

![image-20260722194144027](./assets/image-20260722194144027.png)

## 13.Agent Teams

代理之间能够直接交流、互相挑战、协作推进。

![image-20260722194346558](./assets/image-20260722194346558.png)默认关闭，需要手动启用。

在settings.json 里添加环境变量:

`"env":{"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS":"1"}`

或者在终端里临时设置:

`export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
<img src="./assets/image-20260722195320758.png" alt="image-20260722195320758" style="zoom:50%;" />

#### 任务

共享任务列表是团队协调的核心。任务有三种状态:pending(待领取)、inprogress(进行中)、completed(已完成)。任务还可以声明依赖，任务完成后，被阻塞的任务自动解锁。任务认领用文件锁防止竞态条件。

任务分配有两种方式:
Lead 指派:Lead把特定任务分配给特定 Teammate

自主认领:Teammate完成手头任务后，自动从任务列表里认领下一个未分配、未阻塞的任务

#### 关闭团队

工作完成后，让Lead关闭团队。Lead会向每个Teammate 发送关闭请求。Teammate 可以批准(优雅退出)或拒绝(解释为什么还没做完)。全部Teammate关闭后，Lead清理共享资源。（清理只能由Lead执行）

#### 协作模式

##### 竞争假设

适用场景:根因不明确，需要从多个方向同时验证。
让多个Teammates各自持有不同假设，要求它们互相挑战、试图推翻对方的理论。单个调查者容易产生锚定效应，找到一个合理解释后就停止探索。顺序调查更严重，一旦第一个理论被探索，后续调查会不自觉地偏向它。

`Prompt`:用户报告应用在发送一条消息后就退出了，而不是保持连接。创建一个agentteam，生成5个teammates调查不同的假设。让它们互相对话，试图推翻对方的理论，像科学辩论一样。将最终共识更新到findings文档。

##### 分层评审

适用场景:代码审查、PRReview等需要从多个维度同时评估。

核心机制:每个Teammate负责一个审查维度，同时工作，互不干扰。每个维度都能得到充分关注。不同专家可能发现关联问题。

`Prompt:`创建一个agent team来审查PR#142。生成三个reviewer:一个专注安全隐患，一个检查性能影响，一个验证测试覆盖。让它们各自审查并汇报发现。

##### 模块化开发

适用场景:新功能开发，涉及多个独立模块(前端、后端、数据库、测试)。

核心机制:每个Teammate拥有一个模块，通过共享任务列表协调工作。任务可以声明依赖，被阻塞的任务在依赖完成后自动解锁。拆分工作时必须确保每个Teammate 拥有不同的文件集。

`Prompt`:创建一个agent team来开发用户通知功能。四个teammates:一个做数据库schema和迁移，一个做后端API，一个做前端组件，一个写测试。后端API依赖数据库schema完成后才能开始。

##### 规划-审批

适用场景:复杂或高风险任务，需要在实施前确认方案。

核心机制:要求Teammate 在实施前先提交计划，Lead审批通过后才能执行。

Prompt:生成一个architect teammate来重构认证模块。要求在修改任何代码前先提交计划等待审批。只批准包含测试计划的方案。拒绝任何修改数据库schema的方案。

#### 例子

<img src="./assets/image-20260722200306401.png" alt="image-20260722200306401" style="zoom:50%;" />

#### 对比

Sub-Agents vs Agent Teams选型决策

workers需要互相通信吗? token开销值得吗？

![image-20260722200345068](./assets/image-20260722200345068.png)

#### 小结

<img src="./assets/image-20260722200646201.png" alt="image-20260722200646201" style="zoom:50%;" />

## 14.Skills

