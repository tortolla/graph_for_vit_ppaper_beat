import csv
import matplotlib.pyplot as plt
import numpy as np

# Считываем из файла зависимости
def read_csv_to_dict(file_path):
    """
    Читает CSV-файл и возвращает данные в виде словаря,
    где ключи - названия столбцов, а значения - списки данных из этих столбцов.

    :param file_path: Строка, путь к CSV-файлу.
    :return: Словарь с данными из CSV.
    """
    data_dict = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Чтение заголовков столбцов
        for header in headers:
            data_dict[header] = []  # Инициализация списка для каждого заголовка
        for row in reader:
            for header, value in zip(headers, row):
                data_dict[header].append(value)

    return data_dict

# Перевод периода в частоту
def period_to_frequency(period):
    return 1.0 / period


# Строим зависимости
def plot_dependencies(data_dict, output_path):
    """
    Строит зависимости вида d_xx(t_xx) для всех найденных пар в словаре данных и сохраняет график в файл.

    :param data_dict: Словарь с данными, где ключи - названия столбцов.
    :param output_path: Строка, путь для сохранения файла.
    """
    fig, ax = plt.subplots(figsize=(10, 6))  # Создаем фигуру и оси

    period_labels = [2, 10, 20, 60, 120, 300]
    frequency_labels = [period_to_frequency(period) for period in period_labels]
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(frequency_labels)))  # Цветовая карта от синего к красному

    for idx, period in enumerate(period_labels):
        key = f'd_{period}'
        time_key = f't_{period}'
        if key in data_dict and time_key in data_dict:  # Проверяем, существуют ли соответствующие столбцы
            # Преобразование строк в числа, игнорируя пустые значения
            time_values = [float(x) for x in data_dict[time_key] if x]
            distance_values = [float(x) for x in data_dict[key] if x]

            if len(time_values) == len(distance_values):  # Убедимся, что списки совпадают по длине
                ax.scatter(time_values, distance_values, label=f'{period} sec', color=colors[idx], s=1)
            else:
                print(f'Warning: Mismatched lengths for {key} and {time_key}')

    ax.set_xlabel('Time (sec)')  # Подпись оси X
    ax.set_ylabel('Conductivity (S)')  # Подпись оси Y

    # Добавляем цветовую шкалу
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, norm=plt.Normalize(vmin=min(frequency_labels), vmax=max(frequency_labels)))
    sm.set_array([])  # Выдаем массив значений для цветовой шкалы
    cbar = fig.colorbar(sm, ax=ax)  # Добавляем цветовую шкалу к фигуре
    cbar.set_label('Frequency (Hz)', labelpad=20)

    # Добавляем равномерно распределенные метки на цветовую шкалу
    cbar_ticks = np.linspace(min(frequency_labels), max(frequency_labels), num=6)
    cbar.set_ticks(cbar_ticks)
    cbar.set_ticklabels([f'{tick:.2f} Hz' for tick in cbar_ticks])

    # Сохраняем график в файл с качеством 3000 DPI
    plt.savefig(output_path, dpi=3000, bbox_inches='tight')



# Пример использования функции
file_path = '/Users/tortolla/Downloads/Data_for_Viktor 3/Wn_200_proc.csv'  # Укажите здесь актуальный путь к вашему файлу
data_dict = read_csv_to_dict(file_path)

output_path = '/Users/tortolla/Desktop/vit.png'
plot_dependencies(data_dict, output_path)



