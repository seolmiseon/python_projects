# Streamlit 배포용 엔트리 포인트 파일
import sys
import os

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 3_busVoiceProject/src 디렉토리를 Python path에 추가
bus_project_src = os.path.join(project_root, '3_busVoiceProject', 'src')
sys.path.append(bus_project_src)

# 메인 앱 실행
import importlib.util
spec = importlib.util.spec_from_file_location("app", os.path.join(bus_project_src, "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

if __name__ == "__main__":
    app_module.main()
