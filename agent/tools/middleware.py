from langchain.agents.middleware import AgentState, ModelRequest, before_model, dynamic_prompt, wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from utils.prompt_loader import load_system_prompt, load_report_prompt
from langgraph.runtime import Runtime
from utils.loger_handler import logger
from langchain_core.messages import ToolMessage
from langgraph.types import Command


@wrap_tool_call
def monitor_tool(
    #请求的数据封装
    request: ToolCallRequest,
    #执行的函数本身
    handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:     #工具执行的监控
    logger.info(f"[tool monitor] 执行工具: {request.tool_call['name']}")
    logger.info(f"[tool monitor] 传入参数: {request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor] 工具{request.tool_call['name']}执行成功")
        """这里这样操作是因为prompts\main_prompt.txt里面第16行的规定"""
        if request.tool_call['name'] == "fill_context_for_report":#只要调用的工具名字是fill_context_for_report
            request.runtime.context["report"] = True#fill_context_for_report工具的执行结果为True，则将报告生成场景设置为True
            return result
        return result#工具名字不是fill_context_for_report，则直接返回结果
    except Exception as e:
        logger.error(f"[tool monitor] 工具{request.tool_call['name']}执行失败: {e}")
        raise e

@before_model
def log_brfore_model(
    state: AgentState,      #整个Agent智能体的状态记录
    runtime: Runtime,      #记录整个执行过程的上下文信息
):     #在模型执行前输出日志
    logger.info(f"[log_before_model] 即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt     #每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):     #动态切换提示词
    is_report = request.runtime.context.get("report", False)#get是字典里的一个方法，用来获取字典里的值，这里默认值False
    if is_report:           #是报告生成场景，返回报告生成提示词内容，跟上面monitor_tool函数中的if语句对应
        return load_report_prompt()
                            #不是报告生成场景，返回系统提示词内容
    return load_system_prompt()


