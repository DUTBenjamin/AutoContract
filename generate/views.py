import json
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
import threading
from datetime import datetime


def generate_view(request):
    """Render the generate form page"""
    return render(request, 'generate.html')


# 用于存储生成进度的全局变量
generation_progress = 0
generation_status = ""
process_completed = False


def update_progress(process):
    """监控进程输出并更新进度"""
    global generation_progress, generation_status, process_completed
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                # 检查进程是否结束
                if process.poll() is not None:
                    break
                continue

            line = line.strip()
            print(f"Process output: {line}")  # 调试日志

            if line.startswith('[Progress]'):
                try:
                    generation_progress = int(line.split('%')[0].split()[-1])
                    print(f"Updated progress: {generation_progress}")  # 调试日志
                except Exception as e:
                    print(f"Error parsing progress: {e}")  # 调试日志

            generation_status = line

        # 进程结束后检查退出码
        return_code = process.wait()
        if return_code == 0:
            generation_progress = 100
            generation_status = "合同生成完成"
        else:
            generation_status = f"生成失败，退出码：{return_code}"

    except Exception as e:
        print(f"Error in update_progress: {e}")  # 调试日志
        generation_status = f"发生错误: {str(e)}"
    finally:
        process_completed = True


@csrf_exempt
def generate_draft(request):
    """Handle form submission and generate contract draft"""
    global generation_progress, generation_status

    print("收到生成合同请求")  # 添加日志

    if request.method == 'POST':
        try:
            # 获取请求数据
            data = json.loads(request.body)
            questions = data.get('questions', [])
            answers = data.get('answers', [])

            print(f"收到 {len(questions)} 个问题")  # 添加日志
            for q, a in zip(questions, answers):
                print(f"问题: {q}, 答案: {a}")  # 添加日志

            # 创建 draft.json
            draft_data = []
            for q, a in zip(questions, answers):
                draft_data.append({"q": q, "a": a})

            draft_path = settings.DRAFT_DIR / 'draft.json'
            print(f"保存 draft.json 到 {draft_path}")  # 添加日志

            with open(draft_path, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False, indent=2)

            # 确保输出目录存在
            settings.OUTPUT_DIR.mkdir(exist_ok=True)
            settings.DRAFT_DIR.mkdir(exist_ok=True)

            # 生成合同 JSON 文件的脚本
            generate_script = settings.BASE_DIR / 'generate_contract.py'
            print(f"执行生成脚本: {generate_script}")  # 添加日志

            generate_process = subprocess.Popen(
                ['python', str(generate_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore',
                close_fds = True
            )

            # 捕获并打印输出
            stdout, stderr = generate_process.communicate()
            print("生成脚本标准输出:", stdout)
            print("生成脚本错误输出:", stderr)

            # 检查生成是否成功
            if generate_process.returncode != 0:
                raise Exception(f"生成合同失败，返回码：{generate_process.returncode}")

            # 找到最新生成的 JSON 文件
            json_files = list(settings.OUTPUT_DIR.glob('contract_*.json'))
            if not json_files:
                raise FileNotFoundError("未找到生成的合同 JSON 文件")

            latest_json = max(json_files, key=os.path.getctime)
            print(f"找到最新 JSON 文件: {latest_json}")  # 添加日志

            # 生成 Word 文档
            transfer_script = settings.BASE_DIR / 'transfer.py'
            output_docx = settings.OUTPUT_DIR / f'contract_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx'

            print(f"开始转换 Word 文档: {output_docx}")  # 添加日志

            transfer_process = subprocess.Popen(
                ['python', str(transfer_script), str(latest_json), str(output_docx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore'
            )

            # 捕获并打印输出
            stdout, stderr = transfer_process.communicate()
            print("转换脚本标准输出:", stdout)
            print("转换脚本错误输出:", stderr)

            # 检查转换是否成功
            if transfer_process.returncode != 0:
                raise Exception(f"转换合同失败，返回码：{transfer_process.returncode}")

            return JsonResponse({
                'success': True,
                'message': '合同生成已开始'
            })

        except Exception as e:
            print(f"Error in generate_draft: {e}")
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
def get_progress(request):
    """获取当前生成进度"""
    global generation_progress, generation_status, process_completed

    # 检查是否有最新生成的文件
    latest_file = None
    if process_completed and generation_progress == 100:
        try:
            files = list(settings.OUTPUT_DIR.glob('*.docx'))
            if files:
                latest_file = max(files, key=os.path.getctime).name
        except Exception as e:
            print(f"Error checking output files: {e}")

    return JsonResponse({
        'progress': generation_progress,
        'status': generation_status,
        'completed': process_completed,
        'filename': latest_file
    })


def download_contract(request, filename):
    try:
        file_path = settings.OUTPUT_DIR / filename
        if not os.path.exists(file_path):
            return HttpResponse('File not found', status=404)

        # 准备文件下载
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        return HttpResponse(str(e), status=500)
