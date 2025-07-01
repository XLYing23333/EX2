## **1.  LangChain框架核心模块**

### 1.1 相关概念

###    **（1）LangChain框架简介**  

LangChain是一个AI应用程序开发框架，旨在帮助开发人员使用大语言模型构建端到端的应用程序。它提供了一套工具、组件和接口，可简化创建由大语言模型（LLM）和聊天模型提供支持的应用程序的过程。LangChain可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如API和数据库。

**LangChain的主要价值在于以下几个方面：**

- 组件化：LangChain 框架提供了用于处理大语言模型的抽象组件，以及每个抽象组件的一系列实现。这些组件具有模块化设计，易于使用，无论是否使用 LangChain 框架的其他部分，都可以方便地使用这些组件。
- 简化开发难度：通过提供组件化和现成的链式组装，LangChain 框架可以大大简化大语言模型应用的开发难度。开发人员可以更专注于业务逻辑，而无需花费大量时间和精力处理底层技术细节。

#### **（2）LangChain框架的组成部分**

LangChain框架由以下几部分组成，如下图所示：

- **LangChain 库**：Python 和 JavaScript 库。包含大量组件的接口和集成，将这些组件组合成链和代理的基本运行时，以及链和代理的现成实现。
- **LangChain Template**：一系列易于部署的参考架构，用于各种任务。
- **LangServe**：一个用于将 LangChain 链部署为 REST API 的库。
- **LangSmith**：一个开发者平台，让你可以调试、测试、评估和监控基于任何 LLM 框架构建的链，并且与 LangChain 无缝集成。

   


LangChain 库由以下几个包组成：

- **langchain-core：**基础抽象和 LangChain表达式语言。
- **langchain-community：**第三方集成。
- **langchain**：构成应用程序认知架构的Chain、Agent和RAG检索策略。

![596267428b6d6ef3057389e489953d0d](img/实验手册/596267428b6d6ef3057389e489953d0d.svg)

####    **（3）LangChain的核心模块**

**LangChain提供以下六种标准的、可扩展的接口和外部集成的核心模块：**

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240506%2Fac1d8d7497f44729965a4b88e6aa8be0.jpg)

- **模型I/O（Model I/O）：**负责与语言模型进行交互，处理输入和输出数据。
- **检索（Retrieval）：**从特定数据源检索信息，如数据库或API，为应用提供所需内容。
- **代理（Agents）：**根据高级指令决定使用哪些工具或组件，协调应用内的操作和信息流。
- **链（Chains）**：定义一系列有序步骤以完成特定任务。
- **内存（Memory）**：在LangChain运行间保持应用状态。
- **回调（Callbacks）**：在LangChain的特定步骤触发额外动作，如日志记录或中间步骤的流式传输。



### 1.2 实践3. **LangChain的核心模块详细介绍**

#### **3.1** Model I/O

#####    **（1）基本概念**

   在LangChain中，模型输入/输出（Model I/O）是指与LLM进行交互的组件，它是大语言模型应用的核心元素。该模块的基本流程图如下图所示，主要包含以下3个核心步骤：

- **格式化（Format）**：原始数据被清洗、标记化、编码，并根据特定任务需求构建提示模板，以转换成适合语言模型处理的格式。
- **预测（Predict）**：格式化后的数据被直接送入语言模型，模型基于其内部知识和训练数据生成文本输出。
- **解析（Parse）**：语言模型的文本输出被提取特定信息、转换成不同数据类型，并经过必要的后处理，以满足下游组件或应用程序的结构化需求。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240506%2Fddd0a491d0ff4f79911eb4819c755d21.png)

   Model I/O的核心组件如下图所示，主要包含用于接收和生成文本的语言模型、指导输入格式的提示模板、筛选训练数据的示例选择器、解析模型输出的输出解析器。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240506%2Fd34c2e23b9564c40b6487f19fbb66f2f.png)

① **语言模型 (Language Models)**：提供了与大语言模型的接口，主要有两种类型模型的接口：

- **LLMs：**大型语言模型，接收文本字符串作为输入，并返回文本字符串。OpenAI的GPT-3是LLM实现的一个实例。
- **Chat Model：**聊天模型，是语言模型的一种变体。接受Chat Messages列表作为输入并返回Chat Message。Chat Model专为会话交互设计。与传统的纯文本补全模型相比，这一模型的API采用了不同的接口方式：它需要一个标有说话者身份的聊天消息列表作为输入，如“系统”、“AI”或“人类”。作为响应，Chat Model会返回一个标为“AI”的聊天消息输出。GPT-4和Anthropic 的 Claude都可以通过 Chat Model 调用。



② **消息(Message)**


| 标识符    | 对应类        | 实际含义           | 使用场景               | 示例内容                             |
| --------- | ------------- | ------------------ | ---------------------- | ------------------------------------ |
| human     | HumanMessage  | 来自人类用户的消息 | LangChain 原生消息系统 | "hi"                                 |
| user      | HumanMessage  | 来自人类用户的消息 | 兼容 OpenAI API 的格式 |                                      |
| ai        | AIMessage     | AI 生成的回复      | LangChain 原生消息系统 | "Hello! 😊 How can I help you today?" |
| assistant | AIMessage     | AI 生成的回复      | 兼容 OpenAI API 的格式 |                                      |
| system    | SystemMessage | 系统级指令         | 两种系统通用           | "你是一个专业的翻译助手"             |



③  **提示模板(Prompt Templates)：**

- **PromptTemplate：**用于生成字符串提示。
- **ChatPromptTemplate：**用于生成聊天消息列表的提示。

**④ 示例选择器（Example Selectors）：**

- **训练新模型：**Example Selectors从数据集中筛选代表性的示例来训练新模型，确保其学习高质量、多样化的数据，提升学习效果和泛化能力。
- **调优现有模型：**利用Example Selectors提供的新示例，对现有模型进行持续训练和调优，逐步改进其在特定任务上的表现，提高准确性和效率。

**⑤ 输出解析器（Output Parsers）：**

- **Get format instructions：**返回一个字符串，其中包含要求语言模型应该返回什么格式内容的提示词。
- **Parse：**将模型返回的内容，解析为目标格式。

##### **（2）Model I/O实践**

在model_io_demo.py文件中编写本模块的代码，首先使用BaseChatOpenAI创建一个聊天模型，指定模型名称为“deepseek-chat”；然后创建提示词模板，给定AI一个身份，即设置System提示词为”您是一名精通古代典籍的专家。。用户提示词设置为”请为我推荐诸子百家中必读的经典书籍“。Langchain会调用ChatPromptTemplate.from_messages()生成聊天消息列表的提示。最后，返回LLM回答的结果， 使用model.invoke(chat_test).content获取LLM回答的文本，其中，chat_test表示用户的提示词。

#### 3.2 **Chains**

**（1） Chains介绍**

​	 **① Chains的基本概念及优势**

   虽然独立使用大语言模型能够应对一些简单任务，但对于更加复杂的需求，可能需要将多个大语言模型进行链式组合，或与其他组件进行链式调用。LangChain为这种“链式”应用提供了Chain接口，并将该接口定义得非常通用。作为一个调用组件得序列，还可以包含其他链。Chains具有以下优势：

- **模块化：**提高代码复用性，降低开发复杂性。
- **可维护性：**易于理解和维护，方便修改和扩展。
- **灵活性：**支持不同组合方式，适应多变需求。


​	② **Chains的类型**

​		Chains包含通用链和实用链两种类型：

- **通用链：**这些链使用一个大语言模型（LLM）根据给定的提示生成文本。比如LLM链和简单顺序链。它们主要依赖于单一的语言模型来完成文本生成的任务。
- **实用链：**这些链将多个大语言模型（LLM）一起用于特定任务。例如，检索QA链可能用于问答系统，LLM数学链用于处理数学相关的工作，加载摘要链用于生成文本的摘要，而PAL链则可能用于特定的自然语言处理任务。


​	③ **Chains的工作流程**

Chains的工作流程为：通过定义链构造函数来初始化链，配置所需的组件和可能的其他链，以形成具有特定功能的执行流程。Chains流程包含以下四个核心步骤：

- **Chain Constructor（链构造函数）：**在LangChain中，链构造函数用于初始化链，设定其组件、配置及嵌套的其他链。
- **Function Calling（函数调用）**：这指链是否需要调用外部函数，如OpenAI服务，以执行其任务。
- **Other Tools（其他工具）**：除LangChain核心组件外，链可能还使用其他工具如数据库、API等以增强其功能。
- **When to Use（何时使用）**：这部分提供指导，帮助开发者确定在何种场景或需求下使用特定的LangChain链最为合适。


​	**④ Chains的架构**

Chains作为LangChain的核心组件，通过串联各个逻辑单元，实现了流程控制、数据传递和状态管理，使得复杂的业务逻辑能够高效、有序地执行。

- **流程控制**：Chains通过特定的顺序将逻辑单元串联起来，确保业务流程按照预定的顺序执行。每个逻辑单元在Chains中都被视为一个节点，节点之间的连接形成了完整的业务流程。
- **数据传递**：在Chains中，数据在各个节点之间流动。每个节点接收前一个节点的输出作为输入，并根据业务需求进行处理，然后将结果传递给下一个节点。这种数据传递方式实现了各个逻辑单元之间的无缝衔接。
- **状态管理**：Chains还具备状态管理能力，允许节点在执行过程中修改自身的状态，并根据上一次的状态进行相应的操作。这有助于处理复杂的业务逻辑，提高代码的复用性和可维护性。


**（2） Chains实践**

在langchain_demo/chains_demo.py文件中编写本模块的代码。

如果想对LLM进行复杂的应用，而不是仅进行一次对话，那么就需要将LLM串联起来，要么相互串联，要么与其他组件串联起来。本模块使用LLMChain来完成与LLM的多轮对话交互，而多轮对话便是一个链式调用的过程，以以下场景为例：

- 向鲁菜厨师（System）咨询位于青岛的鲁菜菜馆推荐
- 继续向它咨询午饭的菜品推荐
- 对于它推荐的菜品，向它提问具体做法

   首先沿用之前实验的聊天模型提示词，并构建第一个LLMChain，“向鲁菜厨师（System）咨询位于青岛的鲁菜菜馆推荐”。

   LangChain的构造函数接收一个LLM和一个PromptTemplate作为参数。构造完成之后可以直接调用里面的run方法，将PromptTemplate所需要的变量，通过K=>V对的形式传入进去，返回的结果就是LLM回答的答案。

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import SimpleSequentialChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
openai_api_base = "http://localhost:8000/v1"
openai_api_key = "EMPTY"
model = ChatOpenAI(model_name="Qwen",
                  temperature=0.5,
                   openai_api_base=openai_api_base,
                   openai_api_key=openai_api_key)
system_template = '''你是一名出色的鲁菜厨师。'''
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{test}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

restaurant_chain = LLMChain(llm = model, prompt = chat_prompt)
```

   默认情况下，__call__同时返回输入和输出的键值。你可以通过设置return_only_outputs为True，将其配置为只返回输出键值。

```
print(restaurant_chain('请为我推荐一家位于青岛的著名鲁菜菜馆', return_only_outputs=True))
```

   如果希望Chain只输出一个输出键（即它的output_keys中只有一个元素），你可以使用run方法。注意，run会输出一个字符串而不是一个字典。

```
print(restaurant_chain.run('请为我推荐一家位于青岛的著名鲁菜菜馆'))
```

   构建第二个LLMChain，“继续向它咨询午饭的菜品推荐”

```
system_template = '''请在菜馆中为我的午饭推荐三道饭菜'''
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{test}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
meal_chain = LLMChain(llm = model, prompt = chat_prompt)
```

   构建第三个LLMChain，“对于它推荐的菜品，向它提问具体做法”

```
system_template = '''请讲解这些饭菜的具体做法'''
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{test}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
recipe_chain = LLMChain(llm = model, prompt = chat_prompt)
```

   使用SimpleSequentialChain(chains中的LLMChain类，将我们需要按顺序依次调用的三个LLMChain放在一个数组里，传给这个类的构造函数。对于这个对象，我们调用run方法，把我们的中文问题交给它。这个时候，这个SimpleSequentialChain就会按照顺序依次调用chains这个数组中参数里包含的LLMChain。并且，每一次调用的结果都会存储在这个Chain构造时定义的output_key参数里。而下一次调用的LLMChain的模板内的变量如果有和之前的output_key名字相同的，就会用output_key里存入的内容替换掉模板内变量所在的占位符。

```
overall_chain = SimpleSequentialChain(chains=[restaurant_chain, meal_chain, recipe_chain], verbose = True)  #verbose开启提示符

review = overall_chain.run("请为我推荐一家位于青岛的著名鲁菜菜馆")
```

   代码编写完毕后，运行chains_demo.py文件，输出结果如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240611%2Fcad704bc3e294587b0346c5bf19cbd6a.png)

#### 3.3 **Callbacks**

   **（1）Callbacks基本概念**

   LangChain提供了回调系统，允许连接到大语言模型应用程序的各个阶段。这对于日志记录、监控、流式处理和其他任务非常有用。可以通过使用API中提供的callbacks参数订阅这些事件。CallbackHandlers 是实现 CallbackHandler 接口的对象，每个事件都可以通过一个方法订阅。当事件触发时，CallbackManager 会调用相应事件所对应的处理程序。

```
class BaseCallbackHandler:
    """Base callback handler that can be used to handle callbacks from langchain."""

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""

    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors."""

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        """Run when tool ends running."""

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
```

   **（2）常用的Callbacks类型**

- **StdOutCallbackHandler：**将所有事件的日志作为标准输出，打印到终端中。注意，当verbose参数设置为True时，StdOutCallbackHandler是默认被启用的，即运行过程中的日志会被全部打印到终端中。
- **AsyncCallbackHandler：**异步回调函数，如果我们计划使用异步API，建议使用AsyncCallbackHandler以避免阻塞运行循环。如果在使用异步方法运行LLM、Chain、Tool、Agent时使用同步的CallbackHandler，它仍然可以工作。但在内部，它将使用run_in_executor调用，如果您的CallbackHandler不是线程安全的，可能会导致问题。
- **FileCallbackHandler：**开发项目过程中，写日志是重要的调试手段之一。正式的项目中，我们不能总是将日志输出到终端中，这样无法传递和保存。
- **get_openai_callback:** 使用该回调函数来获取token消耗。

   **（3）Callbacks实践**

   在callback_demo.py文件中编写本模块的代码。

   回调函数可在构造函数中回调，也可以在请求函数中回调：

- 构造函数回调：在构造函数中定义，例如LLMChain(callbacks=[handler], tags=['a-tag'])，它将被用于对该对象的所有调用，并且将只针对该对象。例如，如果你向LLMChain构造函数传递一个handler，它将不会被附属于该链的Model使用。构造函数回调对诸如日志、监控等用例最有用，这些用例不是针对单个请求，而是针对整个链。例如，如果你想记录所有向LLMChain发出的请求，你可以向构造函数传递一个处理程序。
- 请求函数回调：定义在用于发出请求的call()/run()/apply()方法中，例如chain.run(inputs, callbacks=[handler])，它将仅用于该特定请求，以及它包含的所有子请求。例如，对LLMChain的调用会触发对Model的调用，该Model使用run()方法中传递的相同handler。

   方法一，构造函数回调，在初始化链时显式设置StdOutCallbackHandler。

```
print('*****构造函数回调，在初始化链时显式设置StdOutCallbackHandler*****')
from langchain.callbacks import StdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)



openai_api_base = "http://localhost:8000/v1"
openai_api_key = "EMPTY"
model = ChatOpenAI(model_name="Qwen",
                  temperature=0,
                   openai_api_base=openai_api_base,
                   openai_api_key=openai_api_key)

system_template = '''你需要根据用户的饮食需求推荐位于青岛的合适的餐厅。'''
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{input}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
handler = StdOutCallbackHandler()
restaurant_chain = LLMChain(llm=model, prompt=chat_prompt, callbacks=[handler])
print(restaurant_chain.run(input='鲁菜'))
```

   方法二，将verbose参数设置为True，默认启用StdOutCallbackHandler回调：

```
print('****************************使用verbose属性***************************')
restaurant_chain = LLMChain(llm=model, prompt=chat_prompt, verbose=True)
print(restaurant_chain.run(input='鲁菜'))
```

   方法三，使用请求回调，也可以达到相同的效果。

```
print('******************************使用请求回调*****************************')
restaurant_chain = LLMChain(llm=model, prompt=chat_prompt)
print(restaurant_chain.run(input='鲁菜', callbacks=[handler]))
```

   也可以自定义回调处理器：

```
print('*****************************使用自定义回调处理器************************')
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# 自定义回调函数
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(f"My custom handler, token: {token}")

print('--with callback--')
chat = ChatOpenAI(model_name="Qwen",
                    temperature=0,
                    openai_api_base=openai_api_base,
                    openai_api_key=openai_api_key,
                    streaming=True,
                    max_tokens=200,
                    callbacks=[MyCustomHandler()])
chat([HumanMessage(content="给我讲个笑话")])


print('--without callback--')
model = ChatOpenAI(model_name="Qwen",
                    temperature=0,
                    openai_api_base=openai_api_base,
                    openai_api_key=openai_api_key,
                    streaming=True,
                    max_tokens=200)
print(model([HumanMessage(content="给我讲个笑话")]))
```

   代码编写完毕后，运行callback_demo.py文件。

   构造函数回调，在初始化链时显式设置StdOutCallbackHandler，输出结果如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2Ff0f3382717124744af34ac712c54e12d.png)

   使用verbose属性，输出结果如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F7a5aa10f9d0549d480b39af99c605852.png)

   使用请求回调，输出结果如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F579cab4541dc4b0d9db705a9a0b3d3f4.png)

   可以看到，使用上述3种不同的回调函数设置方式，可以达到相同的效果。

   自定义回调处理器，使用回调函数和不使用回调函数效果对比如下：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F3a1a55b5702e4ee8afea8c7c65094d2f.png)

#### 3.4 **Memory**

   **（1）Memory的概念**

   大多数大语言模型应用都使用对话方式与用户交互。对话中的一个关键环节是能够引用和参考之前对话中的信息。对于对话系统来说，最基础的要求是能够直接访问一些过去的消息。在更复杂的系统中还需要一个能够不断更新的世界模型，使其能够维护有关实体及其关系的信息。在Langchain中，这种存储关于过去交互信息的能力被称为“记忆”。Langchain中提供了许多用于向系统中添加记忆的方法，可以单独使用，也可以无缝地整合到链中。

   **（2）Memory模块的基本框架**

   Memory模块的基本框架如下图所示，记忆系统需要支持两个基本操作：读取和写入。每个链都根据输入定义了核心执行逻辑。其中一些输入直接来自用户，但有些输入可以来源于记忆。在接收到初始用户输入，但在执行核心逻辑之前，链将从记忆系统中读取内容并增强用户输入。在核心逻辑执行完毕并在返回答复之前，链会将这一轮的输入和输出都保存到记忆系统中，以便在将来使用他们。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240507%2Faecca826dccb406ba9181dd259e7055e.png)

   **（3）****Memory的类型**

   在LangChain中提供了多种记忆方式的支持，列举以下几个：

- ConversationBufferMemory：只是将聊天消息列表保存到缓冲区中，并将其传递到提示模板中。
- ConversationBufferWindowMemory：允许用户设置一个超参数K，来限定每次从记忆中读取最近的K条记忆。
- ConversationEntityMemory：保存一些实体信息，如从输入中找出一个人名，保存这个人的信息。
- ConversationSummaryMemory：对上下文做摘要。
- ConversationSummaryBufferMemory：保存Token限制内的上下文，对更早的做摘要。
- ConversationTokenBufferMemory：允许用户执行最大的token长度，使得从记忆中取上下文时不会超过token限制。
- VectorStoreRetrieverMemory：将 Memory 存储在向量数据库中，根据用户输入检索回最相关的部分

   **（4）****Memory实践**

   **在**memory_demo.py文件中编写本模块的代码。

   首先使用ConversationBufferWindowMemory类型，在构造LLMChain时为它指定一个ConversationBufferWindowMemory的memory对象，并且将这个对象的chat_history设置为k=3，即只保留最近三轮的对话内容。

```
print('************使用ConversationBufferWindowMemory×××××××××××××××××')
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

openai_api_base = "http://localhost:8000/v1"
openai_api_key = "EMPTY"
model = ChatOpenAI(model_name="Qwen",
                  temperature=0,
                   openai_api_base=openai_api_base,
                   openai_api_key=openai_api_key)

system_template = '''你是青岛的一名出色的鲁菜厨师，现在正在网上回答来青岛旅游的游客的问题，你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在200个字以内
{chat_history}
'''
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{input}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3)
llm_chain = LLMChain(
    llm=model,
    prompt=chat_prompt,
    memory=memory,
    verbose=True
)

print(llm_chain.predict(input="请为我推荐一家合适的鲁菜菜馆"))

print(llm_chain.predict(input="请为我推荐这家餐厅中的菜品"))

print(llm_chain.predict(input="请告诉我青岛啤酒烤虾的具体做法"))

print(llm_chain.predict(input="我向你提问的第一个问题是什么？"))
```

   BufferWindow这样的滑动窗口有几个坏处，就是在几轮对话之后会把之前的对话记录忘记，并且每次保存完整的对话列表会导致占用过大的token。LangChain中提供了一个ConversationSummaryBufferMemory，它可以让AI去总结前几轮的对话内容，这样就不担心对话轮数太多或者过长了。

   ConversationSummaryMemory的构造函数也接收一个LLM对象，这个对象专门用于对历史对话生成小结，它与对话本身使用的LLM可以不一致。

```
print('×××××××××××××××××使用ConversationSummaryMemory×××××××××××××××××××')
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template = '''你是青岛的一名出色的鲁菜厨师，现在正在网上回答来青岛旅游的游客的问题，你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在200个字以内
{chat_history}
'''

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = '''{input}'''
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

memory = ConversationSummaryMemory(memory_key="chat_history", llm=model)
conversation_with_summary = ConversationChain(
    llm=model,
    prompt=chat_prompt,
    memory=memory,
    verbose=True
)

print(conversation_with_summary.predict(input="请为我推荐一家合适的鲁菜菜馆"))

print(conversation_with_summary.predict(input="请为我推荐这家餐厅中的菜品"))

print(conversation_with_summary.predict(input="请告诉我葱烧海参的具体做法"))

print(conversation_with_summary.predict(input="我向你提问的第一个问题是什么？"))
```

   代码编写完毕后，运行memory_demo.py文件，实验结果如下：

   使用ConversationBufferWindowMemory记忆类型，实验结果如下图所示，蓝框中的内容为保存的”记忆“，红框中的内容为LLM根据上下文生成的回答。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F4eb56a611cb24df0909543f643719f88.png)

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2Fb102c17270f149c89b86a8230bc8ee0d.png)

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F7bc76612200c4d39a39b254d640ed424.png)

   使用ConversationSummaryMemory记忆类型，实验结果如下图所示，实验结果如下图所示，蓝框中的内容为保存的”记忆“，是LLMAI总结的前几轮的对话内容（摘要）；红框中的内容为LLM根据上下文生成的回答。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F4c6d26c2e7174cc1ad4d67294422e161.png)

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2Fd442d97aa1ce413dad25def5af4a87a2.png)

#### 3.5 **检索（Retrieval）**

   **（1）** **检索（Retrieval）简介**

   LangChain通过其Retrieval组件简化了检索增强生成(RAG)过程中外部数据的检索与管理，为LLM应用高效地提供了用户特定的数据。主要工作流程为：从指定来源获取并读取文档，经过预处理和向量化后，将文档存储并索引化，最终根据用户查询进行高效搜索并返回相关结果。Retrieval模块的工作流程如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240507%2F067f4a3215ef40339d17d75265d34715.png)

   Retrieval流程包含以下六个核心步骤：

- **Source（来源）：**关键词：**获取**，表示从各种来源获取文档或数据。
- **Load（加载）：**关键词：**读取**，代表从来源中加载并读取文档或数据的过程。
- **Transform（转换）：**关键词：**预处理**，表示对加载的文档或数据进行清洗、格式化和转换，以适应后续步骤。
- **Embed（嵌入）：**关键词：**向量化**，代表将文档或数据转换为向量表示，以捕捉其语义信息。
- **Store（存储）：**关键词：**索引化**，表示将嵌入后的向量存储在数据库中，并建立索引以优化检索性能。
- **Retrieve（检索）：**关键词：**搜索**，代表根据用户查询从存储的向量数据库中检索相关文档或数据的过程。

   **Retrieval的核心组件：****Retrieval的六个核心组件共同协作，实现文档的高效加载、精确拆分、语义嵌入、向量存储、智能检索及优化索引，为各类应用场景提供强大且灵活的文档处理与检索能力。**

   **① 文档加载 (Document Loaders)**

- 功能：从多种来源加载文档。
- 特性：支持100+加载器，与AirByte、Unstructured等集成。
- 应用：加载HTML、PDF、代码等，来源包括私有S3桶、公共网站等。

   **② 文本拆分 (Text Splitting)**

- 功能：将大文档拆分为小片段，以便更精确地检索相关内容。
- 特性：提供多种拆分算法，优化特定文档类型（如代码、Markdown）。

   **③ 文本嵌入模型 (Text Embedding Models)**

- 功能：为文档创建语义嵌入，以快速找到相似文本。
- 特性：支持25+嵌入提供商和方法，包括开源和专有API。
- 优点：标准接口，方便模型切换。

   **④ 向量存储 (Vector Stores)**

- 功能：高效存储和搜索文档嵌入。
- 特性：支持50+向量存储解决方案，包括开源和云托管选项。
- 优点：标准接口，轻松切换存储方案。

   **⑤ 检索器 (Retrievers)**

- 功能：从数据库中检索文档。
- 特性：支持多种检索算法，包括语义搜索和高级算法（如父文档检索器、自查询检索器、集成检索器）。
- 应用：提高检索性能和准确性。

   **⑥ 索引 (Indexing)**

- 功能：将数据源同步到向量存储，避免重复和冗余。
- 特性：LangChain索引API，优化存储和检索过程。
- 优点：节省时间和成本，改善搜索结果质量。

    **（2）检索（****Retrieval****）实践**

   在本部分，基于LangChain的Retrieval模块实现一个简单的”本地知识库问答机器人“。

   首先从【资料】中的"LangChain入门"目录下下载note.txt文件和all-MiniLM-L6-v2.zip压缩包，通过文件管理将这两个文件上传到/root/Desktop/CM_Chat/langchain_demo/目录下。打开一个新的终端，执行以下命令解压all-MiniLM-L6-v2.zip压缩包，该压缩包中存储的是embeddings模型。

```
cd langchain_demo/
unzip all-MiniLM-L6-v2.zip
```

    在retrieval_demo.py文件中编写本模块的代码。
    
    在本模块中，主要实现了一个”基于本地知识库的小说情节问答机器人“，主要实现流程如下：

- 使用TextLoader()加载"note.txt"文件，并转换为document 对象，文件内容来自于《斗破苍穹》小说；
- 使用CharacterTextSplitter()将文本拆分成文本块，设置以下三个参数：separator（用于指定分隔符）；chunk_size（每个文本块/文档的字符数量限制）；chunk_overlap（相邻两个文档重叠区域的长度）；
- 使用SentenceTransformerEmbeddings()加载embeddings模型，采用的embeddings模型all-MiniLM-L6-v2，它可以将句子或者段落映射到384维的向量空间中；
- 文档存储将 document使用embeddings模型进行向量化处理，并临时存入 Chroma 向量数据库，用于后续匹配查询
- 使用RetrievalQA()根据问题从Chroma 向量数据库中检索相似度较高的内容，并将检索到的内容组合成上下文，与原始的输入一起喂给大模型。

```
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import SentenceTransformerEmbeddings

openai_api_base = "http://localhost:8000/v1"
openai_api_key = "EMPTY"
model = ChatOpenAI(model_name="Qwen",
                  temperature=0,
                   openai_api_base=openai_api_base,
                   openai_api_key=openai_api_key)


# 文档加载
loader = TextLoader("note.txt")
# 将数据转成 document 对象
documents = loader.load()

# 文本拆分
text_splitter = CharacterTextSplitter(separator = "\n",chunk_size=300, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 初始化本地部署的 embeddings 模型
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 文档存储：将 document使用embeddings模型进行向量化处理，并临时存入 Chroma 向量数据库，用于后续匹配查询
docsearch = Chroma.from_documents(texts, embeddings)
index_count = docsearch._collection.count()
print('文档数量：',index_count)
# 先检索，后生成
qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": index_count}))

query = "萧炎在拍卖场争夺的斗技叫什么"
print(qa.run(query))
```

   代码编写完毕后，运行retrieval_demo.py文件，结果如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F5d7086954b0f48458b6e6fc11fc41f04.png)

#### 3.6 **Agents**

   **（1）Agents的本质及优势**

   Agents的核心概念是利用语言模型来选择一系列要执行的动作。与传统的硬编码动作链不同，Agents使用语言模型作为推理引擎来确定要执行哪些动作以及它们的执行顺序。主要有以下优势：

- **基于语言模型的决策**：LangChain Agents以语言模型为核心，使其能够理解和执行自然语言或类似自然语言的指令。这种能力让Agents可以灵活地适应不同的任务和环境，无需硬编码特定的逻辑。
- **可组合性与扩展性**：LangChain框架注重Agents的可组合性和系统的扩展性。Agents可以通过组合各种工具和模块（如数据检索、信息提取、API调用等）来扩展其功能。这种设计方式不仅简化了维护和更新过程，还促进了代码和知识的重用。
- **学习与适应性**：结合机器学习技术（如强化学习），Agents可以从经验中学习并优化其行为策略，以应对复杂和动态变化的环境，从而提高性能和效率。

   **（2）****Agents的组成部分**

   Agents的组成部分如下图所示：

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240507%2F9d2fc502ee3b41ef8577f88149e5bd0b.png)

- **模式（Schema）：**是一组规则和结构，定义了代理如何与外部工具进行交互、执行动作以及管理任务状态，从而实现智能的多步骤推理和决策。**主要包括AgentAction、****Intermediate Steps、****AgentFinish。**
- **代理（Agent）**: 负责决策下一个动作的实体。代理使用语言模型、提示和输出解析器来支持其决策过程。**主要包括Agent Inputs、Agent Outputs。**
- **代理执行器（AgentExecutor）**: 负责运行代理并管理其与外部工具的交互。执行器处理复杂性，如工具错误处理、日志记录等。
- **工具（Tools）**: 代理可以调用的函数或服务。每个工具都有一个输入模式和一个关联的函数，用于描述如何调用该工具以及实际执行的操作。
- **工具包（Toolkits）**: 相关工具的集合，用于完成特定任务。例如，GitHub 工具包可能包含用于搜索问题、读取文件、发表评论等的工具。

   **（3）****Agents流程**

   **Agents流程主要包含以下四个核心步骤：**

- **接收任务**：LLM Agent首先接收一个任务描述或问题。
- **思考**：然后，它利用LLM进行推理和决策。例如，它可能会生成一个潜在的解决方案或行动计划。
- **行动**：接下来，LLM Agent会执行一些操作以完成任务。这些操作可能包括调用API获取数据、查询数据库、执行计算等。
- **接收反馈**：在执行操作后，LLM Agent会接收来自环境的反馈。这些反馈可能包括API的响应、数据库查询的结果等。

   如果任务还没有完成，LLM Agent会重复上述步骤，直到任务完成或达到某个终止条件。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240507%2Fe84f0da54fb242ec9113cb10aa3c869d.png)

   **（4）Agent Types**

   在LangChain中，Agent Types定义了不同类型的代理（Agents），这些代理使用不同的策略和方法来与用户和工具进行交互，以完成各种任务。

- **Zero-shot ReAct**：
  这种Agent使用ReAct（Retrieve-and-Act）框架，该框架通过理解工具的描述来选择最合适的工具执行任务。Zero-shot意味着Agent不需要针对特定任务进行训练，而是可以基于工具的描述直接进行推断。
- **Structured tool chat**：
  这种Agent支持使用具有复杂输入参数的工具。通过定义args_schema，Agent可以理解每个工具所需输入参数的结构和类型，从而与用户进行更结构化的对话以收集必要的信息。这有助于确保与工具的交互是准确和一致的。
- **Conversational**：
  与标准ReAct Agent相比，Conversational Agent更注重与用户进行自然对话。它的提示和响应设计得更加对话性，适合在聊天场景中使用。
- **Self-ask with search**：
  这种Agent类型集成了搜索功能，允许它自主地在搜索引擎中查找信息以回答问题。这增加了Agent的知识来源和回答问题的能力。
- **ReAct document store**：
  使用这种Agent，用户可以与一个文档存储进行交互。该Agent包含两个关键工具：“Search”用于在文档存储中搜索相关文档，“Lookup”用于在最近找到的文档中查找特定术语或信息。
- **XML Agent**：
  XML Agent专门用于处理XML格式的数据。它使用XML格式来解析工具调用和最终答案，这使得它特别适合与返回XML响应的工具或服务进行交互。

   **（5）Agent实践**

   在agent_demo.py文件中编写本模块的代码。

   在本模块中，实现一个Zero-shot ReAct类型的Agent，主要定义以下两个工具：

- calculate()：使用LLMMathChain链计算数学公式；
- recommend_meal()：调用该工具时直接返回”葱烧海参“字符串。

   接着创建一个工具列表，并指明每个工具的名称，并添加相应的描述，LLM模型通过理解每个工具的描述来选择合适的工具；最后使用 initialize_agent()初始化Agent。

```
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool

openai_api_base = "http://localhost:8000/v1"
openai_api_key = "EMPTY"
model = ChatOpenAI(model_name="Qwen",
                  temperature=0,
                   openai_api_base=openai_api_base,
                   openai_api_key=openai_api_key)


# 定义计算器过程
def calculate(query: str)->str:
    llm_math = LLMMathChain.from_llm(model, verbose=True)
    ans = llm_math.run(query)
    return ans


# 定义饭菜推荐过程
def recommend_meal(query:str)->str:
    return "葱烧海参"


# 初始化tools
math_tool = Tool(
    name='calculator',
    func=calculate,
    description='计算数学问题时请使用calculator工具'
)
meal_tool = Tool(
    name="recommend_meal",
    func=recommend_meal,
    description="当你被要求为顾客推荐饭菜时请用这个工具"
)

tools = [math_tool, meal_tool]

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=model,
    verbose=True,
    max_iterations=3
)

zero_shot_agent("请使用calculator工具，计算(4.5*2.1)**2.1?")
zero_shot_agent('中午不知道吃什么，请为我推荐')
```

   代码编写完毕后，运行agent_demo.py文件，运行结果如下图所示，对于输入”请使用calculator工具，计算(4.5*2.1)**2.1?“，调用calculate工具进行计算得到结果”111.79098888525806“；对于输入”中午不知道吃什么，请为我推荐“，调用recommend_meal工具返回菜名”葱烧海参“。

![img](https://tecs-prod-static.obs.cn-north-1.myhuaweicloud.com:443/23a1bd42cdb54703b802532f7a361767%2Frichtext%2Fimage%2F20240612%2F2db825adea824d8db22de847c6dd1192.png)

#####  
