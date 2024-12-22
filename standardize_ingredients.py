import json

# 加載 JSON 文件
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 保存 JSON 文件
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 清理並標準化數據
def standardize_ingredients(data):
    standardized_data = []

    for item in data:
        standardized_item = {}

        # 保留 ingredient 欄位
        standardized_item["ingredient"] = item.get("ingredient", "").strip()

        # 處理 aliases 欄位：將字符串轉為陣列
        aliases = item.get("aliases", "").strip()
        if isinstance(aliases, str):
            standardized_item["aliases"] = [alias.strip() for alias in aliases.split(",") if alias.strip()]
        else:
            standardized_item["aliases"] = aliases if isinstance(aliases, list) else []

        # 將營養數據移至 nutrition_per_100g
        nutrition = {}
        for key, value in item.items():
            if "Calories" in key:
                nutrition["calories"] = value
            elif "Protein" in key:
                nutrition["protein"] = value
            elif "Fat" in key:
                nutrition["fat"] = value
            elif "Carbohydrate" in key:
                nutrition["carbohydrate"] = value

        standardized_item["nutrition_per_100g"] = nutrition

        # 添加標準化後的數據
        standardized_data.append(standardized_item)

    return standardized_data

# 主程式
def main():
    input_file = "ingredients.json"   # 原始數據文件
    output_file = "standardized_ingredients.json"  # 標準化後的文件

    # 加載數據
    raw_data = load_json(input_file)

    # 標準化數據
    standardized_data = standardize_ingredients(raw_data)

    # 保存標準化後的數據
    save_json(standardized_data, output_file)
    print(f"標準化完成，結果已保存到 {output_file}")

if __name__ == "__main__":
    main()
