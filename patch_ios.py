import os
import re

def patch_cpp_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Nếu file không dùng ImGui thì bỏ qua
    if "ImGui::Begin" not in content:
        return False

    print(f"Đã tìm thấy file giao diện cần sửa: {file_path}")
    
    # Hàm xử lý chèn code chia đôi màn hình iPad thông minh
    def replace_imgui_begin(match):
        full_line = match.group(0)
        title = match.group(1).lower()
        
        inject_code = "\n    // --- iPadOS Auto Split-Screen Layout ---\n"
        inject_code += "    if (ImGui::GetMainViewport()) {\n"
        inject_code += "        float w = ImGui::GetMainViewport()->WorkSize.x;\n"
        inject_code += "        float h = ImGui::GetMainViewport()->WorkSize.y;\n"
        
        # Nếu là cửa sổ liên quan đến Debug/Memory/Register/Hex thì đẩy sang bên phải
        if any(keyword in title for keyword in ["debug", "mem", "hex", "reg", "disasm"]):
            inject_code += "        ImGui::SetNextWindowPos(ImVec2(w * 0.5f, 0), ImGuiCond_Always);\n"
            inject_code += "        ImGui::SetNextWindowSize(ImVec2(w * 0.5f, h), ImGuiCond_Always);\n"
        else:
            # Các cửa sổ máy tính Casio chính nằm bên trái
            inject_code += "        ImGui::SetNextWindowPos(ImVec2(0, 0), ImGuiCond_Always);\n"
            inject_code += "        ImGui::SetNextWindowSize(ImVec2(w * 0.5f, h), ImGuiCond_Always);\n"
        
        inject_code += "    }\n    "
        return inject_code + full_line

    # Tìm chính xác các đoạn ImGui::Begin("Tên Cửa Sổ"...) của tác giả
    pattern = r'ImGui::Begin\s*\(\s*"([^"]+)"'
    new_content = re.sub(pattern, replace_imgui_begin, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

# Quét sạch thư mục nguồn src để tự động sửa code
patched = False
for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith((".cpp", ".h", ".hpp")):
            if patch_cpp_file(os.path.join(root, file)):
                patched = True

if patched:
    print(">>> Đã cấu hình chia đôi màn hình iPad thành công!")
else:
    print(">>> Không tìm thấy file ImGui nào cần sửa.")
