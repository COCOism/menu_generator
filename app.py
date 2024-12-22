import json
import os
import streamlit as st
from standardize_ingredients import standardize_ingredients  # 导入标准化函数

# 加载 JSON 文件
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 '{file_path}' 不存在，请检查路径！")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 保存 JSON 文件
def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 自动标准化食材数据
def auto_standardize_ingredients():
    input_file = "ingredients.json"  # 输入的原始数据文件
    output_file = "standardized_ingredients.json"  # 输出的标准化数据文件

    try:
        # 加载原始数据
        raw_data = load_data(input_file)
        # 调用标准化函数
        standardized_data = standardize_ingredients(raw_data)
        # 保存标准化后的数据
        save_data(standardized_data, output_file)
        st.success(f"标准化文件已生成：{output_file}")
    except FileNotFoundError:
        st.error(f"错误：文件 '{input_file}' 不存在，请检查路径！")
    except Exception as e:
        st.error(f"标准化过程中发生错误：{e}")

# 主程序
def main():
    st.title("午餐营养菜单生成器")
    st.write("欢迎使用午餐营养菜单生成器，根据输入的数据生成符合条件的菜单。")

    # 自动标准化食材数据
    st.header("步骤 1：标准化食材数据")
    auto_standardize_ingredients()

    # 加载标准化后的数据文件
    try:
        ingredients_data = load_data("standardized_ingredients.json")
        st.success(f"已加载标准化数据，共 {len(ingredients_data)} 条食材。")
    except FileNotFoundError:
        st.error("无法找到标准化后的食材数据文件，请检查！")
        return
    except Exception as e:
        st.error(f"加载数据过程中发生错误：{e}")
        return

    # 生成菜单的逻辑（占位，待补充）
    st.header("步骤 2：生成菜单")
    st.write("菜单生成逻辑将接入这里...")
    # 在这里添加您的菜单生成代码

# 运行主程序
if __name__ == "__main__":
    main()
