import json
import re

COMPUTER_TYPES = {
    "ноутбук",
    "игровой ноутбук",
    "ультрабук",
    "трансформер",
    "системный блок",
    "моноблок",
}


def processed_specs(product):
    return _parse_computer_specs(product)


def _parse_computer_specs(product):
    details = _cleaned_dict(product["parsed_details"])

    product_type = details.get("Тип")
    if product_type not in COMPUTER_TYPES:
        return

    cpu = details.get("Процессор", "")
    cpu = cpu.lower()

    gpu = details.get("Видеопроцессор", details.get("Видеокарта"))
    gpu = _cleaned_gpu(gpu)

    hertz = details.get("Частота процессора", details.get("Производительность"))
    hertz = _extract_hertz(hertz)

    cores = details.get("Количество ядер процессора", details.get("Производительность"))
    cores = _extract_cores(cores)

    ram = details.get("Размер оперативной памяти", details.get("Оперативная память"))
    ram_size = _extract_ram_size(ram)
    ram_type = _extract_ram_type(ram)

    ssd = details.get("Твердотельный диск (SSD)", details.get("Тип жесткого диска"))
    ssd = _extract_ssd(ssd)

    drive_size = details.get(
        "Объем жесткого диска", details.get("Общий объем накопителей")
    )
    drive_size = _extract_drive_size(drive_size)

    return {
        "product_id": product["id"],
        "type": product_type,
        "cpu": cpu,
        "hertz": hertz,
        "cores": cores,
        "gpu": gpu,
        "ram": ram_size,
        "ram_type": ram_type,
        "ssd": ssd,
        "drive_size": drive_size,
        "extra": json.dumps(details, ensure_ascii=False),
    }


def _cleaned_dict(d: dict):
    return {k: v.strip().replace("&nbsp", " ") for k, v in d.items()}


def _cleaned_gpu(gpu: str):
    """
    Clean GPU

    GPU:
        if any russian letter in the word, drop the word
            - but if ends with "," then add "+"
        if only english letters in the word and it ends with ","
            - then add word
            - then add "+"
    """
    if not gpu:
        return

    words = gpu.split()
    result = []
    for word in words:
        if word == "и":
            result.append("+")
            continue

        if "в" in word or "д" in word:
            if word.endswith(","):
                result.append("+")
            continue

        if word.endswith(","):
            result.append(word[:-1])
            result.append("+")
            continue

        result.append(word)

    return " ".join(result).strip("+").strip().lower()


def _extract_hertz(raw_hertz: str):
    """
    Extract hertz

    Hertz:
        - 2-х ядерный 2.4 ГГц
        - 4-х ядерный, 1.6 ГГц
        - 1600 МГц, 4 ядра
        - 2000 MHz, 4 ядра
        - 8 ядер
        - 4 ядра
        - 2 ядра, 2300 МГц
        - 3.9 МГц
        - 1,6 ГГц - ускорение Turbo Boost до 3,9 ГГц
    """
    if not raw_hertz:
        return

    patterns_mhz = (r"(\d\d\d\d)",)
    for pattern in patterns_mhz:
        match = re.search(pattern, raw_hertz)
        if match:
            return match.group()

    patterns_ghz = (
        r"(\d\.\d)",
        r"(\d,\d)",
    )
    for pattern in patterns_ghz:
        match = re.search(pattern, raw_hertz)
        if match:
            hertz = float(match.group().replace(",", ".")) * 1000
            return int(hertz)


def _extract_cores(raw_cores: str):
    """
    Extract cores number

    raw_cores:
        - 2-х ядерный 2.4 ГГц
        - 4-х ядерный, 1.6 ГГц
        - 1600 МГц, 4 ядра
        - 2000 MHz, 4 ядра
        - 8 ядер
        - 4 ядра
    """
    if not raw_cores:
        return

    patterns = (
        r"(\d+)-х ядерный",
        r"(\d) ядра",
        r"(\d) ядер",
    )
    for pattern in patterns:
        match = re.search(pattern, raw_cores)
        if match:
            return match.group(1)


def _extract_ram_size(raw_ram: str):
    """
    Extract RAM size

    raw_ram:
        - 8 ГБ, 8 Гб, 8Гб
        - 8 GB, 8 Gb, 8Gb
    """
    if not raw_ram:
        return

    patterns_size = (
        r"(\d)\s*[Гг][Бб]",
        r"(\d)\s*[Gg][Bb]",
    )

    for pattern in patterns_size:
        match = re.search(pattern, raw_ram)
        if match:
            return match.group(1)


def _extract_ram_type(ram: str):
    """Extract RAM type (DDR3, DDR4, etc.)"""
    if not ram:
        return

    pattern = r"L?P?DDR\d[Lx]?"
    match = re.search(pattern, ram)
    if match:
        return match.group()


def _extract_ssd(ssd: str):
    return ssd and (ssd == "да" or "SSD" in ssd)


def _extract_drive_size(drive_size: str):
    """
    Extract Drive size

    drive_size:
        - 1024 Гб
    """
    if not drive_size:
        return

    pattern = r"(\d+) \w{2}"
    match = re.search(pattern, drive_size)
    if match:
        return match.group(1)
