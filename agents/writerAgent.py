from .agent import Agent
import re

class Writer(Agent):
    def write(self, draft):
        pass

class DefinitionsWriter(Writer):
    def write(self,draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的名词和术语定义部分，确保定义清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的名词和术语定义部分，确保包含所有关键术语的定义。格式如下：\n<Definitions> 定义内容 </Definitions>"""
        definitions = self.chat(user_message=user_message, system_message=system_message)
        definitions_pattern = rf"(?<=<Definitions>).*?(?=</Definitions>)"
        definitions = re.findall(definitions_pattern, definitions, re.DOTALL)[0]
        return definitions

class LicenseGrantWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的许可授予部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的许可授予部分，确保包含许可专利、许可方式、许可范围、分许可等内容。格式如下：\n<LicenseGrant> 许可授予内容 </LicenseGrant>"""
        license_grant = self.chat(user_message=user_message, system_message=system_message)
        license_grant_pattern = rf"(?<=<LicenseGrant>).*?(?=</LicenseGrant>)"
        license_grant = re.findall(license_grant_pattern, license_grant, re.DOTALL)[0]
        return license_grant

class PaymentTermsWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的许可费及支付方式部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的许可费及支付方式部分，确保包含许可费的计算方式、支付方式、支付时间等内容。格式如下：\n<PaymentTerms> 许可费及支付方式内容 </PaymentTerms>"""
        payment_terms = self.chat(user_message=user_message, system_message=system_message)
        payment_terms_pattern = rf"(?<=<PaymentTerms>).*?(?=</PaymentTerms>)"
        payment_terms = re.findall(payment_terms_pattern, payment_terms, re.DOTALL)[0]
        return payment_terms

class TechnicalDeliveryWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的技术资料交付与验收部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的技术资料交付与验收部分，确保包含技术资料的交付方式、验收标准等内容。格式如下：\n<TechnicalDelivery> 技术资料交付与验收内容 </TechnicalDelivery>"""
        technical_delivery = self.chat(user_message=user_message, system_message=system_message)
        technical_delivery_pattern = rf"(?<=<TechnicalDelivery>).*?(?=</TechnicalDelivery>)"
        technical_delivery = re.findall(technical_delivery_pattern, technical_delivery, re.DOTALL)[0]
        return technical_delivery

class TechnicalServiceWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的技术服务与培训部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的技术服务与培训部分，确保包含技术服务的内容、培训的安排等内容。格式如下：\n<TechnicalService> 技术服务与培训内容 </TechnicalService>"""
        technical_service = self.chat(user_message=user_message, system_message=system_message)
        technical_service_pattern = rf"(?<=<TechnicalService>).*?(?=</TechnicalService>)"
        technical_service = re.findall(technical_service_pattern, technical_service, re.DOTALL)[0]
        return technical_service

class ConfidentialityWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的保密条款部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的保密条款部分，确保包含保密信息的定义、保密义务、保密期限等内容。格式如下：\n<Confidentiality> 保密条款内容 </Confidentiality>"""
        confidentiality = self.chat(user_message=user_message, system_message=system_message)
        confidentiality_pattern = rf"(?<=<Confidentiality>).*?(?=</Confidentiality>)"
        confidentiality = re.findall(confidentiality_pattern, confidentiality, re.DOTALL)[0]
        return confidentiality

class ImprovementWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的后续改进成果的提供与分享部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的后续改进成果的提供与分享部分，确保包含改进成果的定义、分享方式等内容。格式如下：\n<Improvement> 后续改进成果内容 </Improvement>"""
        improvement = self.chat(user_message=user_message, system_message=system_message)
        improvement_pattern = rf"(?<=<Improvement>).*?(?=</Improvement>)"
        improvement = re.findall(improvement_pattern, improvement, re.DOTALL)[0]
        return improvement

class RepresentationsWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的陈述与保证部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的陈述与保证部分，确保包含许可方和被许可方的陈述与保证内容。格式如下：\n<Representations> 陈述与保证内容 </Representations>"""
        representations = self.chat(user_message=user_message, system_message=system_message)
        representations_pattern = rf"(?<=<Representations>).*?(?=</Representations>)"
        representations = re.findall(representations_pattern, representations, re.DOTALL)[0]
        return representations

class TechnologyExportWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的技术进出口部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的技术进出口部分，确保包含技术进出口的合规性声明。格式如下：\n<TechnologyExport> 技术进出口内容 </TechnologyExport>"""
        technology_export = self.chat(user_message=user_message, system_message=system_message)
        technology_export_pattern = rf"(?<=<TechnologyExport>).*?(?=</TechnologyExport>)"
        technology_export = re.findall(technology_export_pattern, technology_export, re.DOTALL)[0]
        return technology_export

class InfringementResponseWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的侵权应对及共同维权部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的侵权应对及共同维权部分，确保包含侵权应对的程序、费用分担等内容。格式如下：\n<InfringementResponse> 侵权应对及共同维权内容 </InfringementResponse>"""
        infringement_response = self.chat(user_message=user_message, system_message=system_message)
        infringement_response_pattern = rf"(?<=<InfringementResponse>).*?(?=</InfringementResponse>)"
        infringement_response = re.findall(infringement_response_pattern, infringement_response, re.DOTALL)[0]
        return infringement_response

class PatentInvalidityWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的专利权被宣告无效的处理部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的专利权被宣告无效的处理部分，确保包含专利权无效的处理方式、费用分担等内容。格式如下：\n<PatentInvalidity> 专利权被宣告无效的处理内容 </PatentInvalidity>"""
        patent_invalidity = self.chat(user_message=user_message, system_message=system_message)
        patent_invalidity_pattern = rf"(?<=<PatentInvalidity>).*?(?=</PatentInvalidity>)"
        patent_invalidity = re.findall(patent_invalidity_pattern, patent_invalidity, re.DOTALL)[0]
        return patent_invalidity

class ForceMajeureWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的不可抗力部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的不可抗力部分，确保包含不可抗力的定义、处理方式等内容。格式如下：\n<ForceMajeure> 不可抗力内容 </ForceMajeure>"""
        force_majeure = self.chat(user_message=user_message, system_message=system_message)
        force_majeure_pattern = rf"(?<=<ForceMajeure>).*?(?=</ForceMajeure>)"
        force_majeure = re.findall(force_majeure_pattern, force_majeure, re.DOTALL)[0]
        return force_majeure

class DeliveryWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的送达部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的送达部分，确保包含送达方式、送达地址等内容。格式如下：\n<Delivery> 送达内容 </Delivery>"""
        delivery = self.chat(user_message=user_message, system_message=system_message)
        delivery_pattern = rf"(?<=<Delivery>).*?(?=</Delivery>)"
        delivery = re.findall(delivery_pattern, delivery, re.DOTALL)[0]
        return delivery

class BreachWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的违约与损害赔偿部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的违约与损害赔偿部分，确保包含违约责任的划分、损害赔偿的计算等内容。格式如下：\n<Breach> 违约与损害赔偿内容 </Breach>"""
        breach = self.chat(user_message=user_message, system_message=system_message)
        breach_pattern = rf"(?<=<Breach>).*?(?=</Breach>)"
        breach = re.findall(breach_pattern, breach, re.DOTALL)[0]
        return breach

class TaxWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的税费部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的税费部分，确保包含税费的承担方式等内容。格式如下：\n<Tax> 税费内容 </Tax>"""
        tax = self.chat(user_message=user_message, system_message=system_message)
        tax_pattern = rf"(?<=<Tax>).*?(?=</Tax>)"
        tax = re.findall(tax_pattern, tax, re.DOTALL)[0]
        return tax

class DisputeResolutionWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的争议解决部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的争议解决部分，确保包含争议解决的方式、管辖法院等内容。格式如下：\n<DisputeResolution> 争议解决内容 </DisputeResolution>"""
        dispute_resolution = self.chat(user_message=user_message, system_message=system_message)
        dispute_resolution_pattern = rf"(?<=<DisputeResolution>).*?(?=</DisputeResolution>)"
        dispute_resolution = re.findall(dispute_resolution_pattern, dispute_resolution, re.DOTALL)[0]
        return dispute_resolution

class ContractEffectivenessWriter(Writer):
    def write(self, draft):
        system_message = "你是一位经验丰富的专利律师，擅长起草专利实施许可合同。你可以根据提供的上下文高效生成合同的生效、变更与终止部分，确保内容清晰、准确且符合法律要求。"
        user_message = f"""{draft}\n根据以上内容，请生成专利实施许可合同的生效、变更与终止部分，确保包含合同的生效条件、变更程序、终止条件等内容。格式如下：\n<ContractEffectiveness> 合同的生效、变更与终止内容 </ContractEffectiveness>"""
        contract_effectiveness = self.chat(user_message=user_message, system_message=system_message)
        contract_effectiveness_pattern = rf"(?<=<ContractEffectiveness>).*?(?=</ContractEffectiveness>)"
        contract_effectiveness = re.findall(contract_effectiveness_pattern, contract_effectiveness, re.DOTALL)[0]
        return contract_effectiveness

class DescriptionWriter(Writer):
    def retrieve(self, sub_plan, book):
        pattern = r"(<Reference>.*?</Reference>)"
        prompt = f"""{book["draft"]}\n{book["definitions"]}\n{book["license_grant"]}\n{book["payment_terms"]}\n{book["technical_delivery"]}\n{book["technical_service"]}\n{book["confidentiality"]}\n{book["improvement"]}\n{book["representations"]}\n{book["technology_export"]}\n{book["infringement_response"]}\n{book["patent_invalidity"]}\n{book["force_majeure"]}\n{book["delivery"]}\n{book["breach"]}\n{book["tax"]}\n{book["dispute_resolution"]}\n{book["contract_effectiveness"]}\nWriting Plan: {sub_plan}\n根据专利文本写作计划，确定以下哪些内容是撰写本节所必需的，并原样复制所有相关内容，不得修改或添加任何内容。所有复制的文本必须放在 <Reference></Reference> 标签内，严格遵守格式要求，例如：\n<Reference>\n撰写本节所需的信息\n</Reference>."""
        match = None
        try_times = 0
        while match is None and try_times < 5:
            try_times += 1
            ref = self.chat(user_message=prompt, system_message="您是一位经验丰富的专利实施许可合同律师.")
            match = re.search(pattern, ref, re.DOTALL)
        if match is None:
            return None
        else:
            ref = match.group(0)
            return ref

    def writeSubsection(self, section_plan, sub_plan, ref=None, subsection=None, advice=None):
        system = "您是一位经验丰富的专利实施许可合同律师，擅长起草清晰、精确且符合法律规定的专利实施许可合同描述。您可以将提供的描述和写作指南转化为详细且逻辑结构化的专利实施许可合同描述，彻底解释发明的技术原理和实施方式，确保遵守专利局的规定。您的专业知识确保每一份描述都组织良好、条理清晰，准确反映了发明的核心技术内容，同时展现了对技术和法律要求深刻理解的能力。"

        if ref is None:
            if advice is None:
                prompt = f"""Writing Guideline Overview:{section_plan}\nSubsection Writing Guideline: {sub_plan}\n根据子章节写作指南，请起草这一子章节，确保描述符合法律和专利规定。"""
            else:
                prompt = f"""Writing Guideline Overview: {section_plan}\nSubsection Writing Guideline: {sub_plan}\nThe subsection already written: {subsection}\nFeedback from Patent Examiner: {advice}\n根据子章节写作指南和反馈意见，修订该子章节，确保其符合法律和专利规定的同时，解决了审查员的关注点。不要添加其他任何内容，仅输出修订后的子章节。"""
        else:
            prompt = f"""{ref}\nWriting Guideline Overview:{section_plan}\nSubsection Writing Guideline: {sub_plan}\n根据<Reference></Reference>中的内容和子章节写作指南，请起草这一子章节，确保描述符合法律和专利规定。"""

        content = self.chat(user_message=prompt, system_message=system)
        return content



