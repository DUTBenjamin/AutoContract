import io
import json
import logging
import tqdm
import yaml
import pandas as pd
from openai import OpenAI
import httpx
from agents.writerAgent import (
    DefinitionsWriter, LicenseGrantWriter, PaymentTermsWriter,
    TechnicalDeliveryWriter, TechnicalServiceWriter, ConfidentialityWriter, ImprovementWriter,
    RepresentationsWriter, TechnologyExportWriter, InfringementResponseWriter, PatentInvalidityWriter,
    ForceMajeureWriter, DeliveryWriter, BreachWriter, TaxWriter, DisputeResolutionWriter,
    ContractEffectivenessWriter, DescriptionWriter
)
from agents.planningAgent import PlanningAgent
from agents.examinerAgent import ExaminerAgent
import re
import os
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

def step1(row_data):
    draft = row_data['draft']
    writers = [
        DefinitionsWriter, LicenseGrantWriter, PaymentTermsWriter,
        TechnicalDeliveryWriter, TechnicalServiceWriter, ConfidentialityWriter,
        ImprovementWriter, RepresentationsWriter, TechnologyExportWriter,
        InfringementResponseWriter, PatentInvalidityWriter, ForceMajeureWriter,
        DeliveryWriter, BreachWriter, TaxWriter, DisputeResolutionWriter,
        ContractEffectivenessWriter
    ]
    names = [
        "definitions", "license_grant", "payment_terms",
        "technical_delivery", "technical_service", "confidentiality",
        "improvement", "representations", "technology_export",
        "infringement_response", "patent_invalidity", "force_majeure",
        "delivery", "breach", "tax", "dispute_resolution",
        "contract_effectiveness"
    ]
    book = {"draft": draft}
    total_writers = len(writers)
    for i, (writer, name) in enumerate(zip(writers, names)):
        # 假设 step1 占总进度的 30%
        progress = int((i + 1) / total_writers * 30)
        print(f"Generating {name}...")
        writer_instance = writer(client=client, model_name=model_name)
        book[name] = writer_instance.write(draft)
        print(f"{name} generated successfully.")
    return book


def step2(book):
    plan = planningAgent.plan(book["draft"])

    section_pattern = re.compile(r'<Section-(\d+)>(.*?)</Section-\1>', re.DOTALL)
    section_plans = section_pattern.findall(plan)
    sections = []
    total_sections = len(section_plans)
    for i, section_plan in enumerate(section_plans):
        # 假设 step2 占总进度的 70%
        progress = int(30 + (i + 1) / total_sections * 70)
        print(f"[Progress] {progress}%")
        print(f"Processing section {i + 1}...")
        sub_pattern = re.compile(r'<Subsection-(\d+)>(.*?)</Subsection-\1>', re.DOTALL)
        subsection_plans = sub_pattern.findall(section_plan[1])
        subsections = []
        for subsection_plan in subsection_plans:
            # For Retrieval
            referenceContent = descriptionWriter.retrieve(subsection_plan, book)
            subsection = descriptionWriter.writeSubsection(section_plan, subsection_plan, referenceContent)

            # For Examiner
            result, advice = examinerAgent.reviewSubsection(subsection_plan, subsection, book)
            subsection = descriptionWriter.writeSubsection(section_plan, subsection_plan, advice=advice,
                                                           subsection=subsection)
            result, advice = examinerAgent.reviewSubsection(subsection_plan, subsection, book)
            try_time = 0
            while result != "Pass":
                try_time += 1
                if try_time > 1:
                    break
                subsection = descriptionWriter.writeSubsection(section_plan, subsection_plan, advice=advice,
                                                               subsection=subsection)
                result, advice = examinerAgent.reviewSubsection(subsection_plan, subsection, book)

            subsections.append(subsection)
        section = "\n".join(subsections)
        sections.append(section)
        print(f"Section {i + 1} processed successfully.")
    return sections


if __name__ == '__main__':
    try:
        # 添加详细的日志记录
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='contract_generation.log',
                            filemode='w')

        print("开始生成合同...")
        logging.info("开始生成合同")

        # 构建 draft.json 文件路径
        draft_path = os.path.join(os.getcwd(), 'draft', 'draft.json')
        logging.info(f"尝试读取 draft.json: {draft_path}")

        # 检查 draft.json 文件是否存在
        if not os.path.exists(draft_path):
            logging.error(f"未找到 draft.json 文件: {draft_path}")
            raise FileNotFoundError(f"未找到 draft.json 文件: {draft_path}")

        # 日志输出文件内容
        with open(draft_path, 'r', encoding='utf-8') as f:
            draft_content = f.read()
            logging.info(f"draft.json 内容: {draft_content}")

        # 读取配置文件
        config_path = os.path.join(os.getcwd(), 'config.yml')
        logging.info(f"尝试读取配置文件: {config_path}")

        with open(config_path, 'r') as f:
            configs = yaml.safe_load(f)
            logging.info(f"配置文件内容: {configs}")

        if configs["Pattern"] == "own":
            print("======Use User Pattern======")

            # 使用 json 模块读取文件
            with open(draft_path, 'r', encoding='utf-8') as f:
                draft_json = json.load(f)

            # 转换为 DataFrame
            df = pd.DataFrame(draft_json)

            # 打印调试信息
            print("Draft JSON 内容:")
            print(json.dumps(draft_json, ensure_ascii=False, indent=2))
            print("DataFrame 预览:")
            print(df)

            # 生成 draft 字符串
            draft = "<Draft>"
            for index, row in df.iterrows():
                draft += f"<Question{index + 1}>"
                draft += str(row["q"])  # 确保转换为字符串
                draft += f"</Question{index + 1}>\n"
                draft += f"<Answer{index + 1}>"
                draft += str(row["a"])  # 确保转换为字符串
                draft += f"</Answer{index + 1}>\n"
            draft += "</Draft>"

            # 创建包含 draft 的 DataFrame
            draft_list = [draft]
            df = pd.DataFrame({
                "draft": draft_list
            })

        elif configs["Pattern"] == "test":
            df = pd.read_json("data/test.json")
        else:
            raise FileExistsError("模式必须为 'own' 或 'test'")

        # 初始化 OpenAI 客户端
        client = None
        model_name = None
        if "gpt" in configs["Model-series"]:
            client = OpenAI(
                base_url="https://api.lqqq.ltd/v1",
                api_key=configs["OpenAI-api-key"],
                http_client=httpx.Client(
                    base_url="",
                    follow_redirects=True,
                ),
            )
            model_name = configs["GPT-model"]
        else:
            definitions_client = OpenAI(base_url=f"http://localhost:{configs['Definitions-port']}/v1",
                                        api_key=f"{configs['Definitions-api']}")
            license_grant_client = OpenAI(base_url=f"http://localhost:{configs['LicenseGrant-port']}/v1",
                                          api_key=f"{configs['LicenseGrant-api']}")
            payment_terms_client = OpenAI(base_url=f"http://localhost:{configs['PaymentTerms-port']}/v1",
                                          api_key=f"{configs['PaymentTerms-api']}")
            technical_delivery_client = OpenAI(base_url=f"http://localhost:{configs['TechnicalDelivery-port']}/v1",
                                               api_key=f"{configs['TechnicalDelivery-api']}")
            technical_service_client = OpenAI(base_url=f"http://localhost:{configs['TechnicalService-port']}/v1",
                                              api_key=f"{configs['TechnicalService-api']}")
            confidentiality_client = OpenAI(base_url=f"http://localhost:{configs['Confidentiality-port']}/v1",
                                            api_key=f"{configs['Confidentiality-api']}")
            improvement_client = OpenAI(base_url=f"http://localhost:{configs['Improvement-port']}/v1",
                                        api_key=f"{configs['Improvement-api']}")
            representations_client = OpenAI(base_url=f"http://localhost:{configs['Representations-port']}/v1",
                                            api_key=f"{configs['Representations-api']}")
            technology_export_client = OpenAI(base_url=f"http://localhost:{configs['TechnologyExport-port']}/v1",
                                              api_key=f"{configs['TechnologyExport-api']}")
            infringement_response_client = OpenAI(base_url=f"http://localhost:{configs['InfringementResponse-port']}/v1",
                                                  api_key=f"{configs['InfringementResponse-api']}")
            patent_invalidity_client = OpenAI(base_url=f"http://localhost:{configs['PatentInvalidity-port']}/v1",
                                              api_key=f"{configs['PatentInvalidity-api']}")
            force_majeure_client = OpenAI(base_url=f"http://localhost:{configs['ForceMajeure-port']}/v1",
                                          api_key=f"{configs['ForceMajeure-api']}")
            delivery_client = OpenAI(base_url=f"http://localhost:{configs['Delivery-port']}/v1",
                                     api_key=f"{configs['Delivery-api']}")
            breach_client = OpenAI(base_url=f"http://localhost:{configs['Breach-port']}/v1",
                                   api_key=f"{configs['Breach-api']}")
            tax_client = OpenAI(base_url=f"http://localhost:{configs['Tax-port']}/v1", api_key=f"{configs['Tax-api']}")
            dispute_resolution_client = OpenAI(base_url=f"http://localhost:{configs['DisputeResolution-port']}/v1",
                                               api_key=f"{configs['DisputeResolution-api']}")
            contract_effectiveness_client = OpenAI(base_url=f"http://localhost:{configs['ContractEffectiveness-port']}/v1",
                                                   api_key=f"{configs['ContractEffectiveness-api']}")

            plan_client = OpenAI(base_url=f"http://localhost:{configs['Plan-port']}/v1", api_key=f"{configs['Plan-api']}")
            description_client = OpenAI(base_url=f"http://localhost:{configs['Description-port']}/v1",
                                        api_key=f"{configs['Description-api']}")
            examiner_client = OpenAI(base_url=f"http://localhost:{configs['Examiner-port']}/v1",
                                     api_key=f"{configs['Examiner-api']}")
            client = definitions_client
            model_name = configs["Definitions-model"]

        print("=====Initial Agents=====")
        definitionsWriter = DefinitionsWriter(client=client, model_name=model_name)
        licenseGrantWriter = LicenseGrantWriter(client=client, model_name=model_name)
        paymentTermsWriter = PaymentTermsWriter(client=client, model_name=model_name)
        technicalDeliveryWriter = TechnicalDeliveryWriter(client=client, model_name=model_name)
        technicalServiceWriter = TechnicalServiceWriter(client=client, model_name=model_name)
        confidentialityWriter = ConfidentialityWriter(client=client, model_name=model_name)
        improvementWriter = ImprovementWriter(client=client, model_name=model_name)
        representationsWriter = RepresentationsWriter(client=client, model_name=model_name)
        technologyExportWriter = TechnologyExportWriter(client=client, model_name=model_name)
        infringementResponseWriter = InfringementResponseWriter(client=client, model_name=model_name)
        patentInvalidityWriter = PatentInvalidityWriter(client=client, model_name=model_name)
        forceMajeureWriter = ForceMajeureWriter(client=client, model_name=model_name)
        deliveryWriter = DeliveryWriter(client=client, model_name=model_name)
        breachWriter = BreachWriter(client=client, model_name=model_name)
        taxWriter = TaxWriter(client=client, model_name=model_name)
        disputeResolutionWriter = DisputeResolutionWriter(client=client, model_name=model_name)
        contractEffectivenessWriter = ContractEffectivenessWriter(client=client, model_name=model_name)
        descriptionWriter = DescriptionWriter(client=client, model_name=model_name)
        planningAgent = PlanningAgent(client=client, model_name=model_name)
        examinerAgent = ExaminerAgent(client=client, model_name=model_name)
        print("=====Successfully=====")

        df_iter = tqdm.tqdm(df.iterrows(), total=len(df))

        application_numbers = []
        model_outputs = []
        outputs = []

        for index, row in df_iter:
            # STEP1
            shortComponentBook = step1(row)
            # STEP2
            full_descriptions = step2(shortComponentBook)
            full_description = "<Description>"
            for description in full_descriptions:
                full_description += description
            full_description += "</Description>"
            if "gpt" in configs["Model-series"]:
                output = f"""<Patent Implementation License Agreement>\n<Definitions>\n{shortComponentBook["definitions"]}\n</Definitions>\n<LicenseGrant>\n{shortComponentBook["license_grant"]}\n</LicenseGrant>\n<PaymentTerms>\n{shortComponentBook["payment_terms"]}\n</PaymentTerms>\n<TechnicalDelivery>\n{shortComponentBook["technical_delivery"]}\n</TechnicalDelivery>\n<TechnicalService>\n{shortComponentBook["technical_service"]}\n</TechnicalService>\n<Confidentiality>\n{shortComponentBook["confidentiality"]}\n</Confidentiality>\n<Improvement>\n{shortComponentBook["improvement"]}\n</Improvement>\n<Representations>\n{shortComponentBook["representations"]}\n</Representations>\n<TechnologyExport>\n{shortComponentBook["technology_export"]}\n</TechnologyExport>\n<InfringementResponse>\n{shortComponentBook["infringement_response"]}\n</InfringementResponse>\n<PatentInvalidity>\n{shortComponentBook["patent_invalidity"]}\n</PatentInvalidity>\n<ForceMajeure>\n{shortComponentBook["force_majeure"]}\n</ForceMajeure>\n<Delivery>\n{shortComponentBook["delivery"]}\n</Delivery>\n<Breach>\n{shortComponentBook["breach"]}\n</Breach>\n<Tax>\n{shortComponentBook["tax"]}\n</Tax>\n<DisputeResolution>\n{shortComponentBook["dispute_resolution"]}\n</DisputeResolution>\n<ContractEffectiveness>\n{shortComponentBook["contract_effectiveness"]}\n</ContractEffectiveness>\n</Contract>\n<Full Description>\n{full_description}\n</Full Description>\n</Patent Implementation License Agreement>"""
                outputs.append(output)
                if "application_number" in row:
                    application_numbers.append(row["application_number"])
                else:
                    application_numbers.append(index)

            model_output = f"""<Patent Implementation License Agreement>\n{shortComponentBook["definitions"]}\n{shortComponentBook["license_grant"]}\n{shortComponentBook["payment_terms"]}\n{shortComponentBook["technical_delivery"]}\n{shortComponentBook["technical_service"]}\n{shortComponentBook["confidentiality"]}\n{shortComponentBook["improvement"]}\n{shortComponentBook["representations"]}\n{shortComponentBook["technology_export"]}\n{shortComponentBook["infringement_response"]}\n{shortComponentBook["patent_invalidity"]}\n{shortComponentBook["force_majeure"]}\n{shortComponentBook["delivery"]}\n{shortComponentBook["breach"]}\n{shortComponentBook["tax"]}\n{shortComponentBook["dispute_resolution"]}\n{shortComponentBook["contract_effectiveness"]}\n{full_description}\n</Patent Implementation License Agreement>"""
            model_outputs.append(model_output)

        final_df = [
            {
                "application_number": application_numbers,
                "ground_truth": output,
                "model_output": model_output
            }
            for output, model_output in zip(outputs, model_outputs)
        ]

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H_%M_%S")

        print("====Save the file====")

        try:
            # 构建 output 文件夹路径
            output_folder = os.path.join(os.getcwd(), 'outputs')
            if not os.path.exists(output_folder):
                os.makedirs(output_folder, exist_ok=True)

            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d_%H_%M_%S")

            save_path = os.path.join(output_folder, f"contract_{len(final_df)}_{formatted_time}.json")

            # 使用 json 模块保存，确保正确处理中文
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(final_df, f, ensure_ascii=False, indent=2)

            print(f"文件已保存: {save_path}")
            print(f"文件大小: {os.path.getsize(save_path)} 字节")
            print("文件内容预览:")
            with open(save_path, 'r', encoding='utf-8') as f:
                print(f.read()[:500] + "...")  # 打印前500个字符

            print("Contract generated successfully.")

        except Exception as e:
            # 详细记录错误
            logging.error(f"保存文件时发生错误: {e}", exc_info=True)
            print(f"保存文件时发生错误: {e}")
            sys.exit(1)
    except Exception as e:
        # 详细记录错误
        logging.error(f"生成合同时发生错误: {e}", exc_info=True)
        print(f"生成合同时发生错误: {e}")
        sys.exit(1)
