import os
import re
import json
import requests
from github import Github

# 配置下载地址
DOWNLOAD_URLS = {
    "win-x64": "https://dl.snipaste.com/win-x64",
    "win-x86": "https://dl.snipaste.com/win-x86",
    "mac": "https://dl.snipaste.com/mac",
    "linux": "https://dl.snipaste.com/linux"
}

# 版本记录文件
VERSIONS_FILE = "versions.json"

def get_actual_url(redirect_url):
    """获取重定向后的实际下载地址"""
    try:
        response = requests.head(redirect_url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"获取实际下载地址失败: {str(e)}")
        return None

def extract_version_and_filename(url):
    """从URL中提取版本号和文件名"""
    if not url:
        return None, None
    
    # 匹配文件名格式，例如 Snipaste-2.10.8-x64.zip
    pattern = r"Snipaste-(\d+\.\d+\.\d+)-([\w-]+)\.(zip|dmg|tar\.gz)"
    match = re.search(pattern, url)
    
    if match:
        version = match.group(1)
        filename = f"Snipaste-{version}-{match.group(2)}.{match.group(3)}"
        return version, filename
    return None, None

def load_existing_versions():
    """加载已备份的版本记录"""
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_version(version):
    """保存新备份的版本记录"""
    versions = load_existing_versions()
    if version not in versions:
        versions.append(version)
        with open(VERSIONS_FILE, 'w') as f:
            json.dump(versions, f, indent=2)

def download_file(url, save_path):
    """下载文件到本地"""
    try:
        print(f"开始下载: {url}")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"下载完成: {save_path}")
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        if os.path.exists(save_path):
            os.remove(save_path)
        return False

def create_release_and_upload(version, files):
    """创建    在GitHub上创建Release并上传文件
    """
    try:
        # 初始化GitHub客户端
        g = Github(os.environ['GITHUB_TOKEN'])
        repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
        
        # 检查版本是否存在该版本的release
        for release in repo.get_releases():
            if release.tag_name == f"v{version}":
                print(f"版本 v{version} 已存在，无需重复创建")
                return False
        
        # 创建新的release
        release = repo.create_git_release(
            tag_name=f"v{version}",
            name=f"Snipaste v{version}",
            message=f"自动备份的 Snipaste v{version} 版本",
            draft=False,
            prerelease=False
        )
        
        # 上传文件
        for file_path in files:
            if os.path.exists(file_path):
                release.upload_asset(file_path)
                print(f"已上传: {file_path}")
        
        return True
    except Exception as e:
        print(f"创建release或上传文件失败: {str(e)}")
        return False

def main():
    # 获取所有版本信息
    version_info = {}
    for platform, url in DOWNLOAD_URLS.items():
        actual_url = get_actual_url(url)
        if not actual_url:
            print(f"获取 {platform} 实际地址失败，跳过该平台")
            continue
            
        version, filename = extract_version_and_filename(actual_url)
        if not version or not filename:
            print(f"无法从 {actual_url} 提取版本信息，跳过该平台")
            continue
            
        version_info[platform] = {
            "url": actual_url,
            "version": version,
            "filename": filename
        }
        print(f"{platform}: 版本 {version}, 文件 {filename}")
    
    # 检查所有平台是否版本一致
    versions = list(set(info["version"] for info in version_info.values()))
    if len(versions) != 1:
        print(f"检测到不一致的版本: {versions}，取消执行备份")
        return
    
    current_version = versions[0]
    print(f"检测到统一版本: {current_version}")
    
    # 检查是否已备份该版本
    existing_versions = load_existing_versions()
    if current_version in existing_versions:
        print(f"版本 {current_version} 已备份备份，无需重复操作")
        return
    
    # 下载所有文件
    downloaded_files = []
    for platform, info in version_info.items():
        save_path = info["filename"]
        if download_file(info["url"], save_path):
            downloaded_files.append(save_path)
    
    # 确保所有文件都下载成功
    if len(downloaded_files) != len(DOWNLOAD_URLS):
        print(f"部分文件下载失败，共成功 {len(downloaded_files)} 个，需要 {len(DOWNLOAD_URLS)} 个")
        # 清理已下载的文件
        for file in downloaded_files:
            if os.path.exists(file):
                os.remove(file)
        return
    
    # 创建release并上传文件
    if create_release_and_upload(current_version, downloaded_files):
        print(f"版本 {current_version} 备份成功")
        save_version(current_version)
    else:
        print(f"版本 {current_version} 备份失败")
    
    # 清理本地文件
    for file in downloaded_files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()
