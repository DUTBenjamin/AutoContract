from .agent import Agent
import re

class ExaminerAgent(Agent):
    def reviewDraft(self, answer, i):
        system_message = "你是一名专利实施许可合同代理人，负责审查专利实施许可合同草案，擅长依据相关要求评估这些草案是否符合质量标准。"
        requirements = {
            1: "名词和术语定义部分必须包含所有关键术语的定义。",
            2: "许可授予部分必须包含许可专利、许可方式、许可范围、分许可等内容。",
            3: "许可费及支付方式部分必须包含许可费的计算方式、支付方式、支付时间等内容。",
            4: "技术资料交付与验收部分必须包含技术资料的交付方式、验收标准等内容。",
            5: "技术服务与培训部分必须包含技术服务的内容、培训的安排等内容。",
            6: "保密条款部分必须包含保密信息的定义、保密义务、保密期限等内容。",
            7: "后续改进成果部分必须包含改进成果的定义、分享方式等内容。",
            8: "陈述与保证部分必须包含许可方和被许可方的陈述与保证内容。",
            9: "技术进出口部分必须包含技术进出口的合规性声明。",
            10: "侵权应对及共同维权部分必须包含侵权应对的程序、费用分担等内容。",
            11: "专利权被宣告无效的处理部分必须包含专利权无效的处理方式、费用分担等内容。",
            12: "不可抗力部分必须包含不可抗力的定义、处理方式等内容。",
            13: "送达部分必须包含送达方式、送达地址等内容。",
            14: "违约与损害赔偿部分必须包含违约责任的划分、损害赔偿的计算等内容。",
            15: "税费部分必须包含税费的承担方式等内容。",
            16: "争议解决部分必须包含争议解决的方式、管辖法院等内容。",
            17: "合同的生效、变更与终止部分必须包含合同的生效条件、变更程序、终止条件等内容。",
        }
        requirement = requirements.get(i, "该部分草案必须符合专利实施许可合同的基本要求。")
        prompt = f"""# Draft: {answer}\n# Requirements: {requirement}\n如果包含，请直接返回 <Result> Pass </Result>; 如果不包含，请返回 <Result> Fail </Result>, 并在 <Reason> waiting for filling </Reason>中给出详细解释。\n请告诉我这部分草案是否符合质量标准。不要重复输出"""
        response = self.chat(user_message=prompt, system_message=system_message)
        result_pattern = rf"(?<=<Result>).*?(?=</Result>)"
        result = re.findall(result_pattern, response, re.DOTALL)[0].strip()
        reason_pattern = rf"(?<=<Reason>).*?(?=</Reason>)"
        reason = re.findall(reason_pattern, response, re.DOTALL)
        if len(reason) == 0:
            reason = ""
        else:
            reason = reason[0]
        return result, reason

    def reviewSubsection(self, sub_plan, subsection, book):
        draft = book["draft"]
        result_pattern = r"<Result>(.*?)</Result>"
        reason_pattern = r"<Advice>(.*?)</Advice>"
        prompt = f"""{draft}
        <WritingGuideline>{sub_plan}</WritingGuideline>
        <Content>{subsection}</Content>
        <Requirement> </Requirement>
        参考草案内容，并依据给定的写作指南，评估该内容是否符合所提供的要求。 
        如果内容符合要求和写作指南，则返回  <Result>Pass</Result>; 如果不符合，则返回 <Result>Fail</Result>. 并且，无论结果是通过还是不通过，你都必须在 <Advice> waiting for filling </Advice> 中提供有用且详细的建议。
        """
        try_times = 0
        while True:
            try_times += 1
            ref = self.chat(user_message=prompt, system_message="你是一位经验丰富的专利实施许可合同审查员")
            match = re.search(result_pattern, ref, re.DOTALL)
            match1 = re.search(reason_pattern, ref, re.DOTALL)
            if try_times > 1:
                return "Fail", None
            if match is not None and match1 is not None:
                result = match.group(1).strip()
                advice = match1.group(1)
                if result == "Pass":
                    return "Pass", advice
                else:
                    return "Fail", advice