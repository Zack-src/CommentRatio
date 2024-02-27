import os
import re
import sys
import csv
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

def is_inside_string(line, index):
    in_string = False
    for i, char in enumerate(line):
        if char in ['"', "'"]:
            in_string = not in_string
        if i >= index:
            break
    return in_string

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

                block_comment_start = clean_line.find(start_symbol)
                if block_comment_start != -1:
                    in_block_comment = True
                    comment_chars += len(clean_line) - block_comment_start
                    end_block_index = clean_line.find(end_symbol, block_comment_start)
                    if end_block_index != -1:
                        comment_chars -= len(clean_line) - end_block_index
                        in_block_comment = False
                    continue

            if line_symbol:
                line_comment_start = clean_line.find(line_symbol)
                if line_comment_start != -1 and not is_inside_string(clean_line, line_comment_start):
                    comment_chars += len(clean_line) - line_comment_start

    return comment_chars, total_chars

def calculate_comment_percentage(file_paths, min_ratio, show_failed, export):
    max_length = max(len(path) for path in file_paths)

    total_comment_chars = 0
    total_chars = 0

    results = []

    for file_path in file_paths:
        comment_chars, file_chars = count_comments(file_path)

        if file_chars > 0:
            comment_ratio = comment_chars / file_chars * 100
            color = "\033[92m" if comment_ratio >= min_ratio else ("\033[93m" if min_ratio - 5 <= comment_ratio <= min_ratio + 5 else "\033[91m")
            
            if show_failed == False or comment_ratio < min_ratio:
                print(f"File: {file_path.ljust(max_length)} | Comment Percentage: {color}{comment_ratio:.2f}%\033[0m")
        
            results.append((file_path, comment_ratio))

        else :
            print(f"File: {file_path.ljust(max_length)} | Comment Percentage: No calculable comments (empty or non-code file)")

        total_comment_chars += comment_chars
        total_chars += file_chars

    if total_chars > 0:
        total_comment_ratio = total_comment_chars / total_chars * 100
        color = "\033[92m" if total_comment_ratio >= min_ratio else ("\033[93m" if min_ratio - 5 <= total_comment_ratio <= min_ratio + 5 else "\033[91m")
        print(f"Global Comment Percentage: {color}{total_comment_chars / total_chars * 100:.2f}%\033[0m")
    else:
        print("No files found or files are empty.")

    if export:
        with open(export, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['File Path', 'Comment Percentage'])

            for file_path, comment_ratio in results:
                writer.writerow([file_path, f"{comment_ratio:.2f}%"])

def is_excluded_directory(root, exclude_dir, warned_patterns):
    for pattern in exclude_dir:
        if pattern in warned_patterns:
            continue
        try:
            if re.search(pattern, root):
                return True
        except re.error as e:
            if pattern not in warned_patterns:
                print(f"Avertissement : Expression régulière invalide '{pattern}' - {e}")
                warned_patterns.add(pattern)
    return False

def is_excluded_file(file, include_ext, exclude_ext, config):
    file_extension = os.path.splitext(file)[1].lower()
    if include_ext and file_extension not in include_ext:
        return True
    if exclude_ext and file_extension in exclude_ext:
        return True
    if file_extension not in config["comment_symbols_map"]:
        return True
    return False

def find_files(path, config, include_ext=None, exclude_ext=None, exclude_dir=None):
    found_files = []
    script_file = os.path.abspath(sys.argv[0])
    warned_patterns = set()

    if os.path.isfile(path):
        if path != script_file and not is_excluded_file(os.path.basename(path), include_ext, exclude_ext, config):
            found_files.append(path)
        return found_files

    for root, _, file_list in os.walk(path):
        if exclude_dir and is_excluded_directory(root, exclude_dir, warned_patterns):
            continue

        for file in file_list:
            full_path = os.path.join(root, file)
            if full_path != script_file and not is_excluded_file(file, include_ext, exclude_ext, config):
                found_files.append(full_path)

    return found_files


if __name__ == "__main__":
    colorama.init()
    config = load_config('config.json')

    parser = argparse.ArgumentParser(description='Calculate Comment Percentage in Code')
    parser.add_argument('--path', type=str, default=os.getcwd(), help='Path to the project folder (default: current directory)')
    parser.add_argument('--ratio', type=float, default=30, help='Minimum acceptable comment percentage (default: 30)')
    parser.add_argument('--include-ext', nargs='*', help='Extensions to include (e.g., .py .js)')
    parser.add_argument('--exclude-ext', nargs='*', help='Extensions to exclude (e.g., .md .txt)')
    parser.add_argument('--exclude-dir', nargs='*', help='Directories to exclude (supports regex)')
    parser.add_argument('--show-failed', default=False, help='Print only files that fail to meet the minimum comment percentage')
    parser.add_argument('--export', type=str, default=None, help='Export result to csv format file')
    args = parser.parse_args()

    file_paths = find_files(args.path, config, args.include_ext, args.exclude_ext, args.exclude_dir)

    if not file_paths:
        print("No matching files found.")
        sys.exit(1)

    calculate_comment_percentage(file_paths, args.ratio, args.show_failed, args.export)
