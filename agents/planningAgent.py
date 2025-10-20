from .agent import Agent

class PlanningAgent(Agent):
    def plan(self, draft):
        system_message = "你是一个专利实施许可合同撰写助手。你的任务是分析提供的专利实施许可合同描述，并将其整理成结构化的格式。"
        user_message = f"""{draft}\n根据所提供的专利实施许可合同草案，我需要您协助我编写最详细的专利实施许可合同写作指南。本指南应由多个部分组成，每个部分针对专利实施许可合同描述的特定部分提供写作指导，并涵盖该部分需要涉及的关键要点。请按照以下格式输出：\n<Section-1>\nOverview: 描述该部分的主要目的及其在专利实施许可合同中的作用。\n<Subsection-1>\n该部分的主要内容和起草要点。\n</Subsection-1>\n<Subsection-2>\n该部分的主要内容和起草要点。\n</Subsection-2>\n<Subsection-3>\n该部分的主要内容和起草要点。\n</Subsection-3>\n...\n<Subsection-m>\n该部分的主要内容和起草要点。\n</Subsection-m>\n</Section-1>\n<Section-2>\nOverview: 描述该部分的主要目的及其在专利实施许可合同中的作用。\n<Subsection-1>\n该部分的主要内容和起草要点。\n</Subsection-1>\n<Subsection-2>\n该部分的主要内容和起草要点。\n</Subsection-2>\n...\n<Subsection-m>\n该部分的主要内容和起草要点。\n</Subsection-m>\n</Section-2>\n...\n<Section-n>\nOverview: 描述该部分的主要目的及其在专利实施许可合同中的作用。\n<Subsection-1>\n该部分的主要内容和起草要点。\n</Subsection-1>\n<Subsection-2>\n该部分的主要内容和起草要点。\n</Subsection-2>\n...\n<Subsection-m>\n该部分的主要内容和起草要点。\n</Subsection-m>\n</Section-n>\n每个 Section 应描述该部分在专利实施许可合同中的主要作用和目标。每个 Subsection 应是一个完整的段落，明确概述该部分的主要内容和起草要点，同时确保技术描述的清晰性和法律可执行性之间的平衡。"""
        plan = self.chat(user_message=user_message, system_message=system_message)
        return plan