import os


def search_filename(file_id: str, dir_path: str):
    try:
        # 디렉토리 내의 파일들 검색
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            # 파일인지 확인
            if os.path.isfile(file_path):
                # 확장자 분리
                name, _ = os.path.splitext(filename)
                # 이름이 file_id와 일치하면 해당 파일 반환
                if name == file_id:
                    return file_path
    except Exception as e:
        return None


def get_image_path(file_id: str, search_in_dir: str):
    if file_id == None:
        return None

    # 파일이 저장된 디렉토리 경로
    file_id = file_id.split('.')[0] if '.' in file_id else file_id
    dir_path = search_in_dir

    # 디렉토리가 존재하지 않으면 기본 이미지 반환
    if not os.path.isdir(dir_path):
        return None

    return search_filename(file_id, dir_path)
