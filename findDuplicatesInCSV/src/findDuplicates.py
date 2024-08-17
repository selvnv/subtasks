import argparse
import os
import pandas as pd

def find_duplicates(input_file, field_name, out_dir):
    """
    Поиск дубликатов в csv файле input_file по полю field_name
    Запись в каталог out_dir двух файлов:
        - unique.csv (содержит данные без дублей)
        - duplicates.csv (содержит дублирующиеся строки)
    """

    # Проверка существования пути
    if os.path.exists(input_file) != True:
        print(f'File {input_file} does not exist!')
        return
    elif os.path.exists(out_dir) != True:
        print(f'Path {out_dir} does not exists!')
        return
    
    df = pd.read_csv(input_file)

    # Важжно, чтобы в csv файле не было лишних пробелов в начале и конце строки
    if field_name not in df.columns:
        raise KeyError(f"Столбец '{field_name}' не найден. Доступные столбцы: {list(df.columns)}")

    # Найти дубликаты по field_name (записываются все дубликаты)
    df_duplicates = df[df.duplicated(subset=field_name, keep=False)]

    # Записать уникальные строки (первое вхождение со сбросом индексов)
    df_unique = df.drop_duplicates(subset=field_name, ignore_index=True)


    df_unique.to_csv(path_or_buf=os.path.join(out_dir, 'unique.csv'), index=False)
    df_duplicates.to_csv(path_or_buf=os.path.join(out_dir, 'duplicates.csv'), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input data paths')

    parser.add_argument('-i', '--input_file', type=str, default='data/input.csv', help='Source file to parse')
    parser.add_argument('-f', '--field', type=str, default='column', help='Fsield to find duplicates')
    parser.add_argument('-o', '--out_dir', type=str, default='output/', help='Output directory to write unique.csv and duplicate.csv')

    args = parser.parse_args()

    find_duplicates(os.path.normpath(args.input_file), args.field, args.out_dir)