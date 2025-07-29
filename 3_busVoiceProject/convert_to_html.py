#!/usr/bin/env python3
"""
마크다운 파일을 깔끔한 HTML로 변환하는 스크립트
"""

import markdown
import os

def convert_md_to_html(md_file_path):
    """마크다운 파일을 HTML로 변환"""
    
    # 마크다운 파일 읽기
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # HTML로 변환 (확장 기능 포함)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite'
    ])
    
    html_content = md.convert(md_content)
    
    # CSS 스타일 추가 (깔끔한 PDF 출력용)
    html_template = f"""
<!DOCTYPE html>
<html lang="ko">0
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>버스 음성 안내 시스템 프로젝트 랩업 리포트</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: white;
            color: #333;
        }}
        
        h1, h2, h3 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        h1 {{
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 30px;
        }}
        
        h2 {{
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        
        h3 {{
            font-size: 1.4em;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #34495e;
        }}
        
        ul, ol {{
            padding-left: 25px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
        }}
        
        pre code {{
            background-color: transparent;
            color: #333;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            font-style: italic;
            color: #7f8c8d;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        
        .emoji {{
            font-size: 1.2em;
        }}
        
        @media print {{
            body {{
                background-color: white !important;
                color: black !important;
            }}
            
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
            
            pre, blockquote {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
    """
    
    # HTML 파일로 저장
    html_file_path = md_file_path.replace('.md', '.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ HTML 변환 완료: {html_file_path}")
    print("📋 브라우저에서 열어서 Ctrl+P로 PDF 저장하세요!")
    
    return html_file_path

if __name__ == "__main__":
    md_file = "PROJECT_WRAP_UP_REPORT.md"
    
    if os.path.exists(md_file):
        convert_md_to_html(md_file)
    else:
        print(f"❌ {md_file} 파일을 찾을 수 없습니다.")
