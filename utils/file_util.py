from pathlib import Path


def ensure_file_clear(file_path: str) -> None:
    """
    确保文件存在且内容为空

    若文件不存在，则创建该文件（包括必要的父目录）
    若文件已存在，则清空其内容

    参数:
        file_path: 文件路径字符串
    """
    # 转换为Path对象便于处理
    file = Path(file_path)

    # 确保父目录存在
    file.parent.mkdir(parents=True, exist_ok=True)

    # 打开文件：若不存在则创建，若存在则清空内容
    # "w"模式会自动截断文件（清空内容），如果文件不存在则创建
    with open(file, "w", encoding="utf-8"):
        pass  # 无需写入内容，打开后关闭即可实现创建/清空效果

    print(f"已确保文件状态: {file_path} (存在且内容为空)")