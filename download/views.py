# download/views.py
import os
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.conf import settings


def download_view(request):
    """渲染下载页面"""
    return render(request, 'download.html')


def get_contracts(request):
    """获取可下载的合同文件列表"""
    try:
        print(f"Scanning directory: {settings.OUTPUT_DIR}")  # 添加日志
        contracts = []

        # 确保目录存在
        if not os.path.exists(settings.OUTPUT_DIR):
            print(f"Output directory doesn't exist: {settings.OUTPUT_DIR}")
            return JsonResponse({
                'success': True,
                'contracts': []
            })

        for filename in os.listdir(settings.OUTPUT_DIR):
            if filename.endswith('.docx'):
                print(f"Found file: {filename}")  # 添加日志
                file_path = os.path.join(settings.OUTPUT_DIR, filename)
                file_info = {
                    'filename': filename,
                    'created_time': os.path.getctime(file_path),
                    'size': os.path.getsize(file_path)
                }
                contracts.append(file_info)
                print(f"Added contract: {file_info}")  # 添加日志

        # 按创建时间排序，最新的在前
        contracts.sort(key=lambda x: x['created_time'], reverse=True)

        # 格式化时间和文件大小
        for contract in contracts:
            contract['created_time'] = datetime.fromtimestamp(
                contract['created_time']
            ).strftime('%Y-%m-%d %H:%M:%S')
            contract['size'] = f"{contract['size'] / 1024 / 1024:.2f} MB"

        return JsonResponse({
            'success': True,
            'contracts': contracts
        })
    except Exception as e:
        print(f"Error in get_contracts: {e}")  # 添加错误日志
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def download_contract(request, filename):
    """处理合同文件下载，下载后不删除文件"""
    try:
        file_path = os.path.join(settings.OUTPUT_DIR, filename)

        if not os.path.exists(file_path):
            return JsonResponse({
                'success': False,
                'message': '文件不存在'
            }, status=404)

        # 确保只能下载.docx文件
        if not filename.endswith('.docx'):
            return JsonResponse({
                'success': False,
                'message': '无效的文件类型'
            }, status=400)

        # 准备文件下载
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
    except Exception as e:
        print(f"Error in download_contract: {e}")  # 添加错误日志
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)