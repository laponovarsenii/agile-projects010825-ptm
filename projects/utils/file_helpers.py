import os

ALLOWED_EXTENSIONS = ['csv', 'doc', 'pdf', 'xlsx']

def check_extension(file, allowed_extensions) -> bool:
    file_name = file.name
    file_extension = file_name.split('.')[-1]
    return file_extension in allowed_extensions


def check_file_size(file, max_mb=4) -> bool:
    file_size = file.size
    file_size_mb = file_size / (1024 * 1024)
    return file_size_mb < max_mb


def create_file_path(project_name, file_name) -> str:
    pref = "documents"
    new_project_name = project_name.replace(" ", '_')
    file_path = os.path.join(pref, new_project_name, file_name)
    return file_path


def save_file(file_path, file_content) -> str:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, 'wb') as f:
        for chunk in file_content.chunks(chunk_size=1024):
            f.write(chunk)

    return file_path
