import os
import sys
import json
import argparse
import colorama

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

def get_comment_symbols(extension, config):
    comment_info = config["comment_symbols_map"].get(extension, {})
    line_symbol_key = comment_info.get('line')
    block_symbols_key = comment_info.get('block')
    line_symbol = config["line_comment_symbols"].get(line_symbol_key) if line_symbol_key else None
    block_symbols = [config["block_comment_symbols"][block_symbols_key][0], config["block_comment_symbols"][block_symbols_key][1]] if block_symbols_key else None
    return line_symbol, block_symbols

def count_comments(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    line_symbol, block_symbols = get_comment_symbols(extension, config)

    in_block_comment = False
    comment_chars = 0
    total_chars = 0

    with open(file_path, 'r') as file:
        for line in file:
            clean_line = line.strip()
            total_chars += len(clean_line)

            if block_symbols:
                start_symbol, end_symbol = block_symbols
                if in_block_comment:
                    end_block_index = clean_line.find(end_symbol)
                    if end_block_index != -1:
                        comment_chars += end_block_index + len(end_symbol)
                        in_block_comment = False
                    else:
                        comment_chars += len(clean_line)
                    continue

                if clean_line.startswith(start_symbol):
                    in_block_comment = True
                    start_block_index = clean_line.find(start_symbol)
                    comment_chars += len(clean_line) - start_block_index
                    continue

            if line_symbol and clean_line.startswith(line_symbol):
                comment_chars += len(clean_line) - len(line_symbol)

    return comment_chars, total_chars

def calculate_comment_percentage(file_paths, min_ratio):
    max_length = max(len(path) for path in file_paths)

    total_comment_chars = 0
    total_chars = 0

    for file_path in file_paths:
        comment_chars, file_chars = count_comments(file_path)
        comment_ratio = comment_chars / file_chars * 100

        total_comment_chars += comment_chars
        total_chars += file_chars

        file_name = file_path.ljust(max_length)

        color = "\033[92m" if comment_ratio >= min_ratio else ("\033[93m" if min_ratio - 5 <= comment_ratio <= min_ratio + 5 else "\033[91m")
        print(f"File: {file_name} | Comment Percentage: {color}{comment_ratio:.2f}%\033[0m")

    if total_chars > 0:
        total_comment_ratio = total_comment_chars / total_chars * 100
        color = "\033[92m" if total_comment_ratio >= min_ratio else ("\033[93m" if min_ratio - 5 <= total_comment_ratio <= min_ratio + 5 else "\033[91m")
        print(f"Global Comment Percentage: {color}{total_comment_chars / total_chars * 100:.2f}%\033[0m")
    else:
        print("No files found or files are empty.")

def find_files(root_folder, config):
    found_files = []
    script_file = os.path.abspath(sys.argv[0])

    for root, _, file_list in os.walk(root_folder):
        for file in file_list:
            full_path = os.path.join(root, file)
            if full_path != script_file:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in config["comment_symbols_map"]:
                    found_files.append(full_path)

    return found_files

if __name__ == "__main__":
    colorama.init()
    config = load_config('config.json')

    parser = argparse.ArgumentParser(description='Calculate Comment Percentage in Code')
    parser.add_argument('--path', type=str, default=os.getcwd(), help='Path to the project folder (default: current directory)')
    parser.add_argument('--ratio', type=float, default=30, help='Minimum acceptable comment percentage (default: 30)')
    args = parser.parse_args()

    file_paths = find_files(args.path, config)

    if not file_paths:
        print("No matching file found or empty folder.")
        sys.exit(1)

    calculate_comment_percentage(file_paths, args.ratio)
